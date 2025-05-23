import psycopg2


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

# Didn't do this query yet...

MOSTCOMMONITEMTYPELVL5 = """
"""

MONSTERHIGHESTREWARD = """
SELECT name, health, money
FROM monster
ORDER BY money DESC, health DESC
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
