# Toronto Weather Data Pipeline

An end-to-end data pipeline that ingests live weather data for the city of Toronto from the WeatherStack API,
stores it in a PostgreSQL database, and orchestrates scheduled runs using Apache Airflow —
all containerized with Docker.

## Tech Stack

| Layer            | Tool                            |
|------------------|---------------------------------|
| Orchestration    | Apache Airflow 3.0.0            |
| Containerization | Docker / Docker Compose         |
| Language         | Python                          |
| Data Source      | WeatherStack REST API           |
| Storage          | PostgreSQL 14 (`dev` schema)    |

## Architecture
WeatherStack API
│
api_request.py (Extract + Transform)
│
insert_records.py (Load → dev.raw_weather_data)
│
Airflow DAG — weather_api_orchestrator (every 5 min)

## Services

| Container             | Image                    | Port          | Role                              |
|-----------------------|--------------------------|---------------|-----------------------------------|
| `postgres_container`  | postgres:14.17           | 5001 → 5432   | Weather + Airflow metadata DB     |
| `airflow_container`   | apache/airflow:3.0.0     | 8000 → 8080   | Airflow API server + web UI       |
| `airflow_scheduler`   | apache/airflow:3.0.0     | —             | DAG scheduling (separate process) |

All three services communicate over a shared Docker bridge network (`my-network`).
Postgres data is persisted via a local volume mount (`./postgres/data`).

## Project Structure

weather_data_project/
├── airflow/
│   └── dags/
│       ├── api_request.py              # Fetches weather data from WeatherStack; includes mock for local testing
│       ├── insert_records.py           # Creates table and inserts records into PostgreSQL
│       ├── orchestrator.py             # Airflow DAG definition and task dependencies
│       └── simple_auth_manager_password...
├── postgres/
│   ├── data/                           # Persisted PostgreSQL data (gitignored)
│   └── airflow_init.sql                # Initializes the Airflow metadata database
├── docker-compose.yml
├── .gitignore
└── README.md

## Database Schema

```sql
CREATE TABLE dev.raw_weather_data (
    id                   SERIAL PRIMARY KEY,
    city                 TEXT,
    temperature          FLOAT,
    weather_descriptions TEXT,
    wind_speed           FLOAT,
    time                 TIMESTAMP,
    inserted_at          TIMESTAMP DEFAULT NOW(),
    utc_offset           TEXT,
    UNIQUE(city, time)   -- deduplicates on re-runs via ON CONFLICT DO NOTHING
);
```

## DAG Details

| Property     | Value                        |
|--------------|------------------------------|
| DAG ID       | `weather_api_orchestrator`   |
| Schedule     | Every 5 minutes              |
| Start Date   | 2026-03-24                   |
| Catchup      | Disabled                     |
| Executor     | LocalExecutor                |
| Task         | `safe_main_callable`         |

The DAG uses the **Airflow 3.x TaskFlow API** (`@dag` / `@task` decorators from
`airflow.sdk`), keeping orchestration logic clean and Pythonic.

## Getting Started

### Prerequisites

- Docker and Docker Compose installed
- A free API key from [weatherstack.com](https://weatherstack.com)

### Environment Variables

Create a `.env` file in the project root (never commit this):

WEATHER_API_KEY=your_api_key_here

### Run the Pipeline

**1. Start all services**
```bash
docker-compose up
```

This will start the Postgres database, run `airflow db migrate`, and launch both
the Airflow webserver and scheduler.

**2. Verify the database**
```bash
docker-compose exec db psql -U db_user -d db
```

**3. Open the Airflow UI**

Navigate to `http://localhost:8000`, find `weather_api_orchestrator`,
and click **Trigger DAG**.

### Local Testing (no API key needed)

`api_request.py` includes a `mock_fetch_data()` function that returns a hardcoded
Toronto payload — useful for testing the insert logic without hitting the live API.

## What I Learned

- Orchestrating multi-step pipelines with Airflow DAGs using the TaskFlow API
- Running Airflow webserver and scheduler as separate containers for production-style separation
- Containerizing interdependent services with Docker Compose using a shared bridge network
- Persisting database state across container restarts with volume mounts
- Loading secrets securely via environment variables passed through Docker Compose
- Implementing idempotent loads with `ON CONFLICT DO NOTHING` to safely handle reruns

## Roadmap

- [ ] **Add dbt transformations** — model raw weather data into clean, analytics-ready
      tables with staging and mart layers
- [ ] **Expand city coverage** — parameterize the pipeline to ingest multiple cities
      and build historical snapshots for trend analysis
- [ ] **Deploy to AWS** — migrate PostgreSQL to RDS and run Airflow on MWAA or EC2
- [ ] **Add data quality checks** — integrate dbt tests or Great Expectations to
      validate records on ingestion
- [ ] **Build a dashboard** — connect Power BI or Tableau to visualize temperature
      trends and anomalies over time
- [ ] **Alerting** — configure Airflow email or Slack alerts on DAG failure