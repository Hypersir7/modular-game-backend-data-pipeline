import xml.etree.ElementTree as EM
from database_manager import DatabaseManager
from convertor import Convertor


class MonstersLoader:
    @staticmethod
    def loadMonsters(filepath):
        numberOFInserts = 0
        numberOFSkkips = 0
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
                if monster.find("nom") is not None:
                    name = monster.find("nom").text.strip()
                else:
                    name = None
                health = Convertor.treeConvertInt(monster, "vie")
                attack = Convertor.treeConvertInt(monster, "attaque")
                defense = Convertor.treeConvertInt(monster, "defense")

                money = 0
                probability = 0

                drops = monster.find("drops")
                if drops is not None:
                    goldTag = drops.find("Or")
                    if goldTag is not None:
                        money = Convertor.convertToInt(goldTag.find("nombre").text)
                        probability = Convertor.convertToInt(goldTag.find("probabilité").text)

                if not name or any(x is None for x in [health, attack, defense]):
                    print(f"[WARNING] missing/corrupted data for monster: {name}")
                    numberOFSkkips += 1
                    continue

                request = """
                    INSERT INTO monster (name, health, attack, defense, money, probability)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (name) DO NOTHING
                """
                db.execute(request=request, values=(name, health, attack, defense, money, probability))
                db.commit()
                # LINKING Monster drops to the database
                # RETRIEVE MONSTER ID TO WORK WITH IT
                db.execute("""
                    SELECT id FROM monster WHERE name = %s
                """, (name,))
                result = db.fetchData()
                if not result:
                    print(f"[ERROR] could not retrieve ID for monster: {name}")
                    continue
                monsterID = result[0]["id"]

                if drops is not None:
                    for drop in drops:
                        tag = drop.tag.strip()
                        if tag.lower() == "or":
                            continue  # GOLD ALREADY HANDLED AVOVE
                        try:
                            objectName = tag.replace("_", " ")  # ex: Potion_de_Super en Potion de Super
                            objectProbTag = drop.find("probabilité")
                            if objectProbTag is None:
                                print(f"[WARNING] No probabilité for object {objectName} → skipping")
                                continue

                            objectProb = Convertor.convertToInt(objectProbTag.text.strip())

                            db.execute("SELECT name FROM object WHERE name = %s", (objectName,))
                            result = db.fetchData()
                            if not result:
                                print(f"[WARNING] object '{objectName}' not found in 'object' table → skipping.")
                                continue

                            # LINKING TO monster_object
                            db.execute("""
                                INSERT INTO monster_object (monster_id, object_name, probability)
                                VALUES (%s, %s, %s)
                                ON CONFLICT DO NOTHING
                            """, (monsterID, objectName, objectProb))
                        except Exception as e:
                            print(f"[ERROR] failed to insert drop '{tag}' for monster '{name}': {e}")
                numberOFInserts += 1
                # print(f"Inserted monster: {name}")
            except Exception as e:
                print(f"[ERROR] failed to insert monster {name} into database : {e}")
                db.rollback()
        print(f"[REQUESTS SUMMARY] : MONSTERS -> {numberOFInserts} INSERTED | {numberOFSkkips} SKIPPED")
        db.close()
