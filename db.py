from data import tables, get_type
from sqlite3 import connect

with connect("database.db") as con: 
    cur = con.cursor()
    
    for name, table in tables.items():
        keys = list(range(len(table['columns'])))
        
        print(f"    table {name} is creating ...", end = ' ')
        cmd = f"""create table {name}(
            ZZZ INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            {",".join([chr(65 + i) + " " + get_type(table['columns'][i], True)  for i in keys])}
        );"""
        
        cur.execute(cmd)
        print("OK")
        
    con.commit()