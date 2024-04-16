#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from models.review import Review
import models
from sqlalchemy import Column, String, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    amenity_ids = []
    reviews = relationship("Review", backref="place", cascade="all, delete")

    @property
    def reviews(self):
        """
        Represents the FileStorage relationship between Place and Review and
        returns the list of Review instances with place_id equals
        to the current Place.id
        """

        reviews_objects = models.storage.all(Review)
        place_reviews = []

        for value in reviews_objects.values():
            if value["place_id"] == self.id:
                place_reviews.append(Review(**value))
