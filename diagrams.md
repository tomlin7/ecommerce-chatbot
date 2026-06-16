# Диаграммы проекта — Фермерский интернет-магазин с ИИ-ассистентом

---

## 1. ER-диаграмма (Entity-Relationship)

```mermaid
erDiagram
    USER {
        string id PK
        string email UK
        string name
        string password_hash
        text   preferences
        bool   is_active
        datetime created_at
        datetime updated_at
    }

    CHAT_SESSION {
        string   id PK
        string   user_id FK
        text     session_data
        bool     is_active
        datetime created_at
        datetime updated_at
    }

    MESSAGE {
        string   id PK
        string   chat_session_id FK
        text     content
        bool     is_bot
        string   message_type
        text     products
        text     extra_data
        datetime created_at
    }

    PRODUCT {
        string  id PK
        string  name
        text    description
        float   price
        float   original_price
        string  category
        string  subcategory
        string  brand
        float   rating
        int     review_count
        string  image_url
        int     stock
        text    features
        bool    is_on_sale
        int     sale_percentage
        bool    is_active
        string  embedding_id
        date    harvest_date
        string  farm_location
        bool    is_seasonal
        bool    organic_certified
        string  unit_type
        string  season
        datetime created_at
        datetime updated_at
    }

    FARM {
        string  id PK
        string  name
        text    description
        string  location
        string  address
        float   latitude
        float   longitude
        string  phone
        string  email
        string  website
        string  image_url
        text    gallery
        text    story
        text    practices
        text    certifications
        int     established_year
        float   acreage
        bool    is_active
        datetime created_at
        datetime updated_at
    }

    CART {
        string   id PK
        string   user_id FK
        string   product_id FK
        int      quantity
        datetime created_at
        datetime updated_at
    }

    USER_LIKE {
        string   id PK
        string   user_id FK
        string   product_id FK
        datetime created_at
    }

    USER         ||--o{ CHAT_SESSION : "ведёт"
    CHAT_SESSION ||--o{ MESSAGE      : "содержит"
    USER         ||--o{ CART         : "имеет"
    USER         ||--o{ USER_LIKE    : "лайкает"
    PRODUCT      ||--o{ CART         : "добавляется в"
    PRODUCT      ||--o{ USER_LIKE    : "получает"
```

---

## 2. IDEF0-диаграмма (функциональная декомпозиция)

### Контекстная диаграмма A-0

```mermaid
flowchart TB
    subgraph CONTROLS["🔒 Управление"]
        C1[JWT-аутентификация]
        C2[Бизнес-правила]
        C3[Языковые правила Gemini]
    end

    subgraph INPUTS["📥 Входы"]
        I1[Запрос пользователя]
        I2[Учётные данные]
        I3[Параметры фильтров]
    end

    subgraph FUNCTION["⚙️  A0: Фермерский магазин\nс ИИ-ассистентом"]
        F["🌾 СИСТЕМА"]
    end

    subgraph OUTPUTS["📤 Выходы"]
        O1[Ответ ИИ + карточки товаров]
        O2[Данные корзины / заказа]
        O3[Рекомендации]
        O4[JWT-токены]
    end

    subgraph MECHANISMS["🛠  Механизмы"]
        M1[Flask + Gunicorn]
        M2[Next.js]
        M3[Gemini 2.5 Flash]
        M4[Pinecone]
        M5[SQLite]
    end

    INPUTS   --> FUNCTION
    CONTROLS --> FUNCTION
    FUNCTION --> OUTPUTS
    MECHANISMS --> FUNCTION
```

### Декомпозиция A0 — уровень функций

```mermaid
flowchart LR
    U([Пользователь]) --> A1 & A2 & A4

    subgraph A1["A1 · Управление\nпользователями"]
        direction TB
        a1i[Регистрация\nВход\nПредпочтения]
    end

    subgraph A2["A2 · Управление\nкаталогом"]
        direction TB
        a2i[Просмотр товаров\nФильтрация\nПоиск]
    end

    subgraph A3["A3 · ИИ-чат\nассистент"]
        direction TB
        a3i[Обработка запроса\nВекторный поиск\nГенерация ответа]
    end

    subgraph A4["A4 · Управление\nкорзиной"]
        direction TB
        a4i[Добавление\nИзменение\nОформление]
    end

    subgraph A5["A5 · Управление\nфермами"]
        direction TB
        a5i[Профили ферм\nСезонный календарь\nОрганик-сертификат]
    end

    A1 -- JWT токен --> A2 & A3 & A4
    A2 -- Данные товаров --> A3
    A3 -- Рекомендованные ID --> A4
    A5 -- Данные фермы --> A2

    A1 --> DB[(SQLite)]
    A2 --> DB
    A3 --> PC[(Pinecone)]
    A3 --> LLM([Gemini 2.5 Flash])
    A4 --> DB
    A5 --> DB
```

### Декомпозиция A3 — ИИ-чат (детально)

```mermaid
flowchart TD
    MSG([Сообщение\nпользователя])

    subgraph A3["A3 · ИИ-чат ассистент"]
        A31["A3.1\nСохранить сообщение\nв БД"]
        A32["A3.2\nЗагрузить историю\nсессии (10 сообщений)"]
        A33["A3.3\nLangChain AgentExecutor\n(Gemini выбирает инструмент)"]

        subgraph TOOLS["Инструменты агента"]
            T1[search_products]
            T2[filter_products]
            T3[get_product_details]
            T4[get_recommendations]
            T5[add_to_cart]
        end

        A34["A3.4\nИзвлечь product_ids\nиз intermediate_steps"]
        A35["A3.5\nСохранить ответ бота\n+ product_ids в БД"]
        A36["A3.6\nВернуть ответ\n+ карточки товаров"]
    end

    MSG --> A31 --> A32 --> A33
    A33 --> T1 & T2 & T3 & T4 & T5
    T1 & T2 & T4 --> VEC[(Pinecone\nвекторный поиск)]
    T5 --> DB[(SQLite)]
    A33 --> A34 --> A35 --> A36

    A36 --> RESP([Ответ + товары\nна фронтенд])
```

---

## 3. Архитектурная диаграмма

```mermaid
graph TB
    subgraph CLIENT["🌐 Клиент (Браузер)"]
        UI["Next.js 15\nport :3000\n─────────────\nСтраницы:\n• / Главная\n• /chat ИИ-ассистент\n• /products Каталог\n• /cart Корзина\n• /profile Профиль\n─────────────\nКомпоненты:\nProductCard · ChatMessage\nProductFilters · HarvestInfo\nSeasonalCalendar"]
    end

    subgraph DOCKER["🐳 Docker Compose"]
        subgraph SERVER["server (port :5000)"]
            GUN["Gunicorn\n1 worker · timeout 300s"]
            FLASK["Flask API\n─────────────\nRoutes:\n/auth · /chat\n/products · /cart\n/farms · /likes"]
            SERVICES["Services:\nAuthService\nChatService\nVectorService\nProductService\nCartService"]
            GUN --> FLASK --> SERVICES
        end

        subgraph WEB["web (port :3000)"]
            UI
        end

        SQLITE[("💾 SQLite\n(volume)\n─────────────\nusers\nproducts\nfarms\nchat_sessions\nmessages\ncart\nuser_likes")]
    end

    subgraph EXTERNAL["☁️  Внешние сервисы"]
        GEMINI["🤖 Google Gemini\n2.5 Flash\nLLM генерация\nответов"]
        PINECONE["🌲 Pinecone\nВекторная БД\n1024-dim\nmultilingual-e5"]
        HF["🤗 HuggingFace\nintfloat/\nmultilingual-e5-large\n(cached в образе)"]
    end

    UI        -- "HTTP Axios\nREST API" -->  FLASK
    FLASK     -- "JWT Auth\nSQL ORM"   -->  SQLITE
    SERVICES  -- "LangChain\nAgentExecutor" --> GEMINI
    SERVICES  -- "gRPC\nvector search" --> PINECONE
    SERVER    -- "baked at\nbuild time" --> HF

    PINECONE  -. "embeddings\nindex" .- SQLITE
```

### Диаграмма потока данных при чат-запросе

```mermaid
sequenceDiagram
    actor U as Пользователь
    participant FE as Next.js Frontend
    participant API as Flask API
    participant CS as ChatService
    participant VS as VectorService
    participant PC as Pinecone
    participant LLM as Gemini 2.5 Flash
    participant DB as SQLite

    U->>FE: Вводит сообщение
    FE->>API: POST /api/chat/message
    API->>DB: Сохранить сообщение пользователя
    API->>CS: process_message(session_id, text)
    CS->>DB: Загрузить историю сессии
    CS->>LLM: AgentExecutor.invoke(message + history)
    LLM-->>CS: Выбрать инструмент: search_products
    CS->>VS: search_similar_products(query)
    VS->>VS: encode("query: " + text)
    VS->>PC: vector query (top-k)
    PC-->>VS: matching product IDs + scores
    VS-->>CS: список товаров
    CS->>DB: Получить детали Product по ID
    DB-->>CS: данные товаров
    CS-->>LLM: результаты инструмента
    LLM-->>CS: финальный ответ (на русском)
    CS->>DB: Сохранить ответ бота + product_ids
    CS-->>API: {content, products[]}
    API-->>FE: {response, products, session_id}
    FE->>U: Показать сообщение + карточки товаров
```
