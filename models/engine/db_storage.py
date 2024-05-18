#!/usr/bin/python3

"""This module contains DBStorage class"""
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
import os


class DBStorage:
    """Represents database engine"""

    __engine = None
    __session = None

    def __init__(self):
        user = os.getenv("HBNB_MYSQL_USER")
        password = os.getenv("HBNB_MYSQL_PWD")
        host = os.getenv("HBNB_MYSQL_HOST")
        db = os.getenv("HBNB_MYSQL_DB")

        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}"
                                      .format(user, password, host, db),
                                      pool_pre_ping=True)

        if os.getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Query on the current database session all objects
        depending on the class name
        """

        objects = {}
        query = []

        if cls:
            query = self.__session.query(cls)
            for obj in query:
                obj_key = f"{obj.__class__.__name__}.{obj.id}"
                objects[obj_key] = obj
        else:
            for class_name in [City, State, User, Place, Amenity, Review]:
                query = self.__session.query(class_name).all()
                for obj in query:
                    obj_key = f"{obj.__class__.__name__}.{obj.id}"
                    objects[obj_key] = obj

        return objects

    def new(self, obj):
        """Adds the object to the current database session"""

        self.__session.add(obj)

    def save(self):
        """Commits all changes of the current database session"""

        self.__session.commit()

    def delete(self, obj=None):
        """Deletes from the current database session"""

        if obj:
            self.__session.delete(obj)

    def reload(self):
        """
        Creates all tables in the database (WARNING: all classes who inherit
        from Base must be imported before calling
        Base.metadata.create_all(engine))

        Also creates the current database session
        """

        Base.metadata.create_all(self.__engine)

        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)

        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Closes the current session"""

        self.__session.close()
