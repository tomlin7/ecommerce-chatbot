import json
import logging
import uuid
from datetime import datetime, date

from models.product import Product
from services.product_service import ProductService

logger = logging.getLogger(__name__)


class DatabaseSeeder:
    """Utility class for seeding the database with initial data"""

    def __init__(self, db):
        self.db = db
        self.product_service = ProductService()

    def seed_products(self):
        """Seed the database with sample products"""
        try:
            existing = Product.query.all()
            if existing:
                for p in existing:
                    self.db.session.delete(p)
                self.db.session.commit()
                logger.info(f"Deleted {len(existing)} old products")

            products_data = self._get_sample_products()

            logger.info(f"Seeding {len(products_data)} products...")

            for product_data in products_data:
                try:
                    product = Product(**product_data)
                    self.db.session.add(product)
                    self.db.session.flush()

                    search_text = product.get_search_text()
                    metadata = {
                        "category": product.category,
                        "subcategory": product.subcategory,
                        "brand": product.brand,
                        "price": product.price,
                        "rating": product.rating,
                        "in_stock": product.is_in_stock(),
                    }

                    self.product_service.vector_service.upsert_product_embedding(
                        product.id, search_text, metadata
                    )

                    product.embedding_id = product.id

                except Exception as e:
                    logger.error(
                        f"Error seeding product {product_data.get('name', 'Unknown')}: {str(e)}"
                    )
                    continue

            self.db.session.commit()
            logger.info("Products seeded successfully")

        except Exception as e:
            logger.error(f"Error seeding products: {str(e)}")
            self.db.session.rollback()
            raise

    def _get_sample_products(self):
        """Get sample farm product data"""
        return [
            {
                "id": str(uuid.uuid4()),
                "name": "Клубника органическая",
                "description": "Свежая, сочная органическая клубника, выращенная без пестицидов. Собрана вручную на пике спелости для максимальной сладости и вкуса.",
                "price": 1500.0,
                "original_price": 1800.0,
                "category": "Овощи и фрукты",
                "subcategory": "Ягоды",
                "brand": "Алтын Дала",
                "rating": 4.9,
                "review_count": 1247,
                "image_url": "https://images.unsplash.com/photo-1464965911861-746a04b4bca6?w=400&auto=format&fit=crop",
                "stock": 45,
                "features": ["Органическая", "Без ГМО", "Местная", "Сезонная"],
                "is_on_sale": True,
                "sale_percentage": 17,
                "harvest_date": date(2026, 6, 15),
                "farm_location": "Алматинская область",
                "is_seasonal": True,
                "organic_certified": True,
                "unit_type": "за кг",
                "season": "Лето",
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Яйца куриные домашние",
                "description": "Свежие яйца от счастливых кур свободного выгула. Богатый золотистый желток с исключительным вкусом и питательной ценностью.",
                "price": 900.0,
                "category": "Мясо и птица",
                "subcategory": "Яйца",
                "brand": "Жулдыз",
                "rating": 4.8,
                "review_count": 892,
                "image_url": "https://images.unsplash.com/photo-1582722872445-44dc5f7e3c8f?w=400&auto=format&fit=crop",
                "stock": 200,
                "features": ["Свободный выгул", "Натуральный корм", "Без антибиотиков", "Омега-3"],
                "harvest_date": date(2026, 6, 18),
                "farm_location": "Жамбылская область",
                "is_seasonal": False,
                "organic_certified": True,
                "unit_type": "10 штук",
                "season": "Круглый год",
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Мёд цветочный натуральный",
                "description": "Чистый нефильтрованный мёд с местных цветочных лугов. Никогда не нагревается и не обрабатывается — сохраняет природные ферменты и питательные вещества.",
                "price": 3500.0,
                "original_price": 4000.0,
                "category": "Мёд и сухофрукты",
                "subcategory": "Мёд",
                "brand": "Тау Бар",
                "rating": 4.9,
                "review_count": 567,
                "image_url": "https://images.unsplash.com/photo-1605880980331-20a711b27338?w=400&auto=format&fit=crop",
                "stock": 34,
                "features": ["Натуральный", "Нефильтрованный", "Местный", "Органический"],
                "is_on_sale": True,
                "sale_percentage": 13,
                "harvest_date": date(2026, 5, 20),
                "farm_location": "Алматинская область",
                "is_seasonal": True,
                "organic_certified": True,
                "unit_type": "за кг",
                "season": "Весна",
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Томаты черри органические",
                "description": "Красочный набор томатов черри разных сортов. Выращены традиционными методами для исключительного вкуса и текстуры.",
                "price": 850.0,
                "category": "Овощи и фрукты",
                "subcategory": "Томаты",
                "brand": "Алтын Дала",
                "rating": 4.7,
                "review_count": 423,
                "image_url": "https://images.unsplash.com/photo-1592841200221-a6898f307baa?w=400&auto=format&fit=crop",
                "stock": 200,
                "features": ["Черри", "Без пестицидов", "Без ГМО", "Тепличные"],
                "harvest_date": date(2026, 6, 10),
                "farm_location": "Алматинская область",
                "is_seasonal": True,
                "organic_certified": True,
                "unit_type": "за кг",
                "season": "Лето",
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Говяжий фарш фермерский",
                "description": "Фарш премиум-класса из говядины пастбищного откорма. Нежирный, ароматный, этично выращенный на открытых пастбищах.",
                "price": 3800.0,
                "category": "Мясо и птица",
                "subcategory": "Говядина",
                "brand": "Алтын Дала",
                "rating": 4.8,
                "review_count": 756,
                "image_url": "https://images.unsplash.com/photo-1690983325551-b922137727be?w=400&auto=format&fit=crop",
                "stock": 18,
                "features": ["Пастбищный откорм", "Без гормонов", "Без антибиотиков", "Охлаждённый"],
                "harvest_date": date(2026, 6, 12),
                "farm_location": "Алматинская область",
                "is_seasonal": False,
                "organic_certified": False,
                "unit_type": "за кг",
                "season": "Круглый год",
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Базилик свежий (пучок)",
                "description": "Ароматный свежий базилик, выращенный в питательной почве. Идеален для соусов, салатов и итальянской кухни.",
                "price": 250.0,
                "category": "Сезонные товары",
                "subcategory": "Зелень",
                "brand": "Алтын Дала",
                "rating": 4.6,
                "review_count": 234,
                "image_url": "https://images.unsplash.com/photo-1618375569909-3c8616cf7733?w=400&auto=format&fit=crop",
                "stock": 67,
                "features": ["Свежий", "Ароматный", "Без пестицидов", "Срезан вручную"],
                "harvest_date": date(2026, 6, 17),
                "farm_location": "Алматинская область",
                "is_seasonal": True,
                "organic_certified": True,
                "unit_type": "за пучок",
                "season": "Лето",
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Сыр козий фермерский",
                "description": "Нежный, пикантный козий сыр ручного приготовления малыми партиями. Из молока коз пастбищного содержания.",
                "price": 2200.0,
                "category": "Молочные продукты",
                "subcategory": "Сыр",
                "brand": "Акбота",
                "rating": 4.9,
                "review_count": 445,
                "image_url": "https://images.unsplash.com/photo-1452195100486-9cc805987862?w=400&auto=format&fit=crop",
                "stock": 23,
                "features": ["Фермерский", "Малый тираж", "Пастбищный", "Без консервантов"],
                "harvest_date": date(2026, 6, 14),
                "farm_location": "Акмолинская область",
                "is_seasonal": False,
                "organic_certified": True,
                "unit_type": "за 200г",
                "season": "Круглый год",
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Шпинат молодой",
                "description": "Нежные листья молодого шпината, готовые к употреблению. Идеальны для салатов, смузи и обжаривания.",
                "price": 400.0,
                "category": "Овощи и фрукты",
                "subcategory": "Зелень",
                "brand": "Алтын Дала",
                "rating": 4.5,
                "review_count": 312,
                "image_url": "https://images.unsplash.com/photo-1576045057995-568f588f82fb?w=400&auto=format&fit=crop",
                "stock": 89,
                "features": ["Молодой", "Готов к употреблению", "Органический", "Тепличный"],
                "harvest_date": date(2026, 6, 16),
                "farm_location": "Алматинская область",
                "is_seasonal": False,
                "organic_certified": True,
                "unit_type": "за пучок",
                "season": "Круглый год",
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Лосось дикого улова",
                "description": "Лосось премиум-класса дикого улова. Богат омега-3 жирными кислотами, плотная текстура и нежный вкус.",
                "price": 4500.0,
                "original_price": 5200.0,
                "category": "Мясо и птица",
                "subcategory": "Рыба",
                "brand": "Алтын Дала",
                "rating": 4.9,
                "review_count": 678,
                "image_url": "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=400&auto=format&fit=crop",
                "stock": 12,
                "features": ["Дикий улов", "Экологичный", "Омега-3", "Быстрая заморозка"],
                "is_on_sale": True,
                "sale_percentage": 14,
                "harvest_date": date(2026, 6, 8),
                "farm_location": "Восточно-Казахстанская область",
                "is_seasonal": True,
                "organic_certified": False,
                "unit_type": "за кг",
                "season": "Лето",
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Черника органическая",
                "description": "Крупная, сладкая органическая черника, богатая антиоксидантами. Идеальна для завтрака, выпечки или перекуса.",
                "price": 1200.0,
                "category": "Овощи и фрукты",
                "subcategory": "Ягоды",
                "brand": "Алтын Дала",
                "rating": 4.8,
                "review_count": 534,
                "image_url": "https://images.unsplash.com/photo-1498557850523-fd3d118b962e?w=400&auto=format&fit=crop",
                "stock": 38,
                "features": ["Органическая", "Богата антиоксидантами", "Собрана вручную", "Свежая"],
                "harvest_date": date(2026, 6, 14),
                "farm_location": "Алматинская область",
                "is_seasonal": True,
                "organic_certified": True,
                "unit_type": "за кг",
                "season": "Лето",
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Молоко цельное фермерское",
                "description": "Сливочное цельное молоко от коров пастбищного содержания. Без гомогенизации — с натуральным слоем сливок сверху.",
                "price": 420.0,
                "category": "Молочные продукты",
                "subcategory": "Молоко",
                "brand": "Акбота",
                "rating": 4.7,
                "review_count": 892,
                "image_url": "https://images.pexels.com/photos/248412/pexels-photo-248412.jpeg",
                "stock": 56,
                "features": ["Пастбищное", "Без гомогенизации", "Пастеризованное", "Местное"],
                "harvest_date": date(2026, 6, 18),
                "farm_location": "Акмолинская область",
                "is_seasonal": False,
                "organic_certified": False,
                "unit_type": "за литр",
                "season": "Круглый год",
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Кукуруза сладкая",
                "description": "Свежесобранная сладкая кукуруза с нежными сочными зёрнами. На пике сладости — собрана в идеальный момент.",
                "price": 200.0,
                "category": "Овощи и фрукты",
                "subcategory": "Овощи",
                "brand": "Алтын Дала",
                "rating": 4.6,
                "review_count": 267,
                "image_url": "https://images.unsplash.com/photo-1551754655-cd27e38d2076?w=400&auto=format&fit=crop",
                "stock": 120,
                "features": ["Свежесобранная", "Сладкая", "Без ГМО", "В сезон"],
                "harvest_date": date(2026, 6, 18),
                "farm_location": "Алматинская область",
                "is_seasonal": True,
                "organic_certified": False,
                "unit_type": "за штуку",
                "season": "Лето",
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Курица деревенская целая",
                "description": "Целая курица с пастбищного содержания — на свежем воздухе, с доступом к солнцу. Нежное, ароматное мясо с упругой текстурой.",
                "price": 2500.0,
                "category": "Мясо и птица",
                "subcategory": "Курица",
                "brand": "Жулдыз",
                "rating": 4.8,
                "review_count": 445,
                "image_url": "https://images.unsplash.com/photo-1672787153720-e85fe802fd9f?w=400&auto=format&fit=crop",
                "stock": 15,
                "features": ["Свободный выгул", "Без антибиотиков", "Без гормонов", "Деревенская"],
                "harvest_date": date(2026, 6, 15),
                "farm_location": "Жамбылская область",
                "is_seasonal": False,
                "organic_certified": True,
                "unit_type": "за кг",
                "season": "Круглый год",
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Морковь органическая",
                "description": "Сладкая органическая морковь, богатая бета-каротином. Без химических удобрений, выращена на чистых почвах.",
                "price": 280.0,
                "category": "Овощи и фрукты",
                "subcategory": "Овощи",
                "brand": "Алтын Дала",
                "rating": 4.7,
                "review_count": 623,
                "image_url": "https://images.unsplash.com/photo-1447175008436-054170c2e979?w=400&auto=format&fit=crop",
                "stock": 400,
                "features": ["Органическая", "Сладкая", "Богата бета-каротином", "Без химии"],
                "harvest_date": date(2026, 6, 12),
                "farm_location": "Алматинская область",
                "is_seasonal": False,
                "organic_certified": True,
                "unit_type": "за кг",
                "season": "Круглый год",
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Масло сливочное 82.5%",
                "description": "Настоящее деревенское сливочное масло жирностью 82.5%. Насыщенный сливочный вкус, без растительных жиров и добавок.",
                "price": 1800.0,
                "original_price": 2100.0,
                "category": "Молочные продукты",
                "subcategory": "Масло",
                "brand": "Акбота",
                "rating": 4.9,
                "review_count": 389,
                "image_url": "https://images.unsplash.com/photo-1603596311044-f19158b61f28?w=400&auto=format&fit=crop",
                "stock": 40,
                "features": ["82.5% жирность", "Деревенское", "Без растительных жиров", "ГОСТ"],
                "is_on_sale": True,
                "sale_percentage": 14,
                "harvest_date": date(2026, 5, 15),
                "farm_location": "Акмолинская область",
                "is_seasonal": False,
                "organic_certified": False,
                "unit_type": "за 400г",
                "season": "Круглый год",
            },
        ]