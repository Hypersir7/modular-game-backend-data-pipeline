from data_loader.database_manager import DatabaseManager


# ====================== COMMUNICATING AND GETTING DATA FROM THE DATABASE ======================
class Requests:

    # ====================== REQUETSTS ======================
    TOP10GOLD = """ 
    SELECT username, money
    FROM player
    ORDER BY money DESC
    LIMIT 10;
    """

    PLAYERMOSTCHARCLASS = """
    SELECT username, class, COUNT(*) AS nb_characters
    FROM character
    GROUP BY username, class
    ORDER BY nb_characters DESC
    LIMIT 1;
    """

    BESTREWARDPERLVL = """
    SELECT name, difficulty, money
    FROM quest q1
    WHERE money = (
        SELECT MAX(money)
        FROM quest q2
        WHERE q1.difficulty = q2.difficulty
        )
    ORDER BY difficulty;
    """

    NPCMOSTGOLD = """
    SELECT p.pnj_name, SUM(o.price) AS total_value
    FROM pnjs_object p
    JOIN object o ON p.object_name = o.name
    GROUP BY p.pnj_name
    ORDER BY total_value DESC
    LIMIT 1;
    """

    MOSTCOMMONITEMTYPELVL5 = """
    SELECT o.type, COUNT(*) AS count
    FROM quest q
    JOIN pnjs_quest pq ON q.name = pq.quest_name
    JOIN pnjs_object po ON pq.pnj_name = po.pnj_name
    JOIN object o ON po.object_name = o.name
    WHERE q.difficulty = 5
    GROUP BY o.type
    ORDER BY count DESC
    LIMIT 1;
    """

    MONSTERHIGHESTREWARD = """
    SELECT name, health, money
    FROM monster
    ORDER BY money DESC, health DESC
    """
    def __init__(self):
        self.db = DatabaseManager()
        self.db.connectToDatabase(dbName="gamedata", username="game_admin", password="1919")

    def sendRequestsToDB(self, request: str, values, requestName: str):
        # EXECUTE UNE REQUETE SQL EN TOUTE SECURITE ET EFFICACITE
        try:
            if self.db.isConnected():
                self.db.execute(request, values)
                return self.db.fetchData()
            else:
                print(f"[ERROR] : database is not connected for '{requestName}' query.")
                return None
        except Exception as e:
            print(f"[ERROR] : failed to execute '{requestName}' query: {e}")
            return None

    def commit_transactions(self):
        self.db.commit()

    def getTop10Gold(self):
        return self.sendRequestsToDB(self.TOP10GOLD, None, "Top10Gold")

    def getPlayerMostCharClass(self):
        return self.sendRequestsToDB(self.PLAYERMOSTCHARCLASS, None, "PlayerMostCharClass")

    def getBestRewardPerLvl(self):
        return self.sendRequestsToDB(self.BESTREWARDPERLVL, None, "BestRewardPerLvl")

    def getNpcMostGold(self):
        return self.sendRequestsToDB(self.NPCMOSTGOLD, None, "NpcMostGold")

    def getMostCommonItemTypeLvl5(self):
        return self.sendRequestsToDB(self.MOSTCOMMONITEMTYPELVL5, None, "MostCommonItemTypeLvl5")

    def getMonsterHighestReward(self):
        return self.sendRequestsToDB(self.MONSTERHIGHESTREWARD, None, "MonsterHighestReward")
