import json
import uuid

from flask import Blueprint, jsonify, request
from models import db, Farm, Product
from datetime import datetime

farm_bp = Blueprint("farms", __name__)


@farm_bp.route("/", methods=["GET"])
def get_farms():
    """Get all farms with optional filters"""
    try:
        # Get filter parameters
        location = request.args.get("location")
        certified = request.args.get("certified")
        limit = request.args.get("limit", 50, type=int)

        query = Farm.query.filter(Farm.is_active == True)

        if location:
            query = query.filter(Farm.location.ilike(f"%{location}%"))

        if certified:
            # Filter farms that have the specified certification
            farms = query.all()
            certified_farms = [
                farm
                for farm in farms
                if certified.lower()
                in [c.lower() for c in farm.get_certifications()]
            ]
            return (
                jsonify(
                    {
                        "success": True,
                        "farms": [farm.to_dict() for farm in certified_farms],
                        "count": len(certified_farms),
                    }
                ),
                200,
            )

        farms = query.order_by(Farm.name).limit(limit).all()

        return (
            jsonify(
                {"success": True, "farms": [farm.to_dict() for farm in farms], "count": len(farms)}
            ),
            200,
        )

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@farm_bp.route("/<farm_id>", methods=["GET"])
def get_farm(farm_id):
    """Get a specific farm by ID"""
    try:
        farm = Farm.query.get(farm_id)

        if not farm:
            return (
                jsonify({"success": False, "error": "Farm not found"}),
                404,
            )

        # Get products from this farm
        products = Product.query.filter(
            Product.brand.ilike(f"%{farm.name}%"),
            Product.is_active == True,
        ).all()

        farm_data = farm.to_dict()
        farm_data["products"] = [product.to_dict() for product in products]

        return jsonify({"success": True, "farm": farm_data}), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@farm_bp.route("/", methods=["POST"])
def create_farm():
    """Create a new farm"""
    try:
        data = request.get_json()

        required_fields = ["name", "location"]
        for field in required_fields:
            if field not in data:
                return (
                    jsonify({"success": False, "error": f"Missing required field: {field}"}),
                    400,
                )

        farm = Farm(
            id=data.get("id", str(uuid.uuid4())),
            name=data["name"],
            description=data.get("description"),
            location=data["location"],
            address=data.get("address"),
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
            phone=data.get("phone"),
            email=data.get("email"),
            website=data.get("website"),
            image_url=data.get("image_url"),
            story=data.get("story"),
            established_year=data.get("established_year"),
            acreage=data.get("acreage"),
        )

        db.session.add(farm)
        db.session.commit()

        return jsonify({"success": True, "farm": farm.to_dict()}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500


@farm_bp.route("/<farm_id>", methods=["PUT"])
def update_farm(farm_id):
    """Update an existing farm"""
    try:
        farm = Farm.query.get(farm_id)

        if not farm:
            return (
                jsonify({"success": False, "error": "Farm not found"}),
                404,
            )

        data = request.get_json()

        # Update fields
        updatable_fields = [
            "name",
            "description",
            "location",
            "address",
            "latitude",
            "longitude",
            "phone",
            "email",
            "website",
            "image_url",
            "story",
            "established_year",
            "acreage",
        ]

        for field in updatable_fields:
            if field in data:
                setattr(farm, field, data[field])

        # Handle list fields
        if "gallery" in data and isinstance(data["gallery"], list):
            farm.gallery = json.dumps(data["gallery"])
        if "practices" in data and isinstance(data["practices"], list):
            farm.practices = json.dumps(data["practices"])
        if "certifications" in data and isinstance(data["certifications"], list):
            farm.certifications = json.dumps(data["certifications"])

        farm.updated_at = datetime.now()

        db.session.commit()

        return jsonify({"success": True, "farm": farm.to_dict()}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500


@farm_bp.route("/<farm_id>", methods=["DELETE"])
def delete_farm(farm_id):
    """Soft delete a farm"""
    try:
        farm = Farm.query.get(farm_id)

        if not farm:
            return (
                jsonify({"success": False, "error": "Farm not found"}),
                404,
            )

        farm.is_active = False
        farm.updated_at = datetime.now()
        db.session.commit()

        return jsonify({"success": True, "message": "Farm deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500


@farm_bp.route("/<farm_id>/products", methods=["GET"])
def get_farm_products(farm_id):
    """Get all products from a specific farm"""
    try:
        farm = Farm.query.get(farm_id)

        if not farm:
            return (
                jsonify({"success": False, "error": "Farm not found"}),
                404,
            )

        # Get products from this farm
        products = Product.query.filter(
            Product.brand.ilike(f"%{farm.name}%"),
            Product.is_active == True,
        ).all()

        return (
            jsonify(
                {
                    "success": True,
                    "products": [product.to_dict() for product in products],
                    "count": len(products),
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500