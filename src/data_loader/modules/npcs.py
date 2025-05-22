import json
from database_manager import DatabaseManager
from convertor import Convertor


class NpcsLoader:
    @staticmethod
    def loadNpcs(filePath: str) -> None:
        numberOFInserts = 0
        numberOFSkkips = 0

        dbManager = DatabaseManager()
        dbManager.connectToDatabase(dbName="gamedata", username="game_admin", password="1919")

        try:
            with open(filePath, encoding="utf-8") as file:
                data = json.load(file)
        except Exception as e:
            print(f"[ERROR] failed to load JSON file: {e}")
            return

        for npc in data.get("PNJs", []):
            try:
                name = npc.get("Nom")
                dialogue = npc.get("Dialogue")

                if not name or not dialogue:
                    # print(f"[WARNING] : [NPCS] invalid values detected ! skipping NPC insertion ...")
                    numberOFSkkips += 1
                    continue

                # INSERTING NPC DATA
                request = """
                          INSERT INTO pnjs (name, dialogue)
                          VALUES (%s, %s)
                          ON CONFLICT (name) DO NOTHING
                          """
                dbManager.execute(request=request, values=(name, dialogue))
                dbManager.commit()
                numberOFInserts += 1

                # LINKING TO pnjs_quest

                for quest in npc.get("Quêtes",[]):
                    formattedQuest = quest.split("[")[0].strip()
                    dbManager.execute("SELECT name FROM quest WHERE name = %s LIMIT 1", (formattedQuest,))
                    # Check if the quest exists
                    if dbManager.cursor.fetchone(): # CHECKS FIRST RESULT OF THE QUERY 
                        request = """
                                INSERT INTO pnjs_quest (pnj_name, quest_name)
                                VALUES (%s, %s)
                                ON CONFLICT DO NOTHING
                                """
                        dbManager.execute(request=request, values=(name, formattedQuest))

                    else:
                        # print(f"[WARNING] : [NPCS] quest '{formattedQuest}' does not exist in the database. Skipping ...")
                        numberOFSkkips += 1

                for object in npc.get("Inventaire", []):
                    dbManager.execute("SELECT name FROM object WHERE name = %s LIMIT 1", (object,))
                    if dbManager.cursor.fetchone():
                        # Check if the object exists
                        request = """
                                INSERT INTO pnjs_object (pnj_name, object_name)
                                VALUES (%s, %s)
                                ON CONFLICT DO NOTHING
                                """
                        dbManager.execute(request=request, values=(name, object))
                    
                    else:
                        # print(f"[WARNING] : [NPCS] object '{object}' does not exist in the database. Skipping ...")
                        numberOFSkkips += 1
                dbManager.commit()
            except Exception as e:
                print(f"[ERROR] failed to insert NPC data: {e}")
                dbManager.rollback()
                numberOFSkkips += 1
        print(f"[REQUESTS SUMMARY] : NPCS -> {numberOFInserts} INSERTED | {numberOFSkkips} SKIPPED")
        dbManager.close()
