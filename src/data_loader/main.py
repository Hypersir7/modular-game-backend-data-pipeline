import psycopg2
from psycopg2.extras import RealDictCursor

from database_manager import DatabaseManager

from modules.players import PlayersLoader

def main():
	dbManager = DatabaseManager()

	dbManager.connectToDatabase(dbName="gamedata", username="game_admin", password="1919")

	pLoader = PlayersLoader()
	pLoader.loadPlayers(r"/home/astr0/Desktop/Blocus 2/Projects/H303/data/joueurs.csv")

	try:
		request = "SELECT * from player;"
		dbManager.execute(request=request)
		data = dbManager.cursor.fetchall()
		print("[RESULT] RETRIEVED DATA : ")
		for row in data:
			print(row)
	except Exception as e:
		print(f"[ERROR] could not retrieve data! : {e}")
		dbManager.rollback();


if __name__ == "__main__":
	main()