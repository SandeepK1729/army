from sqlite3 import connect

with connect("database.db") as con: 
    cur = con.cursor()
    cur.execute("CREATE TABLE battle_board( 
            
        );")