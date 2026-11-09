🌍 Live AQI India Monitor

A real-time Air Quality Index (AQI) monitoring platform that tracks air quality across 103 cities in India. The application fetches atmospheric data from the Open-Meteo Air Quality API, processes it through a FastAPI backend, and displays city-wise air quality information through a React dashboard.

🚀 Overview

Live AQI India Monitor provides a centralized dashboard to explore air quality conditions across Indian cities.

The platform uses a modern full-stack architecture with a React frontend, Python FastAPI backend, and PostgreSQL database. Docker support helps simplify deployment and environment management.

Note: AQI values are derived from modelled atmospheric data provided by Open-Meteo. They are not direct measurements from physical ground-based monitoring stations. Nearby cities may sometimes share similar model-grid values.

✨ Features

* 103 Indian Cities: Monitor air quality across multiple Indian cities.
* Live Data Integration: Fetch atmospheric air-quality data using the Open-Meteo API.
* AQI Dashboard: View air-quality information through a React-based interface.
* City Rankings: Compare cities based on their air-quality levels.
* Backend REST API: Access AQI information through FastAPI endpoints.
* PostgreSQL Database: Store city information and AQI records.
* Docker Support: Containerization and environment management.
* Interactive API Documentation: Explore endpoints using Swagger UI.

🛠️ Tech Stack

Category	Technologies
Frontend	React.js, Vite, JavaScript, CSS
Backend	Python, FastAPI
Database	PostgreSQL 17
ORM	SQLAlchemy
External API	Open-Meteo Air Quality API
Containerization	Docker, Docker Compose
API Documentation	Swagger UI

🏗️ Architecture

                 ┌─────────────────────────┐
                 │       Open-Meteo        │
                 │    Air Quality API      │
                 └────────────┬────────────┘
                              │
                              ▼
                 ┌─────────────────────────┐
                 │      FastAPI Backend    │
                 │                         │
                 │  Data Fetching          │
                 │  Processing             │
                 │  REST API               │
                 └────────────┬────────────┘
                              │
                              ▼
                 ┌─────────────────────────┐
                 │      PostgreSQL         │
                 │       Database          │
                 └────────────┬────────────┘
                              │
                              ▼
                 ┌─────────────────────────┐
                 │     React Frontend      │
                 │                         │
                 │    AQI Dashboard        │
                 │    City Rankings        │
                 └─────────────────────────┘

📂 Project Structure

LIVE_AQI_SIDDHESH_DOCKER/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── scripts/
│   │   └── main.py
│   │
│   ├── docker-compose.yml
│   └── requirements.txt
│
├── frontend/
│   ├── public/
│   ├── src/
│   ├── package.json
│   └── vite.config.js
│
└── README.md

⚙️ Getting Started

Follow these instructions to run the project locally.

Prerequisites

Make sure you have installed:

* Python 3.10+
* Node.js and npm
* PostgreSQL 17
* Git
* Docker Desktop (optional)

1. Clone the Repository

git clone https://github.com/siddheshx/LIVE_AQI_MONITOR_INDIA.git
cd LIVE_AQI_MONITOR_INDIA

2. Backend Setup

Navigate to the backend directory:

cd backend

Create and activate a virtual environment:

macOS / Linux

python3 -m venv venv
source venv/bin/activate

Windows

python -m venv venv
venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Configure your environment variables using the configuration expected by the backend.

Start the FastAPI server:

uvicorn app.main:app --reload

Backend API:

http://127.0.0.1:8000

Swagger API Documentation:

http://127.0.0.1:8000/docs

3. Frontend Setup

Open another terminal and navigate to the frontend directory:

cd frontend

Install dependencies:

npm install

Start the development server:

npm run dev

Open the local URL displayed by Vite in your browser.

4. Database Setup

Make sure PostgreSQL is running and configure the database connection using the environment variables expected by the backend.

The project uses PostgreSQL, with the database port configured as 5433 in the current development setup.

5. Docker Setup

Docker Compose configuration is available in the backend directory.

To start the configured services:

cd backend
docker compose up --build

To stop the services:

docker compose down

🔌 API Endpoints

The backend exposes REST API endpoints under /api/v1.

Method	Endpoint	Description
GET	/api/v1/cities	Retrieve available cities
GET	/api/v1/aqi/latest	Retrieve latest AQI records
GET	/api/v1/aqi/rankings	Retrieve city-wise AQI rankings
POST	/api/v1/aqi/refresh	Trigger AQI data refresh
GET	/health	Check backend health

Explore the complete API documentation at:

http://127.0.0.1:8000/docs

📊 Data Source

This project uses the Open-Meteo Air Quality API to retrieve modelled atmospheric information.

Data source: Open-Meteo

The displayed AQI information is based on available modelled data and should not be treated as an official regulatory measurement or a replacement for government monitoring-station readings.

🔮 Future Improvements

* Fully containerized frontend, backend, and database deployment.
* Automated AQI data refresh using scheduled jobs.
* Historical AQI trends and visualizations.
* Improved monitoring and application logging.
* CI/CD pipeline integration.
* Cloud deployment.
* Automated testing.

👨‍💻 Author

Siddhesh Deshmukh

B.Tech Computer Science & Engineering
NIELIT Aurangabad

Interested in DevOps, Cloud Computing, Platform Engineering, and Software Development.

* GitHub: @siddheshx
* LinkedIn: Siddhesh Deshmukh

⸻

⭐ If you find this project interesting, consider giving it a star!