

from database_manager import DatabaseManager  
TOP10_GOLD_QUERY = """
    SELECT ....
    FROM ....
    ORDER ...
    LIMIT 10;
"""

db = DatabaseManager()


db.connectToDatabase("gamedata", "game_admin", "your_password")

db.execute(TOP10_GOLD_QUERY)


data = db.fetchData()

db.displayFetchedData(data)

db.close() # c'est meme automatiquement fait via le destructeu