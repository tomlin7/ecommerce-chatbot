import json
import logging
import threading
import uuid
from typing import Any, Dict, List, Optional

from flask import current_app
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.memory import ConversationBufferWindowMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import StructuredTool
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field

from models.chat_session import ChatSession
from models.message import Message
from models.product import Product

from .cart_service import CartService
from .product_service import ProductService
from .vector_service import VectorService

logger = logging.getLogger(__name__)

# Thread-local storage so each Gunicorn worker tracks its own request context
_request_ctx = threading.local()


# ── Tool input schemas (what the LLM sees) ──────────────────────────────────

class SearchInput(BaseModel):
    query: str = Field(description="Поисковый запрос — описание нужного товара на русском или английском")


class FilterInput(BaseModel):
    category: Optional[str] = Field(None, description="Категория товара: овощи, фрукты, молочные продукты, мясо, выпечка, мёд и сухофрукты")
    subcategory: Optional[str] = Field(None, description="Подкатегория, например: помидоры, сыры, говядина")
    brand: Optional[str] = Field(None, description="Название фермы или бренда")
    min_price: Optional[float] = Field(None, description="Минимальная цена в тенге")
    max_price: Optional[float] = Field(None, description="Максимальная цена в тенге")
    min_rating: Optional[float] = Field(None, description="Минимальный рейтинг от 1 до 5")
    in_stock_only: bool = Field(False, description="True — показывать только товары в наличии")
    search_query: Optional[str] = Field(None, description="Дополнительный текстовый поиск внутри результатов")
    limit: int = Field(8, description="Максимальное количество результатов (1-20)")


class ProductIdInput(BaseModel):
    product_id: str = Field(description="ID товара (UUID из результатов поиска)")


class RecommendInput(BaseModel):
    query: str = Field(description="ID товара для похожих рекомендаций, либо описание предпочтений пользователя")


class AddToCartInput(BaseModel):
    product_id: str = Field(description="ID товара (UUID из результатов поиска) или точное название товара")
    quantity: int = Field(1, ge=1, le=20, description="Количество единиц товара")


# ── Chat service ─────────────────────────────────────────────────────────────

class ChatService:
    """LangChain + Gemini chat service for the farm e-commerce assistant."""

    def __init__(self):
        self.llm: Optional[ChatGoogleGenerativeAI] = None
        self.vector_service = VectorService()
        self.product_service = ProductService()
        self.cart_service = CartService()
        self.memory_sessions: Dict[str, ConversationBufferWindowMemory] = {}
        self._tools: Optional[List] = None
        self._agent = None
        self._prompt: Optional[ChatPromptTemplate] = None
        self.initialized = False

    # ── Initialization ───────────────────────────────────────────────────────

    def initialize(self):
        """Build LLM, tools, prompt and agent — called once on first use."""
        try:
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",
                google_api_key=current_app.config["GOOGLE_API_KEY"],
                temperature=0.3,      # deterministic enough for product queries
                max_tokens=4096,      # generous room for complete answers
            )
            self.vector_service.initialize()
            self._tools = self._build_tools()
            self._prompt = self._build_prompt()
            self._agent = create_tool_calling_agent(self.llm, self._tools, self._prompt)
            self.initialized = True
            logger.info("ChatService initialized successfully")
        except Exception as e:
            logger.error(f"ChatService init failed: {e}")
            raise

    # ── Prompt ───────────────────────────────────────────────────────────────

    def _build_prompt(self) -> ChatPromptTemplate:
        system = (
            "Ты — Farmy, умный ИИ-помощник фермерского интернет-магазина. "
            "Помогаешь покупателям найти свежие фермерские продукты.\n\n"
            "ОБЯЗАТЕЛЬНЫЕ ПРАВИЛА:\n"
            "1. Всегда отвечай на РУССКОМ языке — независимо от языка вопроса.\n"
            "2. Используй инструменты для поиска товаров — никогда не выдумывай названия, цены или ID.\n"
            "3. В каждом ответе давай конкретные товары с ценами и характеристиками.\n"
            "4. Если запрос неясен — задай один уточняющий вопрос.\n"
            "5. Для добавления в корзину: сначала найди товар через search_products или filter_products, "
            "   затем используй полученный product_id в add_to_cart.\n\n"
            "КОГДА ИСПОЛЬЗОВАТЬ ИНСТРУМЕНТЫ:\n"
            "• search_products — семантический поиск по описанию (например: «сладкие яблоки», «свежее молоко»)\n"
            "• filter_products — фильтрация по категории, цене, рейтингу, наличию\n"
            "• get_product_details — подробности конкретного товара (нужен product_id)\n"
            "• get_recommendations — похожие товары (по product_id или предпочтениям)\n"
            "• add_to_cart — добавить товар в корзину (нужен product_id из поиска)\n\n"
            "Категории магазина: овощи, фрукты, молочные продукты, мясо, выпечка, мёд и сухофрукты.\n"
            "Все цены в тенге (₸)."
        )
        return ChatPromptTemplate.from_messages([
            ("system", system),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])

    # ── Tools ────────────────────────────────────────────────────────────────

    def _build_tools(self) -> List:
        return [
            StructuredTool.from_function(
                func=self._search_products,
                name="search_products",
                description="Семантический поиск фермерских товаров по описанию пользователя",
                args_schema=SearchInput,
            ),
            StructuredTool.from_function(
                func=self._filter_products,
                name="filter_products",
                description="Фильтрация товаров по категории, цене, рейтингу или наличию",
                args_schema=FilterInput,
            ),
            StructuredTool.from_function(
                func=self._get_product_details,
                name="get_product_details",
                description="Получить полные подробности о конкретном товаре по его ID",
                args_schema=ProductIdInput,
            ),
            StructuredTool.from_function(
                func=self._get_recommendations,
                name="get_recommendations",
                description="Получить похожие товары или персонализированные рекомендации",
                args_schema=RecommendInput,
            ),
            StructuredTool.from_function(
                func=self._add_to_cart,
                name="add_to_cart",
                description="Добавить товар в корзину пользователя",
                args_schema=AddToCartInput,
            ),
        ]

    def _search_products(self, query: str) -> str:
        try:
            similar = self.vector_service.search_similar_products(query, top_k=6)
            if not similar:
                return json.dumps({"message": "Товары по запросу не найдены.", "product_ids": []})

            ids = [p["id"] for p in similar]
            products = (
                Product.query
                .filter(Product.id.in_(ids), Product.is_active == True)
                .all()
            )

            if not products:
                return json.dumps({"message": "Товары не найдены.", "product_ids": []})

            lines = [f"Найдено {len(products)} товаров:"]
            for p in products:
                stock = "в наличии" if p.is_in_stock() else "нет в наличии"
                organic = " [органик]" if p.organic_certified else ""
                lines.append(
                    f"• ID: {p.id} | {p.name}{organic} ({p.brand}) — {p.price}₸ | "
                    f"рейтинг {p.rating}/5 | {stock}"
                )
                lines.append(f"  {p.description[:120]}")

            return json.dumps({"message": "\n".join(lines), "product_ids": ids})
        except Exception as e:
            logger.error(f"search_products error: {e}")
            return json.dumps({"message": "Ошибка при поиске товаров.", "product_ids": []})

    def _filter_products(
        self,
        category: Optional[str] = None,
        subcategory: Optional[str] = None,
        brand: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        min_rating: Optional[float] = None,
        in_stock_only: bool = False,
        search_query: Optional[str] = None,
        limit: int = 8,
    ) -> str:
        try:
            products = Product.search_by_filters(
                category=category,
                subcategory=subcategory,
                brand=brand,
                min_price=min_price,
                max_price=max_price,
                min_rating=min_rating,
                in_stock_only=in_stock_only,
                search_query=search_query,
                limit=limit,
            )

            if not products:
                return json.dumps({
                    "message": "Товары по заданным фильтрам не найдены.",
                    "product_ids": [],
                })

            lines = [f"Найдено {len(products)} товаров:"]
            for p in products:
                stock = "в наличии" if p.is_in_stock() else "нет в наличии"
                organic = " [органик]" if p.organic_certified else ""
                lines.append(
                    f"• ID: {p.id} | {p.name}{organic} ({p.brand}) — {p.price}₸ | "
                    f"рейтинг {p.rating}/5 | {stock}"
                )

            ids = [p.id for p in products]
            return json.dumps({"message": "\n".join(lines), "product_ids": ids})
        except Exception as e:
            logger.error(f"filter_products error: {e}")
            return json.dumps({"message": "Ошибка при фильтрации товаров.", "product_ids": []})

    def _get_product_details(self, product_id: str) -> str:
        try:
            product = Product.query.get(product_id.strip())
            if not product:
                return f"Товар с ID '{product_id}' не найден."

            lines = [
                f"Товар: {product.name}",
                f"Ферма/Бренд: {product.brand}",
                f"Цена: {product.price}₸",
                f"Рейтинг: {product.rating}/5 ({product.review_count} отзывов)",
                f"Наличие: {product.stock} шт.",
                f"Категория: {product.category} / {product.subcategory}",
                f"Описание: {product.description}",
            ]
            features = product.get_features()
            if features:
                lines.append(f"Характеристики: {', '.join(features)}")
            if product.organic_certified:
                lines.append("Органическая сертификация: да")
            if product.harvest_date:
                lines.append(f"Дата сбора урожая: {product.harvest_date.isoformat()}")
            if product.unit_type:
                lines.append(f"Единица измерения: {product.unit_type}")

            return "\n".join(lines)
        except Exception as e:
            logger.error(f"get_product_details error: {e}")
            return "Ошибка при получении информации о товаре."

    def _get_recommendations(self, query: str) -> str:
        try:
            # Try to treat query as product ID first, fall back to text search
            product = Product.query.get(query.strip())
            search_text = product.get_search_text() if product else query

            similar = self.vector_service.search_similar_products(search_text, top_k=5)
            ids = [p["id"] for p in similar if p["id"] != query][:4]

            if not ids:
                return json.dumps({"message": "Рекомендации не найдены.", "product_ids": []})

            recommendations = Product.query.filter(Product.id.in_(ids)).all()
            if not recommendations:
                return json.dumps({"message": "Рекомендации не найдены.", "product_ids": []})

            lines = ["Рекомендуем:"]
            for p in recommendations:
                lines.append(f"• ID: {p.id} | {p.name} ({p.brand}) — {p.price}₸")

            return json.dumps({"message": "\n".join(lines), "product_ids": ids})
        except Exception as e:
            logger.error(f"get_recommendations error: {e}")
            return json.dumps({"message": "Ошибка при получении рекомендаций.", "product_ids": []})

    def _add_to_cart(self, product_id: str, quantity: int = 1) -> str:
        try:
            user_id = getattr(_request_ctx, "user_id", "guest_user")

            # Resolve product name → ID if the value doesn't look like a UUID
            if len(product_id) < 32 or " " in product_id:
                product = Product.query.filter(
                    Product.name.ilike(f"%{product_id}%")
                ).first()
                if not product:
                    return json.dumps({
                        "message": f"Товар '{product_id}' не найден. Сначала найди товар через search_products.",
                        "success": False,
                    })
                product_id = product.id

            product = Product.query.get(product_id)
            if not product:
                return json.dumps({"message": "Товар не найден.", "success": False})

            result = self.cart_service.add_to_cart(user_id, product_id, quantity)
            if not result.get("success", True):
                return json.dumps(result)

            return json.dumps({
                "message": f"Добавлено в корзину: {quantity} × {product.name} ({product.price}₸)",
                "success": True,
                "product_id": product_id,
            })
        except Exception as e:
            logger.error(f"add_to_cart error: {e}")
            return json.dumps({"message": "Ошибка при добавлении в корзину.", "success": False})

    # ── Memory ───────────────────────────────────────────────────────────────

    def get_or_create_memory(self, session_id: str) -> ConversationBufferWindowMemory:
        if session_id not in self.memory_sessions:
            self.memory_sessions[session_id] = ConversationBufferWindowMemory(
                k=10,
                return_messages=True,
                memory_key="chat_history",
            )
        return self.memory_sessions[session_id]

    # ── Main entry point ─────────────────────────────────────────────────────

    def process_message(
        self, session_id: str, user_message: str, user_id: str = None
    ) -> Dict[str, Any]:
        if not self.initialized:
            self.initialize()

        # Make user_id available to tools in this thread
        _request_ctx.user_id = user_id or "guest_user"

        try:
            self._ensure_session(session_id, user_id)
            self._save_user_message(session_id, user_message)

            memory = self.get_or_create_memory(session_id)
            executor = AgentExecutor(
                agent=self._agent,
                tools=self._tools,
                memory=memory,
                verbose=True,
                handle_parsing_errors=(
                    "Parsing error — re-read the tool schema and retry with correct arguments."
                ),
                max_iterations=8,
                max_execution_time=50,
                return_intermediate_steps=True,
            )

            result = executor.invoke({"input": user_message})
            ai_text = result.get("output", "").strip()

            if not ai_text:
                logger.warning("Agent returned empty output, using direct LLM fallback")
                ai_text = self._direct_llm_fallback(user_message, memory)

            product_ids = self._extract_product_ids(result.get("intermediate_steps", []))
            return self._save_and_return(session_id, ai_text, product_ids)

        except Exception as e:
            logger.error(f"process_message error: {e}", exc_info=True)
            return self._error_response(session_id)

    # ── Helpers ──────────────────────────────────────────────────────────────

    def _ensure_session(self, session_id: str, user_id: Optional[str]):
        if not ChatSession.query.get(session_id):
            from app import db
            db.session.add(ChatSession(id=session_id, user_id=user_id))
            db.session.commit()

    def _save_user_message(self, session_id: str, content: str):
        from app import db
        db.session.add(Message(
            id=str(uuid.uuid4()),
            chat_session_id=session_id,
            content=content,
            is_bot=False,
        ))
        db.session.commit()

    def _save_and_return(
        self, session_id: str, ai_text: str, product_ids: List[str]
    ) -> Dict[str, Any]:
        from app import db
        ai_msg = Message(
            id=str(uuid.uuid4()),
            chat_session_id=session_id,
            content=ai_text,
            is_bot=True,
            message_type="product" if product_ids else "text",
            products=product_ids,
        )
        db.session.add(ai_msg)
        db.session.commit()

        products = []
        for pid in product_ids:
            p = Product.query.get(pid)
            if p:
                products.append(p.to_dict())

        return {
            "id": ai_msg.id,
            "content": ai_text,
            "isBot": True,
            "timestamp": ai_msg.created_at.isoformat(),
            "products": products,
            "type": ai_msg.message_type,
        }

    def _direct_llm_fallback(
        self, user_message: str, memory: ConversationBufferWindowMemory
    ) -> str:
        """Called when the agent executor produces empty output — ask the LLM directly."""
        try:
            recent = memory.chat_memory.messages[-6:] if memory.chat_memory.messages else []
            history = [
                ("human" if m.type == "human" else "ai", m.content)
                for m in recent
            ]
            messages = (
                [("system",
                  "Ты — Farmy, помощник фермерского магазина. "
                  "Ответь на вопрос пользователя на русском языке. "
                  "Если нужно найти товары, предложи уточнить запрос.")]
                + history
                + [("human", user_message)]
            )
            response = self.llm.invoke(messages)
            text = response.content.strip()
            return text or "Извините, не могу ответить сейчас. Попробуйте переформулировать вопрос."
        except Exception as e:
            logger.error(f"Direct LLM fallback error: {e}")
            return "Извините, произошла ошибка. Пожалуйста, попробуйте ещё раз."

    def _extract_product_ids(self, intermediate_steps: list) -> List[str]:
        """Deduplicated product IDs collected from tool outputs, preserving order."""
        seen: Dict[str, None] = {}
        for step in intermediate_steps:
            tool_name = getattr(step[0], "tool", None)
            if tool_name in {"search_products", "filter_products", "get_recommendations"}:
                try:
                    parsed = json.loads(step[1])
                    for pid in parsed.get("product_ids", []):
                        seen[pid] = None
                except Exception:
                    pass
        return list(seen.keys())

    def _error_response(self, session_id: str) -> Dict[str, Any]:
        try:
            from app import db
            msg = Message(
                id=str(uuid.uuid4()),
                chat_session_id=session_id,
                content="Извините, произошла ошибка. Пожалуйста, попробуйте ещё раз.",
                is_bot=True,
            )
            db.session.add(msg)
            db.session.commit()
            return {
                "id": msg.id,
                "content": msg.content,
                "isBot": True,
                "timestamp": msg.created_at.isoformat(),
                "products": [],
                "type": "text",
            }
        except Exception:
            return {
                "id": str(uuid.uuid4()),
                "content": "Произошла ошибка. Попробуйте ещё раз.",
                "isBot": True,
                "timestamp": "",
                "products": [],
                "type": "text",
            }

    # ── History ──────────────────────────────────────────────────────────────

    def get_chat_history(
        self, session_id: str, limit: int = 50
    ) -> List[Dict[str, Any]]:
        try:
            messages = (
                Message.query.filter_by(chat_session_id=session_id)
                .order_by(Message.created_at.asc())
                .limit(limit)
                .all()
            )
            return [msg.to_dict(include_product_details=True) for msg in messages]
        except Exception as e:
            logger.error(f"get_chat_history error: {e}")
            return []

    def clear_session_memory(self, session_id: str):
        self.memory_sessions.pop(session_id, None)
