from data import tables
from sqlite3 import connect

with connect("database.db") as con: 
    cur = con.cursor()
    
    for name, headers in tables.items():

        cmd = f"""create table {name}(
            {",".join([chr(65 + i) for i in range(len(headers))])}
        );"""

        cur.execute(cmd)
    con.commit()