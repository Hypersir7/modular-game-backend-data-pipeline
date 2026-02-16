# Modular Game Backend – Data Pipeline & Persistence Layer

## Overview
This project implements a modular backend data pipeline designed to manage, validate, and ingest structured game data into a PostgreSQL database.  
The system provides a transaction-safe ingestion architecture that ensures reliable loading of game entities such as players, NPCs, quests, items, monsters, and spells.

The architecture emphasizes **low coupling, high cohesion**, and modular entity loaders, allowing scalable expansion of the data ingestion process.

---

## My Contributions
- Designed and implemented the **DatabaseManager** responsible for:
  - PostgreSQL connection management
  - transaction handling and rollback mechanisms
  - query execution abstraction
- Designed the **modular data ingestion pipeline architecture**
- Implemented the **entity loading modules structure**
- Structured the backend directory layout and ingestion workflow

Other contributors implemented the interface and interaction components of the application.

---

## Architecture
Game Logic
↓
Data Loading Modules
↓
DatabaseManager
↓
PostgreSQL Database

The pipeline loads and validates structured data before securely inserting it into the persistence layer.

---

## Features
- PostgreSQL-backed persistence layer
- Transaction-safe ingestion with rollback support
- Modular entity loaders for scalable data management
- Structured backend architecture for maintainability
- Logging and data validation during ingestion

---

## Setup

### Install PostgreSQL
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo service postgresql start
```
Create database and user
CREATE USER game_admin WITH PASSWORD '1919';
CREATE DATABASE gamedata OWNER game_admin;
GRANT ALL PRIVILEGES ON DATABASE gamedata TO game_admin;

Create tables
psql -U game_admin -d gamedata -h localhost -f database/setup.sql

Load data
python src/data_loader/setupData.py

Project Structure
src/
 ├── data_loader/
 │   ├── database_manager.py
 │   ├── converter.py
 │   ├── modules/
 │   │   ├── players.py
 │   │   ├── monsters.py
 │   │   ├── quests.py
 │   │   └── ...
 │   └── setupData.py

