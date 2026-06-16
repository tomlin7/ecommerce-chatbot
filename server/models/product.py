import json
from datetime import datetime, date

from models import db


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(200), nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False, index=True)
    original_price = db.Column(db.Float)
    category = db.Column(db.String(100), nullable=False, index=True)
    subcategory = db.Column(db.String(100), nullable=False, index=True)
    brand = db.Column(db.String(100), nullable=False, index=True)
    rating = db.Column(db.Float, default=0.0, index=True)
    review_count = db.Column(db.Integer, default=0)
    image_url = db.Column(db.String(500))
    stock = db.Column(db.Integer, default=0, index=True)
    features = db.Column(db.Text)
    is_on_sale = db.Column(db.Boolean, default=False, index=True)
    sale_percentage = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(
        db.DateTime, default=datetime.now(), onupdate=datetime.now()
    )
    is_active = db.Column(db.Boolean, default=True, index=True)

    embedding_id = db.Column(db.String(100))

    # Farm-specific fields
    harvest_date = db.Column(db.Date)
    farm_location = db.Column(db.String(200))
    is_seasonal = db.Column(db.Boolean, default=False, index=True)
    organic_certified = db.Column(db.Boolean, default=False, index=True)
    unit_type = db.Column(db.String(50))  # e.g., "per pound", "per dozen", "per bunch"
    season = db.Column(db.String(50))  # e.g., "Spring", "Summer", "Fall", "Winter"

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key == "features" and isinstance(value, list):
                setattr(self, key, json.dumps(value))
            else:
                setattr(self, key, value)

    def get_features(self):
        """Get features as list"""
        try:
            return json.loads(self.features) if self.features else []
        except json.JSONDecodeError:
            return []

    def set_features(self, features_list):
        """Set features from list"""
        self.features = json.dumps(features_list)
        self.updated_at = datetime.utcnow()

    def get_search_text(self):
        """Get combined text for embedding generation"""
        features_text = " ".join(self.get_features())
        return f"{self.name} {self.description} {self.brand} {self.category} {self.subcategory} {features_text}"

    def calculate_discount(self):
        """Calculate discount percentage"""
        if self.original_price and self.original_price > self.price:
            return round(
                ((self.original_price - self.price) / self.original_price) * 100
            )
        return 0

    def is_in_stock(self):
        """Check if product is in stock"""
        return self.stock > 0

    def to_dict(self, include_embedding=False):
        """Convert product to dictionary"""
        data = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "originalPrice": self.original_price,
            "category": self.category,
            "subcategory": self.subcategory,
            "brand": self.brand,
            "rating": self.rating,
            "reviewCount": self.review_count,
            "imageUrl": self.image_url,
            "stock": self.stock,
            "features": self.get_features(),
            "isOnSale": self.is_on_sale,
            "salePercentage": self.sale_percentage or self.calculate_discount(),
            "createdAt": self.created_at.isoformat(),
            "updatedAt": self.updated_at.isoformat(),
            "isActive": self.is_active,
            "inStock": self.is_in_stock(),
            # Farm-specific fields
            "harvestDate": self.harvest_date.isoformat() if self.harvest_date else None,
            "farmLocation": self.farm_location,
            "isSeasonal": self.is_seasonal,
            "organicCertified": self.organic_certified,
            "unitType": self.unit_type,
            "season": self.season,
        }

        if include_embedding:
            data["embeddingId"] = self.embedding_id

        return data

    @staticmethod
    def search_by_filters(
        category=None,
        subcategory=None,
        brand=None,
        min_price=None,
        max_price=None,
        min_rating=None,
        in_stock_only=False,
        search_query=None,
        limit=50,
    ):
        """Search products with filters"""
        query = Product.query.filter(Product.is_active == True)

        if category:
            query = query.filter(Product.category.ilike(f"%{category}%"))

        if subcategory:
            query = query.filter(Product.subcategory.ilike(f"%{subcategory}%"))

        if brand:
            query = query.filter(Product.brand.ilike(f"%{brand}%"))

        if min_price is not None:
            query = query.filter(Product.price >= min_price)

        if max_price is not None:
            query = query.filter(Product.price <= max_price)

        if min_rating is not None:
            query = query.filter(Product.rating >= min_rating)

        if in_stock_only:
            query = query.filter(Product.stock > 0)

        if search_query:
            search_term = f"%{search_query}%"
            query = query.filter(
                db.or_(
                    Product.name.ilike(search_term),
                    Product.description.ilike(search_term),
                    Product.brand.ilike(search_term),
                    Product.features.ilike(search_term),
                )
            )

        return query.order_by(Product.rating.desc()).limit(limit).all()

    def __repr__(self):
        return f"<Product {self.name}>"
