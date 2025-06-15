#!/usr/bin/env python3

from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_mail import Mail, Message
from sqlalchemy.exc import IntegrityError
import os

from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Mail configurations
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'testandonya@gmail.com'
app.config['MAIL_PASSWORD'] = 'juhu uigu aycd huzf'
app.config['MAIL_DEFAULT_SENDER'] = 'testandonya@gmail.com'



db.init_app(app)
migrate = Migrate(app, db)
mail = Mail(app)

def send_notification_email(subject, recipient, body, html_body=None):
    """Helper function to send emails"""
    try:
        msg = Message(
            subject=subject,
            recipients=[recipient],
            body=body,
            html=html_body
        )
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return False

@app.route('/')
def index():
    return {'message': 'Superheroes API with Mail Support'}

# Email sending endpoint
@app.route('/send-email', methods=['POST'])
def send_email():
    data = request.get_json()
    
    required_fields = ['recipient', 'subject', 'body']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({"errors": [f"Missing required fields: {', '.join(missing_fields)}"]}), 400
    
    success = send_notification_email(
        subject=data['subject'],
        recipient=data['recipient'],
        body=data['body'],
        html_body=data.get('html_body')
    )
    
    if success:
        return jsonify({"message": "Email sent successfully"}), 200
    else:
        return jsonify({"error": "Failed to send email"}), 500

# GET /heroes
@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    return jsonify([hero.to_dict() for hero in heroes])

# GET /heroes/<id>
@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero_by_id(id):
    hero = Hero.query.get(id)
    if not hero:
        return jsonify({"error": "Hero not found"}), 404
    
    data = hero.to_dict()
    data["hero_powers"] = [
        {
            "id": hp.id,
            "strength": hp.strength,
            "power_id": hp.power_id,
            "hero_id": hp.hero_id,
            "power": hp.power.to_dict()
        } for hp in hero.hero_powers
    ]
    return jsonify(data)

# GET /powers
@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    return jsonify([power.to_dict() for power in powers])

# GET /powers/<id>
@app.route('/powers/<int:id>', methods=['GET'])
def get_power_by_id(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404
    return jsonify(power.to_dict())

# PATCH /powers/<id>
@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404

    data = request.get_json()
    
    try:
        if 'description' in data:
            power.description = data.get("description")
        db.session.commit()
        
        # Send notification email when power is updated
        send_notification_email(
            subject="Power Updated",
            recipient="testandonya@gmail.com",
            body=f"Power '{power.name}' has been updated with new description: {power.description}"
        )
        
        return jsonify(power.to_dict()), 200
    except ValueError as e:
        db.session.rollback()
        return jsonify({"errors": [str(e)]}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"errors": ["An error occurred while updating the power"]}), 400

# POST /hero_powers
@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    
    required_fields = ['strength', 'hero_id', 'power_id']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({"errors": [f"Missing required fields: {', '.join(missing_fields)}"]}), 400
    
    hero = Hero.query.get(data['hero_id'])
    power = Power.query.get(data['power_id'])
    
    if not hero:
        return jsonify({"errors": ["Hero not found"]}), 400
    if not power:
        return jsonify({"errors": ["Power not found"]}), 400
    
    try:
        new_hp = HeroPower(
            strength=data['strength'],
            hero_id=data['hero_id'],
            power_id=data['power_id']
        )
        db.session.add(new_hp)
        db.session.commit()
        
        # Send notification email when new hero power is created
        send_notification_email(
            subject="New Hero Power Created",
            recipient="testandonya@gmail.com",
            body=f"New hero power created: {hero.name} now has {power.name} with strength {new_hp.strength}",
            html_body=f"""
            <h2>New Hero Power Created</h2>
            <p><strong>Hero:</strong> {hero.name}</p>
            <p><strong>Power:</strong> {power.name}</p>
            <p><strong>Strength:</strong> {new_hp.strength}</p>
            """
        )
        
        return jsonify(new_hp.to_dict()), 201
    except ValueError as e:
        db.session.rollback()
        return jsonify({"errors": [str(e)]}), 400
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"errors": ["Database integrity error"]}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"errors": ["An error occurred while creating the hero power"]}), 400

# POST /heroes - Create new hero with email notification
@app.route('/heroes', methods=['POST'])
def create_hero():
    data = request.get_json()
    
    required_fields = ['name', 'super_name']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({"errors": [f"Missing required fields: {', '.join(missing_fields)}"]}), 400
    
    try:
        new_hero = Hero(
            name=data['name'],
            super_name=data['super_name']
        )
        db.session.add(new_hero)
        db.session.commit()
        
        # Send welcome email notification
        send_notification_email(
            subject="New Hero Registered",
            recipient="testandonya@gmail.com",
            body=f"A new hero has been registered: {new_hero.name} (aka {new_hero.super_name})",
            html_body=f"""
            <h2>New Hero Registration</h2>
            <p><strong>Name:</strong> {new_hero.name}</p>
            <p><strong>Super Name:</strong> {new_hero.super_name}</p>
            <p>Welcome to the superhero database!</p>
            """
        )
        
        return jsonify(new_hero.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"errors": ["An error occurred while creating the hero"]}), 400

if __name__ == '__main__':
    app.run(port=5555, debug=True)