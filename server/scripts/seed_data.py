"""
Seed script — inserts farms, products, and test users into the DB, then indexes
products to Pinecone. All IDs are hardcoded, so the script is idempotent and
safe to run multiple times.

Run inside the server container:
    docker exec -it ecommerce-chatbot-server-1 python scripts/seed_data.py
Or locally:
    cd server && python scripts/seed_data.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from datetime import date

from app import create_app
from models import db
from models.farm import Farm
from models.product import Product
from models.user import User
from services.vector_service import VectorService

# ─────────────────────────────────────────────────────────────────────────────
# Fixed IDs — hardcoded so re-running the script is idempotent
# ─────────────────────────────────────────────────────────────────────────────

_F = lambda n: f"a1000000-0000-0000-0000-{n:012d}"   # farm IDs
_P = lambda n: f"b2000000-0000-0000-0000-{n:012d}"   # product IDs
_U = lambda n: f"c3000000-0000-0000-0000-{n:012d}"   # user IDs

# ─────────────────────────────────────────────────────────────────────────────
# Farms
# ─────────────────────────────────────────────────────────────────────────────

FARMS = [
    {
        "id": _F(1),
        "name": "Ферма Алтын Дала",
        "description": "Семейная ферма в предгорьях Алматы. Органические овощи и фрукты с 1998 года.",
        "location": "Алматинская область",
        "address": "с. Каскелен, Карасайский район",
        "latitude": 43.19,
        "longitude": 76.62,
        "phone": "+7 727 123-45-67",
        "email": "altyndala@farm.kz",
        "website": "https://altyndala.kz",
        "image_url": "https://images.unsplash.com/photo-1500651230702-0e2d8a49d4ad?w=800&auto=format&fit=crop",
        "gallery": [
            "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1466977441628-838349d5e438?w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1523348837708-15d4a09cfac2?w=800&auto=format&fit=crop",
        ],
        "story": (
            "Три поколения семьи Сейткали возделывают эту землю. "
            "Мы применяем капельный полив, только органические удобрения "
            "и компостируем все отходы производства."
        ),
        "practices": ["Органическое земледелие", "Капельный полив", "Компостирование", "Севооборот"],
        "certifications": ["Органик KZ", "GlobalG.A.P."],
        "established_year": 1998,
        "acreage": 120.5,
    },
    {
        "id": _F(2),
        "name": "Молочная ферма Акбота",
        "description": "Современная молочная ферма с собственным стадом голштинских коров. Свежее молоко каждый день.",
        "location": "Акмолинская область",
        "address": "с. Степное, Целиноградский район",
        "latitude": 51.18,
        "longitude": 71.45,
        "phone": "+7 717 234-56-78",
        "email": "akbota@dairy.kz",
        "website": "https://akbota-dairy.kz",
        "image_url": "https://images.unsplash.com/photo-1516467508483-a7212febe31a?w=800&auto=format&fit=crop",
        "gallery": [
            "https://images.unsplash.com/photo-1563805042-7684c019e1cb?w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1572197942069-24d3f3f66b95?w=800&auto=format&fit=crop",
        ],
        "story": (
            "Производим натуральное молоко и молочные продукты без добавок "
            "и консервантов. Коровы пасутся на открытых лугах минимум 8 месяцев в году."
        ),
        "practices": ["Пастбищное содержание", "Без антибиотиков", "Охлаждение за 2 часа"],
        "certifications": ["HACCP", "ISO 22000"],
        "established_year": 2005,
        "acreage": 350.0,
    },
    {
        "id": _F(3),
        "name": "Птицефабрика Жулдыз",
        "description": "Экологически чистое птицеводство. Куры на свободном выгуле, натуральный зерновой корм.",
        "location": "Жамбылская область",
        "address": "г. Тараз, пригород",
        "latitude": 42.90,
        "longitude": 71.37,
        "phone": "+7 726 345-67-89",
        "email": "zhuldyz@poultry.kz",
        "image_url": "https://images.unsplash.com/photo-1548550023-2bdb3c5beed7?w=800&auto=format&fit=crop",
        "gallery": [
            "https://images.unsplash.com/photo-1571748982800-fa51082c2224?w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1612170153139-6f881ff067e0?w=800&auto=format&fit=crop",
        ],
        "story": (
            "Наши куры живут на свежем воздухе круглый год и питаются "
            "зерном без ГМО. Мы не применяем гормоны роста или стимуляторы."
        ),
        "practices": ["Свободный выгул", "Без ГМО", "Натуральный корм", "Без гормонов"],
        "certifications": ["Органик KZ"],
        "established_year": 2010,
        "acreage": 80.0,
    },
    {
        "id": _F(4),
        "name": "Пасека и хозяйство Тау Бар",
        "description": "Горная пасека и производство сухофруктов на высоте 1 200 м. Мёд собирают вручную.",
        "location": "Алматинская область",
        "address": "Каскеленское ущелье, 45 км от Алматы",
        "latitude": 43.05,
        "longitude": 76.48,
        "phone": "+7 701 456-78-90",
        "email": "taubar@honey.kz",
        "image_url": "https://images.unsplash.com/photo-1558642891-54be180ea339?w=800&auto=format&fit=crop",
        "gallery": [
            "https://images.unsplash.com/photo-1587049352846-4a222e784d38?w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1617611647086-3b5daa75dbe3?w=800&auto=format&fit=crop",
        ],
        "story": (
            "Семья Ахметовых содержит 180 ульев высоко в горах. "
            "Пчёлы собирают нектар с дикорастущих трав без удобрений и пестицидов. "
            "Мёд откачивается вручную и не нагревается выше 40°C."
        ),
        "practices": ["Ручной сбор", "Холодная откачка", "Без нагрева", "Дикие луга"],
        "certifications": ["Органик KZ", "EcoKazakhstan"],
        "established_year": 2003,
        "acreage": 40.0,
    },
]

_loc = {f["id"]: f["location"] for f in FARMS}
L1, L2, L3, L4 = _F(1), _F(2), _F(3), _F(4)

# ─────────────────────────────────────────────────────────────────────────────
# Products
# ─────────────────────────────────────────────────────────────────────────────

PRODUCTS = [
    # ── Овощи и фрукты ──────────────────────────────────────────────────────
    {
        "id": _P(1),
        "name": "Томаты черри органические",
        "description": "Сладкие и сочные томаты черри, выращенные без пестицидов в теплицах Алматинской области. Идеальны для салатов и перекусов.",
        "price": 850.0,
        "original_price": 1000.0,
        "category": "Овощи и фрукты",
        "subcategory": "Томаты",
        "brand": "Алтын Дала",
        "rating": 4.8,
        "review_count": 124,
        "image_url": "https://images.unsplash.com/photo-1592841200221-a6898f307baa?w=400&auto=format&fit=crop",
        "stock": 200,
        "features": ["Органические", "Без пестицидов", "Тепличные", "Сочные"],
        "is_on_sale": True,
        "sale_percentage": 15,
        "harvest_date": date(2026, 4, 20),
        "farm_location": _loc[L1],
        "is_seasonal": False,
        "organic_certified": True,
        "unit_type": "за кг",
        "season": "Круглый год",
    },
    {
        "id": _P(2),
        "name": "Огурцы свежие грядочные",
        "description": "Хрустящие огурцы прямо с грядки. Идеальны для салатов и домашней засолки. Собраны утром.",
        "price": 450.0,
        "original_price": None,
        "category": "Овощи и фрукты",
        "subcategory": "Огурцы",
        "brand": "Алтын Дала",
        "rating": 4.6,
        "review_count": 89,
        "image_url": "https://images.unsplash.com/photo-1568584711271-6c929fb49b60?w=400&auto=format&fit=crop",
        "stock": 300,
        "features": ["Свежие", "Хрустящие", "Без ГМО", "Грядочные"],
        "is_on_sale": False,
        "harvest_date": date(2026, 4, 21),
        "farm_location": _loc[L1],
        "is_seasonal": True,
        "organic_certified": True,
        "unit_type": "за кг",
        "season": "Лето",
    },
    {
        "id": _P(3),
        "name": "Яблоки Апорт алматинский",
        "description": "Знаменитые алматинские яблоки сорта Апорт. Крупные, ароматные, с насыщенным вкусом. Бренд Казахстана.",
        "price": 700.0,
        "original_price": None,
        "category": "Овощи и фрукты",
        "subcategory": "Яблоки",
        "brand": "Алтын Дала",
        "rating": 4.9,
        "review_count": 210,
        "image_url": "https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=400&auto=format&fit=crop",
        "stock": 500,
        "features": ["Сорт Апорт", "Крупные", "Ароматные", "Местный сорт"],
        "is_on_sale": False,
        "harvest_date": date(2025, 9, 15),
        "farm_location": _loc[L1],
        "is_seasonal": True,
        "organic_certified": True,
        "unit_type": "за кг",
        "season": "Осень",
    },
    {
        "id": _P(4),
        "name": "Картофель молодой",
        "description": "Молодой картофель с нежной кожицей и рассыпчатой мякотью. Без нитратов, выращен на чистых почвах.",
        "price": 300.0,
        "original_price": None,
        "category": "Овощи и фрукты",
        "subcategory": "Картофель",
        "brand": "Алтын Дала",
        "rating": 4.5,
        "review_count": 67,
        "image_url": "https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=400&auto=format&fit=crop",
        "stock": 1000,
        "features": ["Молодой", "Без нитратов", "Рассыпчатый", "Фермерский"],
        "is_on_sale": False,
        "harvest_date": date(2026, 4, 18),
        "farm_location": _loc[L1],
        "is_seasonal": True,
        "organic_certified": False,
        "unit_type": "за кг",
        "season": "Лето",
    },
    {
        "id": _P(5),
        "name": "Морковь органическая",
        "description": "Сладкая органическая морковь, богатая бета-каротином. Выращена на чистых почвах без химических удобрений.",
        "price": 280.0,
        "original_price": None,
        "category": "Овощи и фрукты",
        "subcategory": "Морковь",
        "brand": "Алтын Дала",
        "rating": 4.7,
        "review_count": 95,
        "image_url": "https://images.unsplash.com/photo-1447175008436-054170c2e979?w=400&auto=format&fit=crop",
        "stock": 400,
        "features": ["Органическая", "Сладкая", "Богата бета-каротином", "Без химии"],
        "is_on_sale": False,
        "harvest_date": date(2026, 4, 10),
        "farm_location": _loc[L1],
        "is_seasonal": False,
        "organic_certified": True,
        "unit_type": "за кг",
        "season": "Круглый год",
    },
    {
        "id": _P(6),
        "name": "Клубника свежая",
        "description": "Ароматная клубника прямо с грядки — сладкая, крупная, без химикатов. Ограниченный сезонный продукт.",
        "price": 1500.0,
        "original_price": 1800.0,
        "category": "Овощи и фрукты",
        "subcategory": "Ягоды",
        "brand": "Алтын Дала",
        "rating": 4.9,
        "review_count": 312,
        "image_url": "https://images.unsplash.com/photo-1464965911861-746a04b4bca6?w=400&auto=format&fit=crop",
        "stock": 150,
        "features": ["Свежая", "Сладкая", "Без химикатов", "Сезонная"],
        "is_on_sale": True,
        "sale_percentage": 17,
        "harvest_date": date(2026, 4, 22),
        "farm_location": _loc[L1],
        "is_seasonal": True,
        "organic_certified": True,
        "unit_type": "за кг",
        "season": "Лето",
    },
    {
        "id": _P(7),
        "name": "Перец болгарский (микс)",
        "description": "Сочный сладкий перец трёх цветов — красный, жёлтый, зелёный. Богат витамином C, без нитратов.",
        "price": 650.0,
        "original_price": None,
        "category": "Овощи и фрукты",
        "subcategory": "Перец",
        "brand": "Алтын Дала",
        "rating": 4.6,
        "review_count": 58,
        "image_url": "https://images.unsplash.com/photo-1605800854006-85faa6220714?w=400&auto=format&fit=crop",
        "stock": 180,
        "features": ["Три вида", "Сочный", "Без нитратов", "Витамин C"],
        "is_on_sale": False,
        "harvest_date": date(2026, 4, 19),
        "farm_location": _loc[L1],
        "is_seasonal": True,
        "organic_certified": False,
        "unit_type": "за кг",
        "season": "Лето",
    },
    {
        "id": _P(8),
        "name": "Тыква столовая",
        "description": "Сладкая тыква сорта Хоккайдо. Нежная мякоть, подходит для супа, каши и выпечки.",
        "price": 350.0,
        "original_price": None,
        "category": "Овощи и фрукты",
        "subcategory": "Тыква",
        "brand": "Алтын Дала",
        "rating": 4.5,
        "review_count": 44,
        "image_url": "https://images.unsplash.com/photo-1570586437263-ab629fccc818?w=400&auto=format&fit=crop",
        "stock": 90,
        "features": ["Сорт Хоккайдо", "Сладкая мякоть", "Для выпечки", "Долго хранится"],
        "is_on_sale": False,
        "harvest_date": date(2025, 10, 5),
        "farm_location": _loc[L1],
        "is_seasonal": True,
        "organic_certified": False,
        "unit_type": "за кг",
        "season": "Осень",
    },
    # ── Молочные продукты ────────────────────────────────────────────────────
    {
        "id": _P(9),
        "name": "Молоко цельное 3.5%",
        "description": "Свежее цельное молоко от пастбищных коров голштинской породы. Жирность 3.5%, без добавок и гомогенизации.",
        "price": 420.0,
        "original_price": None,
        "category": "Молочные продукты",
        "subcategory": "Молоко",
        "brand": "Акбота",
        "rating": 4.7,
        "review_count": 188,
        "image_url": "https://images.unsplash.com/photo-1550583724-b2692b85b150?w=400&auto=format&fit=crop",
        "stock": 80,
        "features": ["Цельное", "3.5% жирность", "Без добавок", "Пастбищное"],
        "is_on_sale": False,
        "harvest_date": date(2026, 4, 22),
        "farm_location": _loc[L2],
        "is_seasonal": False,
        "organic_certified": False,
        "unit_type": "за литр",
        "season": "Круглый год",
    },
    {
        "id": _P(10),
        "name": "Творог домашний 9%",
        "description": "Натуральный домашний творог из цельного молока. Нежный, без кислинки, богат белком и кальцием.",
        "price": 1200.0,
        "original_price": None,
        "category": "Молочные продукты",
        "subcategory": "Творог",
        "brand": "Акбота",
        "rating": 4.8,
        "review_count": 145,
        "image_url": "https://images.unsplash.com/photo-1573810655264-8d1e50f1592d?w=400&auto=format&fit=crop",
        "stock": 50,
        "features": ["9% жирность", "Без консервантов", "Богат белком", "Домашний"],
        "is_on_sale": False,
        "harvest_date": date(2026, 4, 21),
        "farm_location": _loc[L2],
        "is_seasonal": False,
        "organic_certified": False,
        "unit_type": "за кг",
        "season": "Круглый год",
    },
    {
        "id": _P(11),
        "name": "Сметана 20%",
        "description": "Густая сметана из натуральных сливок. Идеальна для заправки борща и приготовления соусов.",
        "price": 650.0,
        "original_price": None,
        "category": "Молочные продукты",
        "subcategory": "Сметана",
        "brand": "Акбота",
        "rating": 4.6,
        "review_count": 102,
        "image_url": "https://images.unsplash.com/photo-1563636619-e9143da7973b?w=400&auto=format&fit=crop",
        "stock": 60,
        "features": ["20% жирность", "Густая", "Натуральные сливки", "Без загустителей"],
        "is_on_sale": False,
        "harvest_date": date(2026, 4, 20),
        "farm_location": _loc[L2],
        "is_seasonal": False,
        "organic_certified": False,
        "unit_type": "за 500г",
        "season": "Круглый год",
    },
    {
        "id": _P(12),
        "name": "Кефир натуральный 2.5%",
        "description": "Живой кефир с активными пробиотическими культурами. Полезен для пищеварения, без искусственных добавок.",
        "price": 380.0,
        "original_price": None,
        "category": "Молочные продукты",
        "subcategory": "Кефир",
        "brand": "Акбота",
        "rating": 4.5,
        "review_count": 78,
        "image_url": "https://images.unsplash.com/photo-1581868164904-77b124b80242?w=400&auto=format&fit=crop",
        "stock": 90,
        "features": ["Живые культуры", "Пробиотики", "2.5% жирность", "Без добавок"],
        "is_on_sale": False,
        "harvest_date": date(2026, 4, 22),
        "farm_location": _loc[L2],
        "is_seasonal": False,
        "organic_certified": False,
        "unit_type": "за литр",
        "season": "Круглый год",
    },
    {
        "id": _P(13),
        "name": "Масло сливочное 82.5%",
        "description": "Настоящее деревенское сливочное масло. Жирность 82.5%, насыщенный сливочный вкус, без растительных жиров.",
        "price": 1800.0,
        "original_price": 2100.0,
        "category": "Молочные продукты",
        "subcategory": "Масло",
        "brand": "Акбота",
        "rating": 4.9,
        "review_count": 230,
        "image_url": "https://images.unsplash.com/photo-1603596311044-f19158b61f28?w=400&auto=format&fit=crop",
        "stock": 40,
        "features": ["82.5% жирность", "Деревенское", "Без растительных жиров", "ГОСТ"],
        "is_on_sale": True,
        "sale_percentage": 14,
        "harvest_date": date(2026, 4, 19),
        "farm_location": _loc[L2],
        "is_seasonal": False,
        "organic_certified": False,
        "unit_type": "за 400г",
        "season": "Круглый год",
    },
    # ── Мясо и птица ─────────────────────────────────────────────────────────
    {
        "id": _P(14),
        "name": "Курица деревенская целая",
        "description": "Домашняя курица свободного выгула. Натуральный зерновой корм, никаких гормонов роста.",
        "price": 2500.0,
        "original_price": None,
        "category": "Мясо и птица",
        "subcategory": "Курица",
        "brand": "Жулдыз",
        "rating": 4.8,
        "review_count": 156,
        "image_url": "https://images.unsplash.com/photo-1672787153720-e85fe802fd9f?w=400&auto=format&fit=crop",
        "stock": 30,
        "features": ["Свободный выгул", "Без гормонов", "Натуральный корм", "Деревенская"],
        "is_on_sale": False,
        "harvest_date": date(2026, 4, 21),
        "farm_location": _loc[L3],
        "is_seasonal": False,
        "organic_certified": True,
        "unit_type": "за кг",
        "season": "Круглый год",
    },
    {
        "id": _P(15),
        "name": "Яйца куриные домашние (10 шт)",
        "description": "Яйца от кур свободного выгула с ярким оранжевым желтком. Богаты витамином D и омега-3.",
        "price": 900.0,
        "original_price": None,
        "category": "Мясо и птица",
        "subcategory": "Яйца",
        "brand": "Жулдыз",
        "rating": 4.9,
        "review_count": 420,
        "image_url": "https://images.unsplash.com/photo-1582722872445-44dc5f7e3c8f?w=400&auto=format&fit=crop",
        "stock": 200,
        "features": ["Свободный выгул", "Яркий желток", "Омега-3", "Без ГМО"],
        "is_on_sale": False,
        "harvest_date": date(2026, 4, 22),
        "farm_location": _loc[L3],
        "is_seasonal": False,
        "organic_certified": True,
        "unit_type": "10 штук",
        "season": "Круглый год",
    },
    {
        "id": _P(16),
        "name": "Баранина молодая (корейка)",
        "description": "Нежная корейка молодого барашка. Без запаха, мясо светлое, быстро готовится — идеально для барбекю.",
        "price": 4500.0,
        "original_price": 5000.0,
        "category": "Мясо и птица",
        "subcategory": "Баранина",
        "brand": "Алтын Дала",
        "rating": 4.7,
        "review_count": 88,
        "image_url": "https://images.unsplash.com/photo-1529692236671-f1f6cf9683ba?w=400&auto=format&fit=crop",
        "stock": 20,
        "features": ["Молодой барашек", "Без запаха", "Нежное мясо", "Охлаждённое"],
        "is_on_sale": True,
        "sale_percentage": 10,
        "harvest_date": date(2026, 4, 20),
        "farm_location": _loc[L1],
        "is_seasonal": False,
        "organic_certified": False,
        "unit_type": "за кг",
        "season": "Круглый год",
    },
    {
        "id": _P(17),
        "name": "Говядина фермерская (вырезка)",
        "description": "Охлаждённая говяжья вырезка от бычков на пастбищном откорме. Нежное мясо, богато железом.",
        "price": 3800.0,
        "original_price": None,
        "category": "Мясо и птица",
        "subcategory": "Говядина",
        "brand": "Алтын Дала",
        "rating": 4.6,
        "review_count": 62,
        "image_url": "https://images.unsplash.com/photo-1690983325551-b922137727be?w=400&auto=format&fit=crop",
        "stock": 15,
        "features": ["Вырезка", "Пастбищный откорм", "Охлаждённая", "Богата железом"],
        "is_on_sale": False,
        "harvest_date": date(2026, 4, 19),
        "farm_location": _loc[L1],
        "is_seasonal": False,
        "organic_certified": False,
        "unit_type": "за кг",
        "season": "Круглый год",
    },
    # ── Сезонные товары ───────────────────────────────────────────────────────
    {
        "id": _P(18),
        "name": "Спаржа зелёная (пучок)",
        "description": "Нежная весенняя спаржа — срезана утром того же дня. Богата фолиевой кислотой и антиоксидантами.",
        "price": 1200.0,
        "original_price": None,
        "category": "Сезонные товары",
        "subcategory": "Зелень",
        "brand": "Алтын Дала",
        "rating": 4.6,
        "review_count": 33,
        "image_url": "https://images.unsplash.com/photo-1604977042946-1eecc30f269e?w=400&auto=format&fit=crop",
        "stock": 40,
        "features": ["Сезонная", "Свежесрезанная", "Богата фолиевой кислотой", "Весенняя"],
        "is_on_sale": False,
        "harvest_date": date(2026, 4, 22),
        "farm_location": _loc[L1],
        "is_seasonal": True,
        "organic_certified": True,
        "unit_type": "за пучок",
        "season": "Весна",
    },
    {
        "id": _P(19),
        "name": "Редис ранний (пучок)",
        "description": "Хрустящий ранний редис — первый урожай сезона. Острый, сочный, в пучке около 300г.",
        "price": 250.0,
        "original_price": None,
        "category": "Сезонные товары",
        "subcategory": "Зелень",
        "brand": "Алтын Дала",
        "rating": 4.4,
        "review_count": 41,
        "image_url": "https://images.unsplash.com/photo-1585670671903-e8242a404b88?w=400&auto=format&fit=crop",
        "stock": 120,
        "features": ["Ранний урожай", "Хрустящий", "Сезонный", "Свежий"],
        "is_on_sale": False,
        "harvest_date": date(2026, 4, 22),
        "farm_location": _loc[L1],
        "is_seasonal": True,
        "organic_certified": False,
        "unit_type": "за пучок",
        "season": "Весна",
    },
    {
        "id": _P(20),
        "name": "Зелень свежая (укроп + петрушка)",
        "description": "Ароматный укроп и петрушка в одном наборе. Срезаны утром, хранятся в холодильнике до 5 дней.",
        "price": 200.0,
        "original_price": None,
        "category": "Сезонные товары",
        "subcategory": "Зелень",
        "brand": "Алтын Дала",
        "rating": 4.7,
        "review_count": 77,
        "image_url": "https://images.unsplash.com/photo-1570910015265-5da158c809e2?w=400&auto=format&fit=crop",
        "stock": 200,
        "features": ["Укроп", "Петрушка", "Свежесрезанная", "Ароматная"],
        "is_on_sale": False,
        "harvest_date": date(2026, 4, 22),
        "farm_location": _loc[L1],
        "is_seasonal": True,
        "organic_certified": True,
        "unit_type": "за набор",
        "season": "Весна",
    },
    {
        "id": _P(21),
        "name": "Черемша (дикий чеснок)",
        "description": "Дикорастущая черемша с гор — весенний деликатес. Богата фитонцидами, улучшает иммунитет.",
        "price": 600.0,
        "original_price": None,
        "category": "Сезонные товары",
        "subcategory": "Дикоросы",
        "brand": "Тау Бар",
        "rating": 4.8,
        "review_count": 29,
        "image_url": "https://images.unsplash.com/photo-1627899045097-e478157bb638?w=400&auto=format&fit=crop",
        "stock": 50,
        "features": ["Дикорастущая", "Горная", "Фитонциды", "Сезонная"],
        "is_on_sale": False,
        "harvest_date": date(2026, 4, 15),
        "farm_location": _loc[L4],
        "is_seasonal": True,
        "organic_certified": True,
        "unit_type": "за пучок",
        "season": "Весна",
    },
    # ── Мёд и сухофрукты ─────────────────────────────────────────────────────
    {
        "id": _P(22),
        "name": "Мёд цветочный весенний",
        "description": "Свежий весенний мёд с горных лугов — собран в апреле 2026. Откачан вручную без нагрева.",
        "price": 3500.0,
        "original_price": None,
        "category": "Мёд и сухофрукты",
        "subcategory": "Мёд",
        "brand": "Тау Бар",
        "rating": 5.0,
        "review_count": 64,
        "image_url": "https://images.unsplash.com/photo-1587049352846-4a222e784d38?w=400&auto=format&fit=crop",
        "stock": 25,
        "features": ["Натуральный", "Горный", "Весенний", "Без нагрева"],
        "is_on_sale": False,
        "harvest_date": date(2026, 4, 10),
        "farm_location": _loc[L4],
        "is_seasonal": True,
        "organic_certified": True,
        "unit_type": "за кг",
        "season": "Весна",
    },
    {
        "id": _P(23),
        "name": "Мёд гречишный тёмный",
        "description": "Насыщенный тёмный мёд с гречишных полей. Богат железом и антиоксидантами, помогает при анемии.",
        "price": 3200.0,
        "original_price": 3800.0,
        "category": "Мёд и сухофрукты",
        "subcategory": "Мёд",
        "brand": "Тау Бар",
        "rating": 4.8,
        "review_count": 48,
        "image_url": "https://images.unsplash.com/photo-1676313779351-9648c6eaae8a?w=400&auto=format&fit=crop",
        "stock": 18,
        "features": ["Гречишный", "Тёмный", "Богат железом", "Антиоксиданты"],
        "is_on_sale": True,
        "sale_percentage": 16,
        "harvest_date": date(2025, 8, 20),
        "farm_location": _loc[L4],
        "is_seasonal": True,
        "organic_certified": True,
        "unit_type": "за кг",
        "season": "Лето",
    },
    {
        "id": _P(24),
        "name": "Курага натуральная (без серы)",
        "description": "Сушёные абрикосы без обработки серой — тёмные, с насыщенным вкусом. Богаты калием и каротином.",
        "price": 1800.0,
        "original_price": None,
        "category": "Мёд и сухофрукты",
        "subcategory": "Сухофрукты",
        "brand": "Тау Бар",
        "rating": 4.7,
        "review_count": 55,
        "image_url": "https://images.unsplash.com/photo-1610401882421-f05386f4dfc5?w=400&auto=format&fit=crop",
        "stock": 70,
        "features": ["Без серы", "Натуральная", "Богата калием", "Без сахара"],
        "is_on_sale": False,
        "harvest_date": date(2025, 7, 15),
        "farm_location": _loc[L4],
        "is_seasonal": True,
        "organic_certified": True,
        "unit_type": "за кг",
        "season": "Лето",
    },
    {
        "id": _P(25),
        "name": "Грецкий орех фермерский",
        "description": "Свежий грецкий орех нового урожая из Алматинской области. Легко колется, ядро светлое, без горечи.",
        "price": 2500.0,
        "original_price": None,
        "category": "Мёд и сухофрукты",
        "subcategory": "Орехи",
        "brand": "Тау Бар",
        "rating": 4.6,
        "review_count": 37,
        "image_url": "https://images.unsplash.com/photo-1524593000379-d4729b2c4f99?w=400&auto=format&fit=crop",
        "stock": 80,
        "features": ["Новый урожай", "Лёгкий скол", "Без горечи", "Местный"],
        "is_on_sale": False,
        "harvest_date": date(2025, 10, 1),
        "farm_location": _loc[L4],
        "is_seasonal": True,
        "organic_certified": False,
        "unit_type": "за кг",
        "season": "Осень",
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# Test users
# ─────────────────────────────────────────────────────────────────────────────

USERS = [
    {
        "id": _U(1),
        "email": "demo@farm.kz",
        "name": "Айгерим Сейткали",
        "password": "Demo1234!",
        "preferences": {
            "favoriteCategories": ["Овощи и фрукты", "Сезонные товары"],
            "priceRange": [0, 2000],
            "favoriteBrands": ["Алтын Дала"],
        },
    },
    {
        "id": _U(2),
        "email": "aizhan@farm.kz",
        "name": "Айжан Қасымова",
        "password": "Test1234!",
        "preferences": {
            "favoriteCategories": ["Молочные продукты", "Мёд и сухофрукты"],
            "priceRange": [0, 5000],
            "favoriteBrands": ["Акбота", "Тау Бар"],
        },
    },
    {
        "id": _U(3),
        "email": "bekzat@farm.kz",
        "name": "Бекзат Жумабеков",
        "password": "Test1234!",
        "preferences": {
            "favoriteCategories": ["Мясо и птица", "Сезонные товары"],
            "priceRange": [500, 10000],
            "favoriteBrands": ["Жулдыз", "Алтын Дала"],
        },
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# Seeding logic
# ─────────────────────────────────────────────────────────────────────────────

def seed_farms(session):
    count = 0
    for data in FARMS:
        if session.get(Farm, data["id"]):
            print(f"  [skip] Ферма: {data['name']}")
            continue
        session.add(Farm(**data))
        count += 1
        print(f"  [+] Ферма: {data['name']}")
    return count


def seed_products(session):
    count = 0
    for data in PRODUCTS:
        if session.get(Product, data["id"]):
            print(f"  [skip] Товар: {data['name']}")
            continue
        session.add(Product(**data))
        count += 1
        print(f"  [+] Товар: {data['name']}")
    return count


def seed_users(session):
    count = 0
    for data in USERS:
        if session.get(User, data["id"]):
            print(f"  [skip] Пользователь: {data['email']}")
            continue
        user = User(id=data["id"], email=data["email"], name=data["name"], password=data["password"])
        user.set_preferences(data["preferences"])
        session.add(user)
        count += 1
        print(f"  [+] Пользователь: {data['email']}  пароль: {data['password']}")
    return count


def index_to_pinecone():
    print("\n--- Индексация товаров в Pinecone ---")
    vector_service = VectorService()
    try:
        vector_service.initialize()
    except Exception as e:
        print(f"  [!] Pinecone init failed: {e}")
        print("  [!] Пропускаем индексацию. Запустите scripts/index_all_products.py позже.")
        return

    products = Product.query.filter_by(is_active=True).all()
    product_dicts = [
        {
            "id": p.id,
            "text": p.get_search_text(),
            "metadata": {
                "category": p.category,
                "subcategory": p.subcategory,
                "brand": p.brand,
                "price": p.price,
                "rating": p.rating,
                "in_stock": p.is_in_stock(),
            },
        }
        for p in products
    ]

    if product_dicts:
        vector_service.batch_upsert_products(product_dicts)
        print(f"  [+] Проиндексировано {len(product_dicts)} товаров.")
    else:
        print("  [!] Товаров не найдено.")


def main():
    print("=== Запуск сидирования ===\n")
    app = create_app()
    with app.app_context():
        db.create_all()

        print("--- Фермы ---")
        farm_count = seed_farms(db.session)

        print("\n--- Товары ---")
        product_count = seed_products(db.session)

        print("\n--- Пользователи ---")
        user_count = seed_users(db.session)

        db.session.commit()
        print(
            f"\n--- Сохранено: {farm_count} ферм, "
            f"{product_count} товаров, {user_count} пользователей ---"
        )

        index_to_pinecone()

    print("\n=== Сидирование завершено ===")


if __name__ == "__main__":
    main()
