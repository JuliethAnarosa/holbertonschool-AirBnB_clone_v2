#!/usr7bin/python3
"""
Este módulo define una clase para administrar el almacenamiento
de la base de datos para el clon de hbnb
"""
from models.base_model import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.state import State
from models.amenity import Amenity
from models.review import Review
import os
import models

classes = {'User': User, 'Place': Place,
           'State': State, 'City': City,
           'Amenity': Amenity, 'Review': Review}


class DBStorage():

    __engine = None
    __session = None

    def __init__(self):
        """
        Crea una instancia del almacenamiento de la
        base de datos para crear el motor
        """
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".format(
                                      os.environ.get('HBNB_MYSQL_USER'),
                                      os.environ.get('HBNB_MYSQL_PWD'),
                                      os.environ.get('HBNB_MYSQL_HOST'),
                                      os.environ.get('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)
        if os.environ.get('HBNB_ENV') == 'test':
            self.__session.drop_all(self.__engine)

    def all(self, cls=None):
        """
        consulta sobre la sesión actual de la base de datos
        """
        new_dic = {}
        if cls is None:
            for key, value in classes.items():
                list_obj = self.__session.query(value).all()
                for item in list_obj:
                    key = "{}.{}".format(item.__class__.__name__, item.id)
                    new_dic.update({key: item})

        else:
            list_obj = self.__session.query(cls).all()
            for value in list_obj:
                key = "{}.{}".format(value.__class__.__name__, value.id)
                new_dic.update({key: value})
        return new_dic

    def new(self, obj):
        """
        Método para agregar el objeto a la
        sesión actual de la base de datos
        """
        self.__session.add(obj)

    def save(self):
        """
        Método para confirmar todos los cambios de la
        sesión actual de la base de datos
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        Método eliminar de la
        sesión de base de datos actual obj si no es None
        """
        if obj is not None:
            self.__session.delete(obj)
            session.commit()

    def reload(self):
        """
        crear todas las tablas en la base de datos
        """
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session()

    def close(self):
        """
        llamar al método remove() en el atributo de sesión privada
        """
        self.__session.close()
