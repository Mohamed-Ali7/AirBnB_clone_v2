#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
import models
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime


Base = declarative_base()


class BaseModel():
    """A base class for all hbnb models"""

    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """
        Instatntiates a new instances of the class

        Args:
            args (list): A list that conttains all
            the attributes of the new instance to create

            kwargs (dict): A dictionary that conttains all
            the attributes of the new instance to create
        """

        if kwargs:
            if "id" not in kwargs:
                self.id = str(uuid.uuid4())
                self.created_at = datetime.now()
                self.updated_at = datetime.now()

            for key, value in kwargs.items():
                if key == "__class__":
                    continue
                elif key == "created_at" or key == "updated_at":
                    setattr(self, key, datetime.fromisoformat(value))
                else:
                    if key not in self.__class__.__dict__:
                        raise KeyError
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

    def __str__(self):
        """Return the string representation of an instance"""

        class_name = self.__class__.__name__
        return "[{}] ({}) {}".format(class_name, self.id, self.__dict__)

    def save(self):
        """
        Updates the public instance attribute
        (updated_at) with the current datetime
        """

        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        res = {}
        for key, value in self.__dict__.items():
            if key != '_sa_instance_state':
                if isinstance(value, datetime):
                    res[key] = value.isoformat()
                else:
                    res[key] = value
        res['__class__'] = self.__class__.__name__
        return res

    def delete(self):
        """Deletes the current instance from the storage"""
        models.storage.delete(self)
