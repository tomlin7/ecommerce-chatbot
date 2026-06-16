import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models import db, Product
from services.vector_service import VectorService


def main():
    app = create_app()
    with app.app_context():
        vector_service = VectorService()
        vector_service.initialize()

        products = Product.query.filter_by(is_active=True).all()
        print(f"Found {len(products)} products to index...")

        product_dicts = []
        for product in products:
            product_dicts.append(
                {
                    "id": product.id,
                    "text": product.get_search_text(),
                    "metadata": {
                        "category": product.category,
                        "subcategory": product.subcategory,
                        "brand": product.brand,
                        "price": product.price,
                        "rating": product.rating,
                        "in_stock": product.is_in_stock(),
                    },
                }
            )

        if product_dicts:
            vector_service.batch_upsert_products(product_dicts)
            print("All products indexed to Pinecone.")
        else:
            print("No products found to index.")


if __name__ == "__main__":
    main()
