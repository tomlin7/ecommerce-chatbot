import json
from datetime import datetime

from models import db


class Farm(db.Model):
    __tablename__ = "farms"

    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(200), nullable=False, index=True)
    description = db.Column(db.Text)
    location = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(300))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    website = db.Column(db.String(300))
    image_url = db.Column(db.String(500))
    gallery = db.Column(db.Text)  # JSON array of image URLs
    story = db.Column(db.Text)  # Farm story/history
    practices = db.Column(db.Text)  # JSON array of farming practices
    certifications = db.Column(db.Text)  # JSON array of certifications
    established_year = db.Column(db.Integer)
    acreage = db.Column(db.Float)  # Farm size in acres
    is_active = db.Column(db.Boolean, default=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(
        db.DateTime, default=datetime.now(), onupdate=datetime.now()
    )

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key in ["gallery", "practices", "certifications"] and isinstance(
                value, list
            ):
                setattr(self, key, json.dumps(value))
            else:
                setattr(self, key, value)

    def get_gallery(self):
        """Get gallery as list"""
        try:
            return json.loads(self.gallery) if self.gallery else []
        except json.JSONDecodeError:
            return []

    def get_practices(self):
        """Get practices as list"""
        try:
            return json.loads(self.practices) if self.practices else []
        except json.JSONDecodeError:
            return []

    def get_certifications(self):
        """Get certifications as list"""
        try:
            return json.loads(self.certifications) if self.certifications else []
        except json.JSONDecodeError:
            return []

    def to_dict(self):
        """Convert farm to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "location": self.location,
            "address": self.address,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "phone": self.phone,
            "email": self.email,
            "website": self.website,
            "imageUrl": self.image_url,
            "gallery": self.get_gallery(),
            "story": self.story,
            "practices": self.get_practices(),
            "certifications": self.get_certifications(),
            "establishedYear": self.established_year,
            "acreage": self.acreage,
            "isActive": self.is_active,
            "createdAt": self.created_at.isoformat(),
            "updatedAt": self.updated_at.isoformat(),
        }

    def __repr__(self):
        return f"<Farm {self.name}>"