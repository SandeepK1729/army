from data import tables, get_type
from sqlite3 import connect

check = lambda x : x != "spares"

with connect("database.db") as con: 
    cur = con.cursor()
    
    for name, table in tables.items():
        re = check(name)
        keys = list(range(len(table['columns'])))
        if re:
            prime_key = keys.pop(table.get('primary_key', 0))
        
        print(f"    table {name} is creating ...", end = ' ')
        cmd = f"""create table {name}(
            {chr(65 + prime_key) if re else "ZZZ INTEGER"} NOT NULL PRIMARY KEY {"AUTOINCREMENT" if not re else ""},
            {",".join([chr(65 + i) + " " + get_type(table['columns'][i], True)  for i in keys])}
        );"""
        
        cur.execute(cmd)
        print("OK")
        
    con.commit()