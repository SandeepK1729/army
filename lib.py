from sqlite3 import connect

def add(table_name, keys, dict):
    """
        def add(table_name, keys, dict):
    """
    data = [
        str(dict[key]) for key in keys
    ]
    print(data)
    with connect('database.db') as con:
        cur = con.cursor()
        cmd = f"""INSERT INTO {table_name} VALUES('{"','".join(data)}');"""
        cur.execute(cmd)
        con.commit()

def load(table_name, key, value):
    """
        def load(table_name, key, value):
    """
    with connect('database.db') as con:
        cur = con.cursor()
        cmd = f"SELECT * FROM {table_name}" 
        if value != "":
            cmd += f"WHERE {key} LIKE '%{value}%';"
        cur.execute(cmd)
        
        return cur.fetchall()

def remove(table_name, key, value):
    """
        def remove(table_name, key, value):
    """
    with connect('database.db') as con:
        cur = con.cursor()
        cmd = f"""DELETE FROM {table_name} WHERE A = '{value}';"""
        con.commit()