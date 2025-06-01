import xml.etree.ElementTree as ET
from database_manager import DatabaseManager
from convertor import Convertor

class QuestsLoader:
    @staticmethod
    def loadQuests(filepath):
        numberOFInserts = 0
        numberOFSkkips = 0
        db = DatabaseManager()
        db.connectToDatabase(dbName="gamedata", username="game_admin", password="1919")

        try:
            tree = ET.parse(filepath)
            root = tree.getroot()
        except Exception as e:
            print(f"[ERROR] failed to parse XML: {e}")
            return

        for quest in root.findall("quête"):
            try:
                name = quest.find("Nom").text.strip()
                xp = Convertor.convertToInt(quest.find("Expérience").text)
                difficulty = Convertor.convertToInt(quest.find("Difficulté").text)

                descriptionTag = quest.find("Descripion") # Descripion IS A TYPO IN THE XML BY THE TEACHER
                                                          # BUT NECESSSARY TO HERE TO RETRIEVE THE DESCRIPTION
                if descriptionTag is not None and descriptionTag.text is not None:
                    description = descriptionTag.text.strip()
                else:
                    description = "No description available"

                rewards = quest.find("Récompenses")
                money = 0

                objects = []


                if rewards is not None:
                    gold = rewards.find("Or")
                    if gold is not None:
                        money = Convertor.convertToInt(gold.text)

                        objectsTag = rewards.findall("Objets")

                        for tag in objectsTag:
                            if tag.text:
                                objects.append(tag.text.strip())


                if not name or xp is None or difficulty is None or money is None:
                    print(f"[WARNING] : [QUESTS] invalid values detected for quest '{name}' — skipping ...")
                    numberOFSkkips += 1
                    continue
                
                request = """
                    INSERT INTO quest (name, xp, difficulty, money, description)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (name) DO NOTHING
                """
                db.execute(request=request, values=(name, xp, difficulty, money, description))
                db.commit()
                # LINKING TO quest_object
                for obj in objects:
                    db.execute("SELECT name FROM object WHERE name = %s LIMIT 1", (obj,))
                    if db.cursor.fetchone(): # ca EXSITE ALORS car le resultat est valide
                        newRequest = """
                                    INSERT INTO quest_object (quest_name, object_name)
                                    VALUES (%s, %s)
                                    ON CONFLICT DO NOTHING
                                     """
                        db.execute(request=newRequest, values=(name, obj))
                db.commit()
                numberOFInserts += 1
            except Exception as e:
                print(f"[ERROR] failed to insert quest: {e}")
                db.rollback()
                numberOFSkkips += 1

        print(f"[REQUESTS SUMMARY] : QUESTS -> {numberOFInserts} INSERTED | {numberOFSkkips} SKIPPED")
        db.close()


