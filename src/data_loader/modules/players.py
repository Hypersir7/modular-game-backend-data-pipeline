import csv
from database_manager import DatabaseManager
from convertor import Convertor

class PlayersLoader:
	@staticmethod
	def loadPlayers(filepath):
		numberOFInserts = 0
		numberOFSkkips = 0
		db = DatabaseManager()
		db.connectToDatabase(dbName="gamedata", username="game_admin", password="1919")

		with open(filepath, newline="", encoding="utf-8") as file:
			data = csv.DictReader(file)

			for row in data:
				try:
					# id = int(row["ID"]) -> pas d'ID car la database genre un automatiquement
					# sinon rique de conflit de cle primaire car dans joueurs.csv il y a plusieur IDs identiques
					playerName = row["NomUtilisateur"]
					level = Convertor.convertToInt(row["Niveau"])
					xp = Convertor.convertToInt(row["XP"])
					money = Convertor.convertToInt(row["Monnaie"])
					slots = Convertor.convertToInt(row["SlotsInventaire"])


					if(level is None or xp is None or money is None or slots is None):
						print(f"[WARNING] : [PLAYERS] invalide values detected ! skipping line ...")
						numberOFSkkips += 1
						continue

					if(level < 0 or xp < 0 or money < 0 or slots < 0):
						print(f"[WARNING] : [PLAYERS] negative values detected ! skipping line ...")
						numberOFSkkips += 1
						continue
					request = """
					          INSERT INTO player (username, level, xp, money, inventory_slots)
					          VALUES (%s, %s, %s, %s, %s)
							  ON CONFLICT (username) DO NOTHING
					          """
					db.execute(request=request, values= (playerName, level, xp, money, slots))
					db.commit()
					numberOFInserts += 1
					# print(f"Inserted player: {playerName}")

				except Exception as e:
					print(f"[ERROR] failed to load player into database : {e}")
					db.rollback();
		print(f"[REQUESTS SUMMARY] : PLAYERS -> {numberOFInserts} INSERTED | {numberOFSkkips} SKIPPED")
		db.close()