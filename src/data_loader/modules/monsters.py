import xml.etree.ElementTree as EM

from database_manager import DatabaseManager
from convertor import Convertor

class MonstersLoader:
    @staticmethod
    def loadMonsters(filepath):
        db = DatabaseManager()
        db.connectToDatabase(dbName="gamedata", username="game_admin", password="1919")

        try:
            tree = EM.parse(filepath)
            root = tree.getroot()
        except Exception as e:
            print(f"[ERROR] failed to parse XML file: {filepath} -> {e}")
            return

        for monster in root.findall("monstre"):
            try:
                monsterId = Convertor.convertToInt(monster.find("id").text)
                name = monster.find("nom").text
                health = Convertor.convertToInt(monster.find("vie").text)
                attack = Convertor.convertToInt(monster.find("attaque").text)
                defense = Convertor.convertToInt(monster.find("defense").text)
                
                money  = 0
                probability = 0

                drops = monster.find("drops")
                if drops is not None:
                    goldTag = drops.find("Or")

                    if(goldTag is not None):
                        money = Convertor.convertToInt(goldTag.find("nombre").text)
                        probability = Convertor.convertToInt(goldTag.find("probabilité").text)

                if name is None or health is None or attack is None or defense is None:
                    print(f"[ERROR] missing data for monster: {monsterId}")
                    continue

                request = """
                          INSERT INTO monster (id, name, health, attack, defense, money, probability)
                          VALUES (%s, %s, %s, %s, %s, %s, %s)
                          """
                db.execute(request=request, values=(monsterId, name, health, attack, defense, money, probability))
                db.commit()
                print(f"Inserted monster: {name}")

            except Exception as e:
                print(f"[ERROR] failed to insert monster into database :{name} -> {e}")
                db.rollback()

        db.close()
