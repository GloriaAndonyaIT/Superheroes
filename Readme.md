# Flask Superheroes API

A RESTful API for managing superheroes, their powers, and the relationships between them. Built with Flask and SQLAlchemy with integrated email notification system.

## Author
**Gloria Andonya** - Flask Superheroes API Implementation

## Description

This Flask application provides a complete API for managing superheroes and their powers with advanced email notification capabilities. The API allows you to:

- View all heroes and their individual details
- Browse available superpowers
- Create associations between heroes and powers
- Update power descriptions
- Manage hero-power relationships with strength levels
- **Send automated email notifications** for all major actions
- **Custom email sending** through dedicated endpoint

The application follows RESTful conventions and returns JSON responses for all endpoints, with integrated Flask-Mail for professional email notifications.

## Features

### Core Functionality
- **Hero Management**: Create, read, and manage superhero profiles
- **Power Management**: Manage superpowers with descriptions and validations
- **Relationship Tracking**: Associate heroes with powers and track strength levels
- **Data Validation**: Ensure data integrity with built-in validations
- **Error Handling**: Comprehensive error responses for invalid requests

### 📧 Email Notification System
- **Automated Notifications**: Automatic emails sent for all major database changes
- **Power Updates**: Email alerts when power descriptions are modified
- **Hero Registration**: Welcome emails when new heroes are created
- **Hero-Power Associations**: Notifications when heroes gain new powers
- **HTML Email Support**: Rich formatting with HTML templates
- **Custom Email Endpoint**: Send custom emails through API
- **Professional SMTP**: Configured with Gmail SMTP for reliability

### API Endpoints

#### Core Endpoints
- `GET /heroes` - List all heroes
- `GET /heroes/:id` - Get specific hero with their powers
- `GET /powers` - List all available powers
- `GET /powers/:id` - Get specific power details
- `PATCH /powers/:id` - Update power description (triggers email notification)
- `POST /hero_powers` - Create new hero-power association (triggers email notification)
- `POST /heroes` - Create new hero (triggers welcome email)

#### Email Endpoints
- `POST /send-email` - Send custom email notifications

### Data Models
- **Hero**: Stores hero information (name, super_name)
- **Power**: Stores power information with validated descriptions
- **HeroPower**: Junction table managing hero-power relationships with strength levels

## Setup Instructions

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Gmail account (for email notifications)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/GloriaAndonyaIT/Superheroes
   cd superheroes
   ```

2. **Install dependencies**
   ```bash
  
   pipenv install
   pipenv shell
   ```

3. **Configure Email Settings**
   
   The application is pre-configured with Gmail SMTP. To use your own email:
   
   Update the email configuration in `app.py`:
   ```python
   app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
   app.config['MAIL_PASSWORD'] = 'your-app-password' 
   app.config['MAIL_DEFAULT_SENDER'] = 'your-email@gmail.com'
   ```
   
   **Gmail Setup Instructions:**
   - Enable 2-Factor Authentication on your Gmail account
   - Generate an App Password: Google Account → Security → 2-Step Verification → App passwords
   - Use the generated 16-character app password (not your regular Gmail password)

4. **Set up the database**
   ```bash
   # Initialize the database
   flask db init
   
   # Create migration
   flask db migrate -m "Initial migration"
   
   # Apply migration
   flask db upgrade
   ```

5. **Seed the database**
   ```bash
   python seed.py
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

The API will be available at `http://localhost:5555`

## API Usage Examples

### Core Hero Management

#### Get all heroes
```bash
curl http://localhost:5555/heroes
```

#### Get a specific hero
```bash
curl http://localhost:5555/heroes/1
```

#### Create a new hero (triggers welcome email)
```bash
curl -X POST http://localhost:5555/heroes \
  -H "Content-Type: application/json" \
  -d '{"name": "Peter Parker", "super_name": "Spider-Man"}'
```

### Power Management

#### Update a power description (triggers notification email)
```bash
curl -X PATCH http://localhost:5555/powers/1 \
  -H "Content-Type: application/json" \
  -d '{"description": "An amazing power that grants incredible strength to the wielder and allows them to lift enormous objects"}'
```

### Hero-Power Associations

#### Create a hero-power association (triggers notification email)
```bash
curl -X POST http://localhost:5555/hero_powers \
  -H "Content-Type: application/json" \
  -d '{"strength": "Strong", "hero_id": 1, "power_id": 2}'
```

### 📧 Email Features

#### Send custom email
```bash
curl -X POST http://localhost:5555/send-email \
  -H "Content-Type: application/json" \
  -d '{
    "recipient": "admin@example.com",
    "subject": "Custom Notification",
    "body": "This is a custom email message",
    "html_body": "<h2>Custom Notification</h2><p>This is a <strong>custom</strong> email message</p>"
  }'
```

## Email Notification Examples

### Automatic Email Triggers

1. **When a power is updated:**
   - **Subject**: "Power Updated"
   - **Content**: Details about the power modification
   - **Recipient**: Configured admin email

2. **When a new hero is created:**
   - **Subject**: "New Hero Registered"
   - **Content**: Welcome message with hero details
   - **Format**: HTML with styled formatting

3. **When a hero gains a new power:**
   - **Subject**: "New Hero Power Created"
   - **Content**: Hero name, power name, and strength level
   - **Format**: Both plain text and HTML versions

## Data Validations

### Power Model
- **Description**: Must be present and at least 20 characters long

### HeroPower Model
- **Strength**: Must be one of: 'Strong', 'Weak', 'Average'

### Email Model
- **Recipient**: Must be a valid email address
- **Subject**: Required field
- **Body**: Required field

## Error Handling

The API returns appropriate HTTP status codes and error messages:

- **200**: Success
- **201**: Created successfully
- **400**: Bad request (validation errors)
- **404**: Resource not found
- **500**: Server error (email sending failures)

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

Email-specific errors:
```json
{
  "error": "Failed to send email"
}
```

## Project Structure

```
flask-superheroes-api/
├── app.py              # Main Flask application with email integration
├── models.py           # Database models
├── seed.py             # Database seeding script
├── Pipfile             # Python dependencies (includes Flask-Mail)
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
- **Flask-Mail**: Email integration and SMTP handling
- **SQLite**: Database (development)
- **Gmail SMTP**: Email delivery service

## Email Configuration Details

### SMTP Settings
- **Server**: smtp.gmail.com
- **Port**: 587 (TLS)
- **Security**: TLS encryption
- **Authentication**: Username/password (App Password recommended)

### Email Features
- **HTML Templates**: Rich email formatting
- **Plain Text Fallback**: Compatibility with all email clients
- **Error Handling**: Graceful failure handling
- **Logging**: Email sending status tracking

## Kenyan Superhero Seed Data

My database comes pre-loaded with culturally relevant Kenyan superheroes:

- **Wanjiku Kamau** (Lightning Strike)
- **Kipchoge Rotich** (Speed Runner)
- **Akinyi Ochieng** (Lake Guardian)
- **Njoroge Mwangi** (Mountain Shield)
- **Amina Hassan** (Desert Wind)
- **Baraka Omondi** (Storm Caller)
- **Rehema Maina** (Healing Touch)
- **Jomo Kiptoo** (Earth Shaker)
- **Fatuma Abdullahi** (Fire Weaver)
- **Mwende Kiprotich** (Shadow Walker)

## Support

For issues, questions, or contributions:

- **Email**: gloriaandonyaa@gmail.com


### Email Support Issues
If you encounter email sending problems:
1. Verify Gmail App Password is correct
2. Check that 2FA is enabled on your Gmail account
3. Ensure SMTP settings match your email provider
4. Check application logs for detailed error messages

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

*Built as part of the Flask Superheroes coding challenge with advanced email notification system*