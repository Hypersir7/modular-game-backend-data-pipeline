import psycopg2
from psycopg2.extras import RealDictCursor

# DatabaseManager class is used to manage the connection to a PostgreSQL database.
# It provides methods to connect to the database, execute queries, commit requests, and close the connection.
# It also provides a rollback method to rollback transactions in case of errors.

class DatabaseManager:

    LOCALHOST = 'localhost'
    PORT = 5432 # PostgreSQL port

    def __init__(self, host = LOCALHOST, port = PORT) -> None:
        self.LOCALHOST = host
        self.PORT = port
        self.connection = None
        self.cursor = None
        self.connected = False

    def connectToDatabase(self, dbName, username, password):
        try:
            self.connection = psycopg2.connect(
                    dbname = dbName,
                    user = username, 
                    password = password,
                    host = self.LOCALHOST, 
                    port = self.PORT,
                )
            
            self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            self.connected = True
            print(f"[INFO] Connected to database: {dbName} as {username} !")

        except Exception as e:
            print(f"[ERROR] connection to database: {dbName} failed!")
            print(f"ERROR TYPE : {e} ")

    def execute(self, request, values = None):
        try:
            if self.cursor is None:
                raise Exception("[ERROR] No database cursor : call 'connectToDatabase()' to initalize it!")

            if values is not None:
                self.cursor.execute(request, values)
            else: # values = None
                self.cursor.execute(request)
        except Exception as e:
            print("[ERROR] could not execute!")
            print(f"ERROR TYPE : {e} ")
            print(f"Request : {request}")
            if values is not None:
                print(f"Values: {values}")
            self.rollback()

    def commit(self):
        try:
            self.connection.commit()
        except Exception as e:
            print(e)

    def close(self):
        try:
            if self.cursor is not None:
                self.cursor.close()
            if self.connection is not None:
                self.connection.close()
            
            self.connected = False
            
            print("[INFO] database was closed!")
        except Exception as e:
            print("[ERROR] could not close database!")
            print(f"ERROR TYPE : {e} ")

    def rollback(self):
            try:
                if self.connection is not None:
                    self.connection.rollback()
                    print("[INFO] transaction rolled back")
            except Exception as e:
                print("[ERROR] could not rollback transaction!")
                print(f"ERROR TYPE : {e}")

    def fetchData(self):
        try:
            if self.cursor is None:
                raise Exception("[ERROR] No database cursor : call 'connectToDatabase()' to initalize it!")
            if self.cursor.description is not None:
                data = self.cursor.fetchall()
                print(data)
                return data
            else:
                return []
        except Exception as e:
            print("[ERROR] could not fetch data!")
            print(f"ERROR TYPE : {e} ")
            self.rollback()
            return None

    def displayFetchedData(self, data):
        if data is None:
            print("[ERROR] No data to display!")
            return

        for row in data:
            print(dict(row))
        print("[INFO] data displayed successfully!")

    def isConnected(self):
        return self.connected
    
    def __del__(self):
        if self.connected:
            self.close()
            print("[INFO] database was closed!")
                   
        self.connected = False
        self.cursor = None
        self.connection = None
        print("[INFO] database manager was deleted!")