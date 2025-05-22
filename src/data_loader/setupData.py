import psycopg2 # type: ignore
from psycopg2.extras import RealDictCursor # type: ignore

import os

# =============== MY CUSTOMIZED MODULES ===============
from database_manager import DatabaseManager
from modules.players import PlayersLoader
from modules.objects import ObjectsLoader
from modules.monsters import MonstersLoader
from modules.spells import SpellsLoader
from modules.characters import CharactersLoader
from modules.npcs import NpcsLoader
from modules.quests import QuestsLoader
from convertor import Convertor

# ==================================== DATA FILPATHS ====================================
currentDir = os.path.dirname(os.path.abspath(__file__))
playersFilePath = os.path.join(currentDir, "..", "..", "data", "joueurs.csv")
objectsFilePath = os.path.join(currentDir, "..", "..", "data", "objets.csv")
monstersFilePath = os.path.join(currentDir, "..", "..", "data", "monstres.xml")
spellsFilePath = os.path.join(currentDir, "..", "..", "data", "sorts.csv")
charactersFilePath = os.path.join(currentDir, "..", "..", "data", "personnages.json")
npcsFilePath = os.path.join(currentDir, "..", "..", "data", "pnjs.json")
questsFilePath = os.path.join(currentDir, "..", "..", "data", "quetes.xml")

def main():
	dbManager = DatabaseManager()

	dbManager.connectToDatabase(dbName="gamedata", username="game_admin", password="1919") # type: ignore

	# ----- LOADING PLAYERS DATA -----
	print("\n\n========== [INFO] LOADING PLAYERS DATA ==========")
	pLoader = PlayersLoader()
	pLoader.loadPlayers(playersFilePath)
	print(f"\n==========[RESULT] SUCCESSFULLY LOADED PLAYERS DATA ! ==========")

	# ----- LOADING OBJECTS DATA -----
	print("\n\n========== [INFO] LOADING OBJECTS DATA ==========")
	oLoader = ObjectsLoader()
	oLoader.loadObjects(objectsFilePath)
	print(f"\n==========[RESULT] SUCCESSFULLY LOADED OBJECTS DATA ! ==========")

	# ----- LOADING MONSTERS DATA -----
	print("\n\n========== [INFO] LOADING MONSTERS DATA ==========")
	mLoader = MonstersLoader()
	mLoader.loadMonsters(monstersFilePath)
	print(f"\n==========[RESULT] SUCCESSFULLY LOADED MONSTERS DATA ! ==========")

	# ----- LOADING SPELLS DATA -----
	print("\n\n========== [INFO] LOADING SPELLS DATA ==========")
	sLoader = SpellsLoader()
	sLoader.loadSpells(spellsFilePath)
	print(f"\n==========[RESULT] SUCCESSFULLY LOADED SPELLS DATA ! ==========")
	
	# ----- LOADING CHARACTERS DATA -----
	print("\n\n========== [INFO] LOADING CHARACTERS DATA ==========")
	cLoader = CharactersLoader()
	cLoader.loadCharacters(charactersFilePath)
	print(f"\n==========[RESULT] SUCCESSFULLY LOADED CHARACTERS DATA ! ==========")

	# ----- LOADING NPCS DATA -----
	print("\n\n========== [INFO] LOADING NPCS DATA ==========")
	nLoader = NpcsLoader()
	nLoader.loadNpcs(npcsFilePath)
	print(f"\n==========[RESULT] SUCCESSFULLY LOADED NPCS DATA ! ==========")

	# ----- LOADING QUESTS DATA -----
	print("\n\n========== [INFO] LOADING QUESTS DATA ==========")
	qLoader = QuestsLoader()
	qLoader.loadQuests(questsFilePath)
	print(f"\n==========[RESULT] SUCCESSFULLY LOADED QUESTS DATA ! ==========")


	# ----- FETCHING AND DISPLAYING DATA -----
	# Decomment the following lines to fetch and display data from the database
	try:
		# # ======= Fetch and display players data =======
		# print("\n\n[RESULT] PLAYERS RETRIEVED DATA : ")
		# dbManager.execute("SELECT * from player") 
		# playersData = dbManager.fetchData() 
		# dbManager.displayFetchedData(playersData) 
		
		# # ======= Fetch and display objects data =======
		# print("\n\n[RESULT] OBJECTS RETRIEVED DATA : ")
		# dbManager.execute("SELECT * from object") 
		# objectsData = dbManager.fetchData() 
		# dbManager.displayFetchedData(objectsData) 

		# # ======= Fetch and display monsters data =======
		# print("\n\n[RESULT] MONSTERS RETRIEVED DATA : ")
		# dbManager.execute("SELECT * from monster") 
		# monstersData = dbManager.fetchData() 
		# dbManager.displayFetchedData(monstersData)

		# # ======= Fetch and display spells data =======
		# print("\n\n[RESULT] SPELLS RETRIEVED DATA : ")
		# dbManager.execute("SELECT * from spell")
		# spellsData = dbManager.fetchData()
		# dbManager.displayFetchedData(spellsData)

		# # ======= Fetch and display characters data =======
		# print("\n\n[RESULT] CHARACTERS RETRIEVED DATA : ")
		# dbManager.execute("SELECT * from character")
		# charactersData = dbManager.fetchData()
		# print("[RESULT] SUCCESSFULLY FETCHED CHARACTERS DATA !")
		# dbManager.displayFetchedData(charactersData)

		# # ======= Fetch and display NPCs data =======
		# print("\n\n[RESULT] NPCS RETRIEVED DATA : ")
		# dbManager.execute("SELECT * from pnjs")
		# npcsData = dbManager.fetchData()
		# dbManager.displayFetchedData(npcsData)

		# ======= Fetch and display quests data =======
		# print("\n\n[RESULT] QUESTS RETRIEVED DATA : ")
		# dbManager.execute("SELECT * from quest")
		# questsData = dbManager.fetchData()
		# dbManager.displayFetchedData(questsData)

		print("\n[END] : SUCESSFULLY LOADED AND FETCHED  ALL DATA  (DECOMMENTE PREVIOUS LINES TO SHOW FETCHED DATA!") 

	except Exception as e:
		print(f"[ERROR] could not retrieve data! : {e}")
		dbManager.rollback();

if __name__ == "__main__":
	main()