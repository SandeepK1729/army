from sqlite3 import connect
from data import get_type, tables,choices
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
        cmd = f"""
        
            INSERT INTO {table_name}({",".join([chr(65 + tables[table_name]['columns'].index(key)) for key in keys])}) 
            VALUES({",".join([f"{cast_type(key, dict[key])}" for key in keys])});
            
            """
        print(cmd)
        cur.execute(cmd)
        print( cmd, "\n\n\n")
        con.commit()
        
def special_update(table_name, dict, primes = -1):
    table = tables[table_name]
    with connect('database.db') as con:
        cur = con.cursor()
        
        cmd  = f"""
                UPDATE {table_name} 
                SET A = '{dict['DET NAME']}', E = {dict["QTY"]}
                WHERE ZZZ = {dict['UPDATE_SPARE_DATA']};
            """
        cur.execute(cmd)
        
        con.commit()
        
def load(table_name, keys = "", value = "", search_col = -1):
    """
        def load(table_name, key, value):
    """
    table = tables[table_name]
    key = chr((table['search_column'] if search_col == -1 else search_col)  + 65)
    keys = [chr(65 + table['columns'].index(key)) for key in keys]
    key_name = table['columns'][table['search_column']]

    with connect('database.db') as con:
        cmd = f'SELECT { ",".join(["ZZZ"] + keys)} FROM {table_name}'
        if value != "":
            cmd += f" WHERE {key}"
            
            if get_type(key_name) == "number":
                cmd += f" = {cast_type(key_name, value)}"
            else :
                cmd += f" LIKE '%{value}%'"
            
        cmd += ';'
        print(cmd)
        
        path = 'static/files/csv/download.csv'
        df = pd.DataFrame(pd.read_sql_query(cmd, con), columns=keys)
        
        df.to_csv(path)
        cur = con.cursor()
        cur.execute(cmd)
        return cur.fetchall()

def special_load(table_name, keys = "", value = ""):
    """
        def load(table_name, key, value):
    """
    table = tables[table_name]
    key = chr(table['search_column'] + 65)
    keys = [chr(65 + table['columns'].index(key)) for key in keys]
    key_name = table['columns'][table['search_column']]
    
    with connect('database.db') as con:
        cur = con.cursor()
        cmd = f"SELECT ZZZ,B,C,D,SUM(E) AS E FROM {table_name}" 
        if value != "":
            cmd += f" WHERE {key}"
            if get_type(key_name) == "number":
                cmd += f" = {cast_type(key_name, value)[0]}"
            else :
                cmd += f" LIKE '%{value}%'"
            
        cmd += ' GROUP BY D;'
        
        path = 'static/files/csv/download.csv'
        df = pd.DataFrame(pd.read_sql_query(cmd, con), columns=keys)
        df.to_csv(path)
        cur.execute(cmd)
        print(cmd)
        x = cur.fetchall()
        return x

def remove(table_name, prime_key, key_no = -1):
    """
        def remove(table_name, key, value):
    """
    
    if key_no != -1:
        key = chr(65 + key_no)
        value = cast_type(tables[table_name]['columns'][key_no], prime_key)
    else:
        key = "ZZZ"
        value = prime_key

    with connect('database.db') as con:
        cur = con.cursor()
        cmd = f"DELETE FROM {table_name} WHERE {key}={value};"
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

def transfer(table_name, dict):
    transfer_qty = int(dict['TRANSFER QTY'])
    keys = tables[table_name]['columns']
    with connect('database.db') as con:
        cur = con.cursor()
    
        # extracting primary key
        cmd = f"""
                SELECT E, ZZZ from Spares 
                WHERE A = '{dict['DET NAME']}'
                AND
                D = '{dict['CAT PART NO']}';
            """
        cur.execute(cmd)
        print(cmd)

        previous_qty, e = cur.fetchone()
        print(f" p qu : {previous_qty}, {e}")
        # reducing from previous
        cmd  = f"""
                    UPDATE {table_name} 
                    SET E = {previous_qty - transfer_qty}
                    WHERE ZZZ = {e};
                """
        con.commit()
        print(cmd)
        cur.execute(cmd)
        # adding for new det 
        cmd = f"""
            SELECT E, ZZZ from spares
            WHERE A = '{dict["TRANSFER DET NAME"]}'
            AND
            D = '{dict['CAT PART NO']}';
        """
        print(cmd)
        cur.execute(cmd)

        x = cur.fetchone()
        print(x)
        
        re = {}
        re['QTY'] = transfer_qty
        re["DET NAME"] = dict["TRANSFER DET NAME"]
        re['CAT PART NO'] = dict['CAT PART NO']
        re['SECTION NO'] = dict['SECTION NO']
        re['NAME OF SPARE'] = dict['NAME OF SPARE']

        if x is None:
            print(re)
            
            cmd = f"""
            
                INSERT INTO {table_name}({",".join([chr(65 + tables[table_name]['columns'].index(key)) for key in keys])}) 
                VALUES({",".join([f"{cast_type(key, re[key])}" for key in keys])});
                
                """
            cur.execute(cmd)
            
        else:
            new_qty, e = x
            cmd  = f"""
                    UPDATE {table_name} 
                    SET E = {new_qty + transfer_qty}
                    WHERE ZZZ = {e};
                """
            cur.execute(cmd)
            print(cmd)
        con.commit()
    
def all_dets():
    with connect('database.db') as con:
        cur = con.cursor()
        try:
            cmd = f"""
                SELECT DISTINCT A FROM dets;
                """
            cur.execute(cmd)
            x = [i for i, *j in cur.fetchall()]
            choices['DET NAME'] = x
        except:
            pass