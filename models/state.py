#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from models.city import City
import models
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship("City", backref="state", cascade="all, delete")

    @property
    def cities(self):
        """
        Represents the FileStorage relationship between State and City and
        returns the list of City instances with state_id equals
        to the current State.id
        """

        cities = models.storage.all(City)
        state_cities = []

        for value in cities.values():
            if value["state_id"] == self.id:
                state_cities.append(City(**value))

        return state_cities
