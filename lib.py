from sqlite3 import connect
from data import tables
import pandas as pd
#import pdfkit

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
        try:
            cmd = f"""INSERT INTO {table_name} VALUES({",".join([
                f"'{value}'" for value in data])});"""
            print(cmd)
            cur.execute(cmd)
            con.commit()
        except:
            return f"{keys[0]} must be unique"

def load(table_name, value = "", key = 'A'):
    """
        def load(table_name, key, value):
    """
    with connect('database.db') as con:
        cur = con.cursor()
        cmd = f"SELECT * FROM {table_name}" 
        if value != "":
            cmd += f" WHERE {key} LIKE '%{value}%';"
        cur.execute(cmd)
        
        return cur.fetchall()

def remove(table_name, value, key = 'A'):
    """
        def remove(table_name, key, value):
    """
    with connect('database.db') as con:
        cur = con.cursor()
        cmd = f"""DELETE FROM {table_name} WHERE {key} = '{value}';"""
        print(cmd)
        cur.execute(cmd)
        con.commit()

def csv_generate(name):
    path = 'static/files/csv/download.csv'
    keys = tables[name]
    data = load(table_name = name)
    with open(path, 'w') as file:
        file.write(",".join([f'"{key}"' for key in keys]) + '\n')
        for row in data:
            file.write(",".join(row) + '\n')
        
"""def pdf_generate():
    root ='static/files/csv/download.csv'
    path = 'static/files/pdf/download.pdf'

    df = pd.read_csv(root)
    html_string = df.to_html()
    pdfkit.from_string(html_string, path )
    """