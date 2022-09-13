from data import tables
from sqlite3 import connect

with connect("database.db") as con: 
    cur = con.cursor()
    
    for name, table in tables.items():
        n = len(table['columns'])
        cmd = f"""create table {name}(
            A PRIMARY KEY NOT NULL, 
            {",".join([chr(66 + i) + " TEXT NOT NULL" for i in range(n - 1)])}
        );"""

        cur.execute(cmd)
    con.commit()