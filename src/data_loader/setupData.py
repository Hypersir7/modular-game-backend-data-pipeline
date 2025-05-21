import psycopg2 # type: ignore
from psycopg2.extras import RealDictCursor # type: ignore

import os

# MY MODULES IMPORTS
from database_manager import DatabaseManager
from modules.players import PlayersLoader
from modules.objects import ObjectsLoader
from modules.monsters import MonstersLoader
from convertor import Convertor

# DATA FILPATHS
currentDir = os.path.dirname(os.path.abspath(__file__))
playersFilePath = os.path.join(currentDir, "..", "..", "data", "joueurs.csv")
objectsFilePath = os.path.join(currentDir, "..", "..", "data", "objets.csv")
monstersFilePath = os.path.join(currentDir, "..", "..", "data", "monstres.xml")

def main():
	dbManager = DatabaseManager()

	dbManager.connectToDatabase(dbName="gamedata", username="game_admin", password="1919") # type: ignore

	# ----- LOADING PLAYERS DATA -----
	pLoader = PlayersLoader()
	pLoader.loadPlayers(playersFilePath)
	
	# ----- LOADING OBJECTS DATA -----
	oLoader = ObjectsLoader()
	oLoader.loadObjects(objectsFilePath)

	# ----- LOADING MONSTERS DATA -----
	mLoader = MonstersLoader()
	mLoader.loadMonsters(monstersFilePath)

	# ----- FETCHING AND DISPLAYING DATA -----
	try:
		print("\n\n[RESULT] PLAYERS RETRIEVED DATA : ")
		dbManager.execute("SELECT * from player") 
		playersData = dbManager.fetchData() 
		dbManager.displayFetchedData(playersData) 
		

		print("\n\n[RESULT] OBJECTS RETRIEVED DATA : ")
		dbManager.execute("SELECT * from object") 
		objectsData = dbManager.fetchData() 
		dbManager.displayFetchedData(objectsData) 

		print("\n\n[RESULT] MONSTERS RETRIEVED DATA : ")
		dbManager.execute("SELECT * from monster") 
		monstersData = dbManager.fetchData() 
		dbManager.displayFetchedData(monstersData) 

	except Exception as e:
		print(f"[ERROR] could not retrieve data! : {e}")
		dbManager.rollback();

if __name__ == "__main__":
	main()