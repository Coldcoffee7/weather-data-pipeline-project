# Weather Data Pipeline (Airflow + Docker)

## 📌 Overview
This project builds a production-style data pipeline using Apache Airflow to ingest weather data from an external API.

## ⚙️ Tech Stack
- Apache Airflow
- Docker 
- Python
- REST API (WeatherStack)
- PostgreSQL

## 🔄 Pipeline Flow
1. Fetch weather data from API
2. Transform data
3. Store into database
4. Schedule daily using Airflow DAG

## 🚀 How to Run
1. Get data from weather API
    - Get access key from weatherstack.com
    - Run api-request.py 
    
2. Set up Postgres DB using Docker
    - Find latest docker image for postgres in docker
    - docker-compose.yml
    - Run docker-compose up
    - Run docker-compose exec db psql -U db_user -d db (to test out db)
3. Store data in Postgres DB
    - Create table in postgres with create_table()
    - Insert data into table with insert_records()
4. Automate data ingestion using Airflow
- Set up airflow using docker (update docker-compose.yml)
- Run docker-compose up (to initialize airflow and migrate db)
- Run docker-compose exec db psql -U db_user -d db (to confirm airflow_db has been successfully created and there are tables in the public schema)
- orchestrator.py for dag
- Go to airflow UI and click trigger DAG
