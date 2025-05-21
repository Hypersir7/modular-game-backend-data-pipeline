import csv
from database_manager import DatabaseManager
from convertor import Convertor

class ObjectsLoader:
	@staticmethod
	def loadObjects(filepath):
		db = DatabaseManager()
		db.connectToDatabase(dbName="gamedata", username="game_admin", password="1919")

		with open(filepath, newline="", encoding="utf-8") as file:
			data = csv.DictReader(file)

			for row in data:                
				try:
					name = row["Nom"]
					objectType = row["Type"]
					objectPropertie = row["Propriétés"]
					price = Convertor.convertToInt(row["Prix"])
					
					if(not name or not objectType or not objectPropertie or price is None):
						print(f"[WARNING] invalid values detected ! skipping line ...")
						continue
						
					if(price < 0):
						print(f"[WARNING] negative price detected ! skipping line ...")
						continue
		
					request = """ 
					          INSERT INTO object (name, type, property, price)
					          VALUES (%s, %s, %s, %s)
					          """
					db.execute(request=request, values=(name, objectType, objectPropertie, price))
					db.commit()
					print(f"Inserted object: {name}")

				except Exception as e:
					print(f"[ERROR] failed to insert object into database :{name} -> {e}")
					db.rollback()
		
		db.close()
