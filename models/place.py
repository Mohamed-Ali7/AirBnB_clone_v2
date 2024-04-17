#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from models.review import Review
from models.amenity import Amenity
import models
import os
from sqlalchemy import Column, String, Float, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship


place_amenity = Table(
    "place_amenity", Base.metadata,
    Column("place_id", String(60), ForeignKey("places.id"),
           nullable=False, primary_key=True),
    Column("amenity_id", String(60), ForeignKey("amenities.id"),
           nullable=False, primary_key=True)
           )


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
    amenities = relationship("Amenity", secondary=place_amenity, viewonly=False)

    if os.getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def reviews(self):
            """
            Represents the FileStorage relationship between Place and Review
            and returns the list of Review instances with place_id equals
            to the current Place.id
            """

            reviews_objects = models.storage.all(Review)
            place_reviews = []

            for value in reviews_objects.values():
                if value.place_id == self.id:
                    place_reviews.append(Review(**value))

            return place_reviews

        @property
        def amenities(self):
            """
            Represents the FileStorage relationship between Place and Amenity
            and returns the list of Amenity instances based on the attribute
            amenity_ids that contains all Amenity.id linked to the Place
            """

            amenities_objects = models.storage.all(Amenity)
            place_amenities = []

            for value in amenities_objects.values():
                if value.id in self.amenity_ids:
                    place_amenities.append(Amenity(**value))

            return place_amenities

        @amenities.setter
        def amenities(self, obj):
            """
            adding an Amenity.id to the attribute amenity_ids.
            This method should accept only Amenity object,
            otherwise, do nothing.
            """

            if type(obj) is Amenity:
                if obj.id not in self.amenity_ids:
                    self.amenity_ids.append(obj.id)
