# 🧠 KMeans++ Async Web API
Overview

This project implements an asynchronous FastAPI-based web service that provides user authentication, chat management, and machine learning clustering using the KMeans++ algorithm.

It supports secure user management, asynchronous database operations, and efficient centroid storage for previously trained KMeans models.

The system is designed with scalability, modularity, and data security in mind — suitable for both research and production use.

# ⚙️ Technologies Used

FastAPI — asynchronous web framework for Python

SQLAlchemy (async) — ORM for defining and querying models asynchronously

asyncpg — high-performance PostgreSQL driver

psycopg[binary] — binary-based PostgreSQL adapter

Alembic — database migrations manager

NumPy — numerical computations for KMeans++

python-jose — JWT token generation and verification

passlib[bcrypt] — password hashing and verification

python-dotenv — environment configuration management

uvicorn — ASGI server for running FastAPI apps

uuid — unique identifier generation for entities

# 🧩 Modules

users → handles registration, login, JWT authentication, and password hashing

chats → manages user conversations and related metadata

centers → stores and retrieves KMeans cluster centers for previously trained datasets

core → contains security, token, and utility functions

database → manages the async SQLAlchemy engine, session, and Base model

ml.kmeans → implements the KMeans++ clustering algorithm with custom Helper and Cluster classes

# 🔐 Security

Passwords are hashed using Passlib’s bcrypt algorithm

Tokens are generated using python-jose (JWT)

All protected routes require a valid access token

# 🧱 Database & Migration Setup

This project uses PostgreSQL as the primary database.
Migrations are managed with Alembic, and asynchronous connections are handled by SQLAlchemy with asyncpg.

#🪜 Steps to Set Up:

1. Create and activate a virtual environment:

```bash
pipenv install --python 3.11
pipenv shell
```

2. Install dependencies:

```bash
pipenv install
pip install -r requirements.txt
```

3. Set up your environment variables:
Create a .env file in the project root with:

```bash
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/dbname
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_MINUTES = 30
REFRESH_TOKEN_DAYS = 7
VITE_API_URL = http://localhost:5173
```
4. Configure Alembic:
In alembic.ini, set:
```bash
sqlalchemy.url = postgresql+asyncpg://username:password@localhost:5432/dbname
```
5. Ensure migrations are properly loaded:
In alembic/env.py, import:
```bash
from database import Base
from modules import *
target_metadata = Base.metadata
```
6. Generate and apply migrations:
```bash
alembic revision --autogenerate -m "initial migration"
alembic upgrade head
```
#🚀 Running the Application

Once the environment and database are set up, start the FastAPI app:
```bash
uvicorn main:app --reload
```

# 🧮 Machine Learning (KMeans++)

The app integrates a custom-built KMeans++ implementation:

Uses probabilistic center initialization to avoid poor clustering

Iteratively adjusts centers until convergence or max iterations

Stores trained centers in the centers table for reuse

Main components:

Helper → calculates distance probabilities

Cluster → manages group memberships

KMeans → performs training and convergence checking

# 📦 Dependencies
```bash
alembic==1.17.0
asyncpg==0.30.0
bcrypt==4.0.1
cryptography==46.0.3
dotenv==0.9.9
fastapi==0.120.0
numpy==2.3.4
passlib==1.7.4
psycopg==3.2.11
psycopg-binary==3.2.11
python-dotenv==1.1.1
python-jose==3.5.0
python-multipart==0.0.20
SQLAlchemy==2.0.44
uuid==1.30
uvicorn==0.38.0
```
