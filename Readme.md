# Flask Superheroes API

A RESTful API for managing superheroes, their powers, and the relationships between them. Built with Flask and SQLAlchemy.

## Author
**Your Name** - Flask Superheroes API Implementation

## Description

This Flask application provides a complete API for managing superheroes and their powers. The API allows you to:

- View all heroes and their individual details
- Browse available superpowers
- Create associations between heroes and powers
- Update power descriptions
- Manage hero-power relationships with strength levels

The application follows RESTful conventions and returns JSON responses for all endpoints.

## Features

### Core Functionality
- **Hero Management**: Create, read, and manage superhero profiles
- **Power Management**: Manage superpowers with descriptions and validations
- **Relationship Tracking**: Associate heroes with powers and track strength levels
- **Data Validation**: Ensure data integrity with built-in validations
- **Error Handling**: Comprehensive error responses for invalid requests

### API Endpoints
- `GET /heroes` - List all heroes
- `GET /heroes/:id` - Get specific hero with their powers
- `GET /powers` - List all available powers
- `GET /powers/:id` - Get specific power details
- `PATCH /powers/:id` - Update power description
- `POST /hero_powers` - Create new hero-power association

### Data Models
- **Hero**: Stores hero information (name, super_name)
- **Power**: Stores power information with validated descriptions
- **HeroPower**: Junction table managing hero-power relationships with strength levels

## Setup Instructions

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd flask-superheroes-api
   ```

2. **Install dependencies**
   ```bash
   pip install pipenv
   pipenv install
   pipenv shell
   ```

3. **Set up the database**
   ```bash
   # Initialize the database
   flask db init
   
   # Create migration
   flask db migrate -m "Initial migration"
   
   # Apply migration
   flask db upgrade
   ```

4. **Seed the database**
   ```bash
   python seed.py
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

The API will be available at `http://localhost:5555`

## API Usage Examples

### Get all heroes
```bash
curl http://localhost:5555/heroes
```

### Get a specific hero
```bash
curl http://localhost:5555/heroes/1
```

### Update a power description
```bash
curl -X PATCH http://localhost:5555/powers/1 \
  -H "Content-Type: application/json" \
  -d '{"description": "An amazing power that grants incredible strength to the wielder"}'
```

### Create a hero-power association
```bash
curl -X POST http://localhost:5555/hero_powers \
  -H "Content-Type: application/json" \
  -d '{"strength": "Strong", "hero_id": 1, "power_id": 2}'
```

## Data Validations

### Power Model
- **Description**: Must be present and at least 20 characters long

### HeroPower Model
- **Strength**: Must be one of: 'Strong', 'Weak', 'Average'

## Error Handling

The API returns appropriate HTTP status codes and error messages:

- **200**: Success
- **201**: Created successfully
- **400**: Bad request (validation errors)
- **404**: Resource not found

Error responses follow the format:
```json
{
  "error": "Resource not found"
}
```

Or for validation errors:
```json
{
  "errors": ["Validation error message"]
}
```

## Project Structure

```
flask-superheroes-api/
├── app.py              # Main Flask application
├── models.py           # Database models
├── seed.py             # Database seeding script
├── Pipfile             # Python dependencies
├── README.md           # This file
├── migrations/         # Database migrations
└── instance/           # SQLite database file
```

## Database Schema

### Heroes Table
- `id` (Primary Key)
- `name` (String, required)
- `super_name` (String, required)

### Powers Table
- `id` (Primary Key)
- `name` (String, required)
- `description` (String, required, min 20 chars)

### HeroPowers Table
- `id` (Primary Key)
- `strength` (String, required: 'Strong'/'Weak'/'Average')
- `hero_id` (Foreign Key)
- `power_id` (Foreign Key)

## Technologies Used

- **Flask**: Web framework
- **SQLAlchemy**: ORM for database operations
- **Flask-Migrate**: Database migration management
- **SQLite**: Database (development)

## Support

For issues, questions, or contributions:

- **Email**: your.email@example.com
- **GitHub**: Create an issue in the repository
- **Documentation**: Refer to Flask and SQLAlchemy documentation

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

*Built as part of the Flask Superheroes coding challenge*