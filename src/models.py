from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    
   
    favorite_people = relationship("FavoritePeople", back_populates="user")
    favorite_planets = relationship("FavoritePlanet", back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,            
        }


class People(db.Model):
    __tablename__ = 'people'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    height: Mapped[str] = mapped_column(String(50), nullable=True)
    mass: Mapped[str] = mapped_column(String(50), nullable=True)
    hair_color: Mapped[str] = mapped_column(String(50), nullable=True)
    skin_color: Mapped[str] = mapped_column(String(50), nullable=True)
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color
        }

class Planet(db.Model):
    __tablename__ = 'planet'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    diameter: Mapped[str] = mapped_column(String(50), nullable=True)
    population: Mapped[str] = mapped_column(String(50), nullable=True)
    climate: Mapped[str] = mapped_column(String(50), nullable=True)
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "population": self.population,
            "climate": self.climate
        }

class FavoritePeople(db.Model):
    __tablename__ = 'favorite_people'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, db.ForeignKey('user.id'))
    people_id: Mapped[int] = mapped_column(Integer, db.ForeignKey('people.id'))
    
    user = relationship("User", back_populates="favorite_people")
    people = relationship("People")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "people_id": self.people_id,
            "people": self.people.serialize()
        }

class FavoritePlanet(db.Model):
    __tablename__ = 'favorite_planet'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, db.ForeignKey('user.id'))
    planet_id: Mapped[int] = mapped_column(Integer, db.ForeignKey('planet.id'))
    
    user = relationship("User", back_populates="favorite_planets")
    planet = relationship("Planet")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "planet": self.planet.serialize()
        }