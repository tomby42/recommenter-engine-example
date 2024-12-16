# Example Recommendation Engine Mock

The structure of this repository is based on the [Full Stack FastAPI Template](https://github.com/fastapi/full-stack-fastapi-template/).

## Getting Started

### Configuration

1. Copy the `.env.in` file to `.env` file:
   ```bash
   cp .env.in .env
   ```
2. Update the `.env` file to configure the application settings. **At a minimum**, ensure you set secure values for:
   - `SECRET_KEY`: A strong secret key for application security.
   - `FIRST_SUPERUSER_PASSWORD`: Password for the initial superuser account.
   - `POSTGRES_PASSWORD`: Password for the PostgreSQL database.

---

### Running Locally

To run the application locally, follow these steps:

1. Start the local stack using Docker Compose:
   ```bash
   docker compose up -d
   ```

2. Access the API documentation and test the endpoints at:  
   [http://0.0.0.0:8000/docs](http://0.0.0.0:8000/docs)

---

## REST API Endpoints

The following are the main API endpoints provided by the application:

- **`POST /api/v1/items/uploadcsv`**  
  Upload a CSV file containing car data to the database.

- **`GET /api/v1/items/recommend/{item_id}/similar`**  
  Retrieve a list of items similar to the specified item.

- **`GET /api/v1/items/recommend/most_popular`**  
  Retrieve a list of the most popular items.

- **`POST /api/v1/items/recommend/similar_query`**  
  Retrieve the items most similar to a given query.

- **`POST /api/v1/users/{user_id}/recommendations`**  
  Retrieve personalized recommendations for the specified user.

- **`POST /api/v1/events/`**  
  Record an event in the system, such as user interactions or item-related actions.

---

## Directory Structure

```plaintext
.
├── data
│   └── cars.csv                         # Test car dataset
├── backend                              # Backend directory
│   ├── alembic.ini                      # Alembic configuration file for database migrations
│   ├── app                              # Main application directory
│   │   ├── alembic                      # Alembic migration scripts and management
│   │   ├── api                          # REST API implementation
│   │   │   ├── deps.py                  # Dependency injection for API routes
│   │   │   ├── main.py                  # API entry point
│   │   │   └── routes                   # API route definitions
│   │   │       ├── events.py            # Routes related to event management
│   │   │       ├── items.py             # Routes related to item management
│   │   │       ├── items_recommend.py   # Routes for item recommendations
│   │   │       ├── login.py             # Authentication and login routes
│   │   │       ├── private.py           # Private or restricted routes
│   │   │       ├── users.py             # Routes for user management
│   │   │       └── utils.py             # Utility routes and helper endpoints
│   │   ├── core                         # Core application logic and configurations
│   │   │   ├── config.py                # Configuration settings for the app
│   │   │   ├── db.py                    # Database connection and setup
│   │   │   └── security.py              # Security-related utilities
│   │   ├── crud                         # CRUD operations for database models
│   │   │   ├── csv.py                   # CRUD utilities for handling CSV data
│   │   │   └── __init__.py              # Package initialization, basic CRUD operations
│   │   ├── main.py                      # Application entry point
│   │   ├── models                       # Database model definitions
│   │   │   ├── event.py                 # Model for events
│   │   │   ├── __init__.py              # Package initialization, generic models
│   │   │   ├── item.py                  # Model for items
│   │   │   └── user.py                  # Model for users
│   │   ├── recommend                    # Recommendation system logic
│   │   │   └── recommender.py           # Recommendation algorithm implementation
│   │   ├── tests                        # Directory for application tests
│   ├── cron                             # Cron job configuration and management
│   │   └── cron-tasks                   # Definitions for scheduled tasks
│   ├── Dockerfile                       # Dockerfile for backend containerization
│   ├── pyproject.toml                   # Python project configuration (e.g., dependencies)
│   └── scripts                          # Scripts for automation and setup
│       ├── cron_job.sh                  # Script for cron job execution
│       ├── prestart.sh                  # Script to run before starting the app
│       ├── test.sh                      # Script for running tests
│       └── tests-start.sh               # Script for initializing tests and run them
├── docker-compose.override.yml          # Overrides for Docker Compose configuration
├── docker-compose.traefik.yml           # Docker Compose configuration with Traefik
├── docker-compose.yml                   # Main Docker Compose configuration
└── README.md                            # Project documentation file
```

---

### Additional Notes

- **Testing**: Run the `scripts/tests-start.sh` script in `backend` directory to run tests and validate functionality. Make sure that your PostgreSQL server is running and you have configured credentials.
