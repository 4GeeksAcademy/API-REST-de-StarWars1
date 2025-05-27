from app import app
from models import db, User, People, Planet

def populate_database():
    with app.app_context():
       
        db.drop_all()
        db.create_all()

        
        users = [
            User(email="user1@test.com", password="123456", is_active=True),
            User(email="user2@test.com", password="123456", is_active=True)
        ]
        db.session.add_all(users)

       
        characters = [
            People(name="Luke Skywalker", height="172", mass="77", hair_color="blond"),
            People(name="Darth Vader", height="202", mass="136", hair_color="none"),
            People(name="Leia Organa", height="150", mass="49", hair_color="brown"),
            People(name="Han Solo", height="180", mass="80", hair_color="brown"),
            People(name="Yoda", height="66", mass="17", hair_color="white")
        ]
        db.session.add_all(characters)

       
        planets = [
            Planet(name="Tatooine", diameter="10465", climate="arid", population="200000"),
            Planet(name="Alderaan", diameter="12500", climate="temperate", population="2000000000"),
            Planet(name="Hoth", diameter="7200", climate="frozen", population="unknown"),
            Planet(name="Endor", diameter="4900", climate="forest", population="30000000"),
            Planet(name="Coruscant", diameter="12240", climate="temperate", population="1000000000000")
        ]
        db.session.add_all(planets)

        db.session.commit()
        print("✅ ¡Datos insertados correctamente!")

if __name__ == '__main__':
    populate_database()