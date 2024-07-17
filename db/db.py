import sqlite3
def makedb():
    conn = sqlite3.connect("./db/results.db")
    c=conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS game(
            gameid integer PRIMARY KEY AUTOINCREMENT,
            cho TEXT,
            han TEXT,
            moves integer,
            result TEXT,
            variant integer,
            record TEXT
            )""")
    conn.commit()
    conn.close()

def add_game(cho,han,moves,result,variant,record):
    conn = sqlite3.connect("./db/results.db")
    c=conn.cursor()
    c.execute("INSERT INTO game VALUES (null,?,?,?,?,?,?)",(cho,han,moves,result,variant,record))
    conn.commit()
    conn.close()

def game_count():
    conn = sqlite3.connect("./db/results.db")
    c=conn.cursor()
    c.execute("SELECT gameid FROM game")
    games=c.fetchall()
    return len(games)

def get_cho(id:int):
    conn = sqlite3.connect("./db/results.db")
    c=conn.cursor()
    c.execute(f"SELECT cho FROM game WHERE gameid={id}")
    cho=c.fetchone()[0]
    return cho

def get_han(id:int):
    conn = sqlite3.connect("./db/results.db")
    c=conn.cursor()
    c.execute(f"SELECT han FROM game WHERE gameid={id}")
    han=c.fetchone()[0]
    return han

def get_moves(id:int):
    conn = sqlite3.connect("./db/results.db")
    c=conn.cursor()
    c.execute(f"SELECT moves FROM game WHERE gameid={id}")
    moves=c.fetchone()[0]
    return moves

def get_result(id:int):
    conn = sqlite3.connect("./db/results.db")
    c=conn.cursor()
    c.execute(f"SELECT result FROM game WHERE gameid={id}")
    result=c.fetchone()[0]
    return result

def get_record(id:int):
    conn = sqlite3.connect("./db/results.db")
    c=conn.cursor()
    c.execute(f"SELECT variant,record FROM game WHERE gameid={id}")
    record=c.fetchone()
    return record