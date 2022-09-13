from sqlite3 import connect
from data import tables
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import pypandoc 

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
    df = pd.DataFrame(data, columns = keys)
    df.to_csv(path)

def update(table_name, col, dict):
    x = dict['v1']
    y = dict['v2']
    col = chr(65 + tables[table_name].index(col))

    with connect('database.db') as con:
        cur = con.cursor()
        cmds = [
            f"update {table_name} set {col} = 'temp' where {col} = '{x}';", 
            f"update {table_name} set {col} = '{x}'  where {col} = '{y}';",
            f"update {table_name} set {col} = '{y}' where {col} = 'temp';",
        ]
        for cmd in cmds:
            cur.execute(cmd) 
        con.commit() 


def pdf_generate():
    root ='static/files/csv/download.csv'
    path = 'static/files/pdf/download.pdf'

    """df = pd.read_csv(root)
    html_string = df.to_html()

    path_wkhtmltopdf = r'D:\Softwares\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

    pdfkit.from_string(html_string, path)
    config = pdfkit.configuration(wkhtmltopdf='/path/to/wkhtmltopdf')
    pdfkit.from_file(root, path, configuration=config )"""

    output = pypandoc.convert_file(root, 'pdf', outputfile=path)
    assert output == ""
