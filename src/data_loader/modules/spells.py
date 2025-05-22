import csv
from database_manager import DatabaseManager
from convertor import Convertor


class SpellsLoader:
    @staticmethod
    def loadSpells(filepath):
        numberOFInserts = 0
        numberOFSkkips = 0
        db = DatabaseManager()
        db.connectToDatabase(dbName="gamedata", username="game_admin", password="1919")

        with open(filepath, newline="", encoding="utf-8") as file:
            data = csv.DictReader(file)

            for row in data:
                try:
                    name = row["Nom"]
                    manaCost = Convertor.convertToInt(row["Coût en Mana"])
                    chargingTime = Convertor.convertToInt(row["Temps de Recharge"])
                    attackingPower = Convertor.convertToInt(row["Puissance d'Attaque"])                  

                    if not name or manaCost is None or chargingTime is None or attackingPower is None:
                        print(f"[WARNING] : [SPELLS] invalid values detected ! skipping line ...")
                        numberOFSkkips += 1
                        continue

                    if manaCost < 0 or chargingTime < 0 or attackingPower < 0:
                        print(f"[WARNING] : [SPELLS] negative values detected ! skipping line ...")
                        numberOFSkkips += 1
                        continue

                    request = """
                              INSERT INTO spell (name, mana_cost, charge_time, attack_power)
                              VALUES (%s, %s, %s, %s)
                              """
                    db.execute(request=request, values=(name, manaCost, chargingTime, attackingPower))
                    db.commit()
                    numberOFInserts += 1
                    #print(f"Inserted spell: {name}")

                except Exception as e:
                    print(f"[ERROR] failed to insert spell into database :{name} -> {e}")
                    db.rollback()
        print(f"[REQUESTS SUMMARY] : SPELLS -> {numberOFInserts} INSERTED | {numberOFSkkips} SKIPPED")
        db.close()
