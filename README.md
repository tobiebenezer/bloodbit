# BloodBit API

A RESTful backend service for managing blood donor networks, inventory levels, and hospital transfusion requests. Built with Flask, SQLAlchemy, Flask-Migrate, and JWT authentication.

---

## Architecture & Features

- **Application Factory**: Modular app setup via `create_app()` with configuration inheritance for dev, testing, and production.
- **Authentication & RBAC**: JWT-based stateless auth (`Flask-JWT-Extended`) with protected endpoints, token refresh flows, and user identity lookups.
- **Database Layer**: SQLAlchemy ORM with explicit relationships (`User`, `Donor`, `BloodRequest`, `BloodDonation`) and schema version control using `Flask-Migrate` (Alembic).
- **Interactive Documentation**: Integrated Swagger/OpenAPI documentation powered by `Flasgger`.
- **Production Ready**: Gunicorn-compatible WSGI entry point (`wsgi.py`) and environment-driven configurations.

---

## Core Domain Modules

- **Authentication (`/auth`)**: User registration, login, token refresh, and credential validation.
- **Donors (`/donors`)**: Donor profile registration, eligibility tracking, and blood group categorization.
- **Blood Requests (`/blood-requests`)**: Hospital and clinic requisition management, urgency scoring, and status workflows.
- **Donation Logging (`/blood-donations`)**: Inventory updates, donation history tracking, and fulfillment confirmation.

---

## Getting Started

### 1. Prerequisites
- Python 3.10+
- PostgreSQL or SQLite (default for development)

### 2. Setup Environment
```bash
git clone https://github.com/tobiebenezer/bloodbit.git
cd bloodbit

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file in the root directory:
```env
FLASK_APP=main.py
FLASK_ENV=development
SECRET_KEY=your-secure-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
DATABASE_URL=sqlite:///bloodbit.db
```

### 4. Database Initialization & Migrations
```bash
flask db upgrade
```

### 5. Run the Application
For development:
```bash
python main.py
# or using the startup script
./devserver.sh
```

For production via WSGI:
```bash
gunicorn wsgi:app --bind 0.0.0.0:8080
```

---

## API Documentation

Once the server is running locally, navigate to:
```
http://127.0.0.1:8080/apidocs/
```
to explore the interactive Swagger UI and test endpoints directly.

---

## Testing

Run the test suite:
```bash
pytest tests/
```

---

## License

Developed by [Tobi Ebenezer](https://github.com/tobiebenezer). Licensed under MIT.
