#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.city import City
from os import getenv
import models

storecondition = getenv("HBNB_TYPE_STORAGE")


class State(BaseModel, Base):
    """ State class """
    if storecondition == "db":
        __tablename__ = "states"
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="states")
    else:
        name = ""

    if storecondition != "db":
        @property
        def cities(self):
            """Returns a list of City instances with state_id equals
            to the current State.id"""
            citylist = []
            allcitys = models.storage.all(City)
            for value in allcitys.values():
                if city.state_id == self.id:
                    citylist.append(value))
            return citylist
