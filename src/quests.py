import psycopg2


TOP10GOLD = """

"""


def get_from_database(quest: str):
    conn = psycopg2.connect(
        dbname="gamedata",
        user="game_admin",
        password="your_password",
        host="localhost"
    )
    cur = conn.cursor()

    cur.execute(quest)
    res = cur.fetchall()
    cur.close()
    conn.close()
    return res
