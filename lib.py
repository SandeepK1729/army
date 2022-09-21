from sqlite3 import connect
from data import get_type, tables
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import pypandoc 
import pandasql as ps

def cast_type(key, value):
    return value if get_type(key) == "number" else f"'{value}'"
    
def add(table_name, keys, dict):    
    """
        def add(table_name, keys, dict):
    """

    with connect('database.db') as con:
        cur = con.cursor()
        try:
            cmd = f"""
            
                INSERT INTO {table_name}({",".join([chr(65 + tables[table_name]['columns'].index(key)) for key in keys])}) 
                VALUES({",".join([f"{cast_type(key, dict[key])}" for key in keys])});
                
                """
            print(cmd)
            print(cur.execute(cmd))
            con.commit()
        except:
            return f"{keys[0]} must be unique"

def special_update(table_name, dict, primes = -1):
    table = tables[table_name]
    cols = table['columns']
    primes = [table['columns'][table.get('primary_key', 0)]] if primes == -1 else primes
    
    data = []
    for i in range(len(cols)):
        if cols[i] in dict:
            data.append(f"{chr(i + 65)} = {cast_type(cols[i], dict[cols[i]])}")
    print(dict)
    
    with connect('database.db') as con:
        cur = con.cursor()
        try:
            cmd = f"""
                    SELECT ZZZ from {table_name} 
                    WHERE A {f"= '{dict['UPDATE_SPARE_DATA']}'" if dict['UPDATE_SPARE_DATA'] != 'None' else "IS NULL"}
                    AND
                    D = '{dict['CAT PART NO']}';
                """
            cur.execute(cmd)
            
            e = cur.fetchone()
            cmd  = f"""
                    UPDATE {table_name} 
                    SET {", ".join(data)}
                    WHERE ZZZ = {e[0]};
                """
            
            con.commit()
        except Exception as e:
            print(e)
            return "null"

def load(table_name, keys = "", value = ""):
    """
        def load(table_name, key, value):
    """
    table = tables[table_name]
    key = chr(table['search_column'] + 65)
    keys = [chr(65 + table['columns'].index(key)) for key in keys]
    key_name = table['columns'][table['search_column']]

    with connect('database.db') as con:
        cmd = f'SELECT { ",".join(keys)} FROM {table_name}'
        if value != "":
            cmd += f" WHERE {key}"
            
            if get_type(key_name) == "number":
                cmd += f" = {cast_type(key_name, value)[0]}"
            else :
                cmd += f" LIKE '%{value}%'"
            
        cmd += ';'
        print(cmd)
        
        path = 'static/files/csv/download.csv'
        df = pd.DataFrame(pd.read_sql_query(cmd, con), columns=keys)
        print(keys)
        df.to_csv(path)
    
        return df.values.tolist()

def special_load(table_name, keys = "", value = ""):
    """
        def load(table_name, key, value):
    """
    table = tables[table_name]
    key = chr(table['search_column'] + 65)
    keys = [chr(65 + table['columns'].index(key)) for key in keys]
    
    with connect('database.db') as con:
        cur = con.cursor()
        cmd = f"SELECT B,C,D,SUM(E) AS E FROM {table_name}" 
        if value != "":
            cmd += f" WHERE {key} LIKE '%{value}%'"
        cmd += ' GROUP BY B;'
        print(cmd)
        
        path = 'static/files/csv/download.csv'
        df = pd.DataFrame(pd.read_sql_query(cmd, con), columns=keys)
        df.to_csv(path)
    
        return df.values.tolist()

def remove(table_name, values, keys = -1):
    """
        def remove(table_name, key, value):
    """
    table = tables[table_name]
    cols = table['columns']

    idxs = table.get('primary_key', 0) if keys == -1 else keys
    
    with connect('database.db') as con:
        cur = con.cursor()
        cmd = f"DELETE FROM {table_name} WHERE "
            
        if "list" in str(type(values)) or "tuple" in str(type(values)):
            cmd += " AND ".join(f"{chr(idx + 65)} = {cast_type(cols[idx], value)}" for idx, value in zip(idxs, values))
        else:
            cmd += f"{chr(65 + idxs)} = {cast_type(cols[idxs], values)}"
        
        cmd += ';'

        print(cmd)
        cur.execute(cmd)
        con.commit()

def update(table_name, col, dict):
    x = dict['v1']
    y = dict['v2']
    col = chr(65 + tables[table_name]['columns'].index(col))

    with connect('database.db') as con:
        cur = con.cursor()
        cmds = [
            #f"update {table_name} set {col} = 'temp' where {col} = '{x}';", 
            f"update {table_name} set {col} = '{x}'  where {col} = '{y}';",
            #f"update {table_name} set {col} = '{y}' where {col} = 'temp';",
        ]
        for cmd in cmds:
            print(cmd)
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
