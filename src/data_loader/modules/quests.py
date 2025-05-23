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

                descriptionTag = quest.find("Description")
                if descriptionTag is not None and descriptionTag.text is not None:
                    description = descriptionTag.text.strip()
                else:
                    description = "No description available"

                rewards = quest.find("Récompenses")
                money = 0
                if rewards is not None:
                    gold = rewards.find("Or")
                    if gold is not None:
                        money = Convertor.convertToInt(gold.text)

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
                numberOFInserts += 1
            except Exception as e:
                print(f"[ERROR] failed to insert quest: {e}")
                db.rollback()
                numberOFSkkips += 1

        print(f"[REQUESTS SUMMARY] : QUESTS -> {numberOFInserts} INSERTED | {numberOFSkkips} SKIPPED")
        db.close()


