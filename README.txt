
# Modular Game Backend – Data Pipeline & Persistence Layer

## Overview
This project implements a modular backend data pipeline designed to manage, validate, convert, and ingest structured game data into a PostgreSQL database.  
The system provides a transaction-safe ingestion architecture that ensures reliable loading of game entities such as players, NPCs, quests, items, monsters, and spells.

The architecture emphasizes **low coupling, high cohesion**, and modular entity loaders, allowing scalable expansion of the data ingestion process while maintaining clean separation between game logic, ingestion modules, and persistence layers.

---

## My Contributions
- Designed and implemented the **DatabaseManager** responsible for:
  - PostgreSQL connection management
  - transaction handling and rollback mechanisms
  - query execution abstraction
  - connection lifecycle management
- Designed the **modular data ingestion pipeline architecture**
- Implemented the **entity loading modules structure**
- Structured the backend directory layout and ingestion workflow
- Implemented logging and validation support during ingestion

Other contributors implemented the interface and interaction components of the application.

---

## Architecture

```

Game Logic
↓
Data Loading Modules
↓
DatabaseManager
↓
PostgreSQL Database

````

The pipeline loads, validates, and converts structured data before securely inserting it into the persistence layer using transactional operations.

---

## Features
- PostgreSQL-backed persistence layer
- Transaction-safe ingestion with rollback support
- Modular entity loaders for scalable data management
- Structured backend architecture for maintainability
- Logging and data validation during ingestion
- Extensible loader modules for additional entity types

---

## Setup Instructions

### 1. Install PostgreSQL
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo service postgresql start
````

### 2. Open PostgreSQL terminal

```bash
sudo -u postgres psql
```

### 3. Create database user

```sql
CREATE USER game_admin WITH PASSWORD '1919';
```

### 4. Create database

```sql
CREATE DATABASE gamedata OWNER game_admin;
```

### 5. Grant privileges

```sql
GRANT ALL PRIVILEGES ON DATABASE gamedata TO game_admin;
```

Exit SQL terminal:

```sql
\q
```

---

### 6. Create tables

Run from project root directory:

```bash
psql -U game_admin -d gamedata -h localhost -f database/setup.sql
```

---

### 7. Load initial data

```bash
python src/data_loader/setupData.py
```

---

## Project Structure

```
src/
 ├── data_loader/
 │   ├── converter.py
 │   ├── database_manager.py
 │   ├── loadingInfo.log
 │   ├── modules/
 │   │   ├── characters.py
 │   │   ├── monsters.py
 │   │   ├── npcs.py
 │   │   ├── objects.py
 │   │   ├── players.py
 │   │   ├── quests.py
 │   │   └── spells.py
 │   └── setupData.py
 ├── interface/
 ├── modules/
 └── tools/
```

---

## Data Loader Responsibilities

The **data_loader** subsystem is responsible for:

* Converting raw game data into validated structured formats
* Loading entity-specific datasets through modular loaders
* Managing database transactions safely
* Ensuring rollback in case of ingestion errors
* Logging ingestion activity for monitoring and debugging

---

## Future Improvements

* Support for batch ingestion optimization
* Parallel loading pipelines for large-scale datasets
* Integration of schema validation tools
* Migration support for schema evolution
* Automated ingestion monitoring dashboard

---


