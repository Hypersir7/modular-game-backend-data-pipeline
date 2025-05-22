import json
from database_manager import DatabaseManager
from convertor import Convertor

class CharactersLoader:
    @staticmethod
    def loadCharacters(filepath):
        numberOFInserts = 0
        numberOFSkkips = 0
        db = DatabaseManager()
        db.connectToDatabase(dbName="gamedata", username="game_admin", password="1919")

        try:
            with open(filepath, encoding="utf-8") as file:
                data = json.load(file)
        except Exception as e:
            print(f"[ERROR] failed to load JSON file: {e}")
            return
        
        for character in data.get("personnages", []):
            try:
                name = character.get("Nom")
                characterClass = character.get("Classe")
                health = Convertor.convertToInt(character.get("Vie"))
                mana = Convertor.convertToInt(character.get("Mana"))
                force = Convertor.convertToInt(character.get("Force"))
                intelligence = Convertor.convertToInt(character.get("Intelligence"))
                agility = Convertor.convertToInt(character.get("Agilite"))
                username = character.get("utilisateur")

                if not name or not characterClass or not username:
                    print(f"[WARNING] : [CHARACTERS] invalid values detected ! skipping character insertion ...")
                    numberOFSkkips += 1
                    continue
                
                if health is None or mana is None or force is None or intelligence is None or agility is None:
                    print(f"[WARNING] : [CHARACTERS] invalid values detected ! skipping character insertion ...")
                    numberOFSkkips += 1
                    continue
                if health < 0 or mana < 0 or force < 0 or intelligence < 0 or agility < 0:
                    print(f"[WARNING] : [CHARACTERS] invalid negative values detected ! skipping character insertion ...")
                    numberOFSkkips += 1
                    continue
                request = """
                          INSERT INTO character (name, class, health, mana, strength, intelligence, agility, username)
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                          ON CONFLICT (name) DO NOTHING
                          """
                db.execute(request=request, values=(name, characterClass, health, mana, force, intelligence, agility, username))
                db.commit()
                numberOFInserts += 1
                #print(f"Inserted character: {name}")
            
            except Exception as e:
                print(f"[ERROR] failed to insert character data: {e}")
                db.rollback()
        print(f"[REQUESTS SUMMARY] : CHARACTERS -> {numberOFInserts} INSERTED | {numberOFSkkips} SKIPPED")
        db.close()