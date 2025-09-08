#  Telemedicine API

A robust and scalable backend for a telemedicine platform, built with **Flask**, **PostgreSQL**, and **WebSockets**. This API supports secure **user authentication**, **role-based access**, **appointment management**, and **real-time doctor status updates**.

Fully containerized with **Docker** and easily extensible for production deployments.

---

##  Features

-  **User Authentication**  
  Secure registration and login with **JWT (JSON Web Tokens)**

-  **Role-Based Access Control**  
  Separate access rules for **doctors** and **patients**

-  **Appointment Management**  
  Patients can schedule appointments and view their bookings

-  **Real-Time Communication**  
  Doctor availability/status updates using **WebSockets**

-  **Interactive API Documentation**  
  Auto-generated with **Flasgger** (Swagger UI)

---

##  Prerequisites

Make sure the following tools are installed:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/) (usually comes with Docker Desktop)

---

##  Getting Started

### 1️ Clone the Repository

```bash
git clone https://github.com/RahulPatil-Tech/Telemedicine-API.git
cd Telemedicine-API
```

### 2️ Start the Services

Use Docker Compose to build and run the application:

```bash
docker compose up --build
```

### 3️ Access the Application

- **API Base URL:** `http://localhost:5000`
- **Swagger UI (API Docs):** [http://localhost:5000/apidocs/](http://localhost:5000/apidocs/)

---

##  Project Structure

```
├── app/
│   ├── __init__.py        # App factory and setup
│   ├── auth.py            # Role-based access decorators
│   ├── models.py          # SQLAlchemy models (User, Appointment)
│   └── routes.py          # API routes + WebSocket logic
├── config.py              # Environment config
├── docker-compose.yml     # Docker services config
├── Dockerfile             # Flask app image definition
├── requirements.txt       # Python dependencies
└── run.py                 # Application entry point
```

---

##  Environment Variables

Environment configuration is handled via variables defined in `docker-compose.yml`. You can override these as needed.

| Variable         | Description                            | Default Value                                                     |
|------------------|----------------------------------------|-------------------------------------------------------------------|
| `DATABASE_URL`   | PostgreSQL connection URI              | `postgresql://rp32:Strong%40123@db:5432/telemedicine_db`         |
| `SECRET_KEY`     | Flask session secret                   | `a_strong_and_random_fallback_secret_key`                        |
| `JWT_SECRET_KEY` | Secret for JWT signing                 | `a_different_strong_and_random_jwt_key`                          |

---

##  Contributing

We welcome contributions! 

-  Open an issue to discuss new features or improvements
-  Fork the repo, create a branch, and submit a **pull request**
-  Make sure your code passes linting and tests

---

##  License

This project is open-source and available under the **MIT License**.

---

## Support

If you find this project helpful, consider giving it a on GitHub and sharing it with others in the developer community.
