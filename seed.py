from app import app
from models import db, Hero, Power, HeroPower

with app.app_context():
    print("🌱 Seeding data...")


    HeroPower.query.delete()
    Hero.query.delete()
    Power.query.delete()

  
    super_strength = Power(
        name="super strength", 
        description="gives the wielder super-human strengths"
    )
    flight = Power(
        name="flight", 
        description="gives the wielder the ability to fly through the skies at supersonic speed"
    )
    super_senses = Power(
        name="super human senses", 
        description="allows the wielder to use her senses at a super-human level"
    )
    elasticity = Power(
        name="elasticity", 
        description="can stretch the human body to extreme lengths"
    )

    db.session.add_all([super_strength, flight, super_senses, elasticity])
    db.session.commit()


    heroes_data = [
        {"name": "Wanjiku Kamau", "super_name": "Lightning Strike"},
        {"name": "Kipchoge Rotich", "super_name": "Speed Runner"},
        {"name": "Akinyi Ochieng", "super_name": "Lake Guardian"},
        {"name": "Njoroge Mwangi", "super_name": "Mountain Shield"},
        {"name": "Amina Hassan", "super_name": "Desert Wind"},
        {"name": "Baraka Omondi", "super_name": "Storm Caller"},
        {"name": "Rehema Maina", "super_name": "Healing Touch"},
        {"name": "Jomo Kiptoo", "super_name": "Earth Shaker"},
        {"name": "Fatuma Abdullahi", "super_name": "Fire Weaver"},
        {"name": "Mwende Kiprotich", "super_name": "Shadow Walker"}
    ]

    heroes = []
    for hero_data in heroes_data:
        hero = Hero(name=hero_data["name"], super_name=hero_data["super_name"])
        heroes.append(hero)

    db.session.add_all(heroes)
    db.session.commit()


    hero_powers = [
        HeroPower(strength="Strong", hero_id=heroes[0].id, power_id=flight.id),
        HeroPower(strength="Average", hero_id=heroes[1].id, power_id=super_strength.id),
        HeroPower(strength="Weak", hero_id=heroes[2].id, power_id=super_senses.id),
        HeroPower(strength="Strong", hero_id=heroes[3].id, power_id=elasticity.id),
        HeroPower(strength="Average", hero_id=heroes[4].id, power_id=super_strength.id),
        HeroPower(strength="Strong", hero_id=heroes[5].id, power_id=flight.id),
    ]

    db.session.add_all(hero_powers)
    db.session.commit()

    print("✅ Done seeding!")
    print(f"Added {len(heroes)} heroes, {len([super_strength, flight, super_senses, elasticity])} powers, and {len(hero_powers)} hero-power associations.")