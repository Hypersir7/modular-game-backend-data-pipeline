Setup the project before launching main.py

# Setup : 

1. sudo apt update
2. sudo apt install postgresql postgresql-contrib
3. sudo service postgresql start
4. sudo -u postgres psql # This will open the sql terminal

In the sql Terminal : 

5. Create a new user:
	CREATE USER game_admin WITH PASSWORD '1919';

6. Create a new database
	CREATE DATABASE gamedata OWNER game_admin;

7. Give the user privileges
	GRANT ALL PRIVILEGES ON DATABASE gamedata TO game_admin;

8. \q # close the sql terminal


9. Create the tables using (you should be inside the project folder): 
	psql -U game_admin -d gamedata -h localhost -f database/setup.sql

10. Run setupData to insert the values in the tables 

Now you can run main.py

===========================================================================================================================

# Project Structure - Data Loader

## IMPORTANT INFORMATION

Inside the src/data_loader/ folder, you will find the backend scripts of the project.

The data_loader/ directory is responsible for loading, converting, and inserting game data into the database in a secure and modular way (Low coupling + high cohesion architecture)


### Structure of data_loader/

data_loader/
├── convertor.py             # Safely converts values (e.g., string to int) with error handling, etc
├── database_manager.py      # Manages database connections, queries, transactions, and rollbacks, etc
├── loadingInfo.log          # Log file : INFO ON loading operations and warnings
├── modules/                 # Independant modules to handle and load enteties DATA
│   ├── characters.py        # Loads character data 
│   ├── monsters.py          # Loads monsters 
│   ├── npcs.py              # Loads NPCs and their quests, dialogues, inventories
│   ├── objects.py           # Loads inventory items
│   ├── players.py           # Loads player data
│   ├── quests.py            # Loads quests, xp, difficulty, etc
│   └── spells.py            # Loads spells 
├── pycache/                 
│   └── *.pyc
└── setupData.py             # Main script that coordinates the full data loading, fetching and displaying process
