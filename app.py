from flask import Flask, request, render_template, send_file, session, redirect
from lib import *
from flask_session import Session  
from data import get_type, tables, choices
from functools import wraps

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = 'filesystem'
Session(app)

globeOne = '1234'

@app.route("/login", methods = ("POST", "GET"))
def login():
    
    if request.method == "POST":
        print("hello")
        username = request.form.get("username")
        password = request.form.get("password")
        if password == globeOne and username == "admin":
            session['name'] = username
            return redirect("/")
        else:
            return render_template("login.html", message = "Either username or password are wrong")
    return render_template("login.html")

@app.route('/logout')
def logout():
    session['name'] = 'newbie'
    return redirect('/')

def login_required(func):
    @wraps(func)
    def m_func(*args, **kwargs):
        user = session.get("name", "newbie")
        if user == "newbie":
            return redirect("/login")
        if user != "admin":
            return "Your Not Admin"
        return func(*args, **kwargs)

    return m_func 

@app.route("/")
@login_required
def home():
    return render_template("home.html")

@app.route('/dets', methods = ["PUT", "GET", "POST"])
@login_required
def dets(name = "dets"):
    headers_all = tables[name]['columns']
    headers = headers_all[:6]
    
    if request.method == "POST":
        if "ADD" in request.form:
            add(table_name = name, keys = headers_all, dict = request.form)
        if "DELETE" in request.form:
            remove(
                table_name = name, 
                prime_key = request.form.get("DELETE", -1),
                key_no = 1
            )
    data = load(
        table_name = name,
        keys = headers,
        value = request.args.get('search', '')
    )
    if len(data) == 0:
        return redirect("/dets")
    
    return render_template(
        "dets.html",
        table = data, 
        choices = choices,
        headers = ["ZZZ"] + [(name, get_type(name)) for name in headers], 
        headers_all = [(name, get_type(name)) for name in headers_all], 
        
        title = " ".join(name.split("_")).upper(), 
        name = name,
        search_key = request.args.get("search", "")
    )

@app.route('/dets/<id>', methods = ["GET", "POST"])
@login_required
def det_view(id):
    name = "dets"
    headers = tables[name]['columns']
    print(request.method, request.form)
    if "ADD" in request.form:
        print("adding ..")
        add(table_name = name, keys = headers, dict = request.form)
    if "DELETE" in request.form:
        remove(
            table_name = name, 
            prime_key = request.form.get("DELETE", -1)
        )
    
    data = load(
        table_name = name,
        keys = headers,
        value = id
    )

    return render_template(
        "persons.html",
        table = data, 
        headers = [(name, get_type(name)) for name in headers], 
        
        title = " ".join(name.split("_")).upper(), 
        name = name,
        search_key = request.args.get("search", "")
    )

@app.route('/spares', methods = ["PUT", "GET", "POST"])
@login_required
def spares():
    name = list(request.path.split('/'))[-1]
    headers = tables[name]['columns'][1:]
    headers_all = headers + ['DET NAME']
    all_dets()

    if request.method == "POST":
        if "ADD" in request.form:
            add(table_name = name, keys = headers_all, dict = request.form)
            print("adding ...")
        if "SADD" in request.form:
            add(table_name = name, keys = tables[name]['columns'], dict = request.form)
            print("Spare Adding ...")
        if "UPDATE_SPARE_DATA" in request.form:
            special_update(name, request.form, primes = ('CAT PART NO', 'DET NAME'))
            print("updating spares ...")
        if "DELETE" in request.form:
            remove(
                name, 
                request.form.get("DELETE"),
                abnorm = "NON_PRIME_DELETE" not in request.form
            )
            print("delete spares ...")
        if "TRANSFER" in request.form:
            transfer(table_name = name, dict = request.form)
            print("transfer spares ..")
    data = special_load(
        table_name = name,
        keys = headers,
        value = request.args.get('search', '')
    )
    
    if request.method == "POST" and "show_spare" in request.form:
        print("hell")
        name_of_spare = request.form.get("NAME OF SPARE")
        cat_part_no = request.form.get("CAT PART NO")
        section_no = request.form.get("SECTION NO")

        headers2 = ["DET NAME", "QTY"]
        data2 = load(
            table_name = name, 
            keys = headers2,
            value = cat_part_no
        )
        return render_template(
            "spares.html",
            table = data, 
            headers = [(name, get_type(name)) for name in headers],
            headers_all = [(name, get_type(name)) for name in headers_all],
            choices = choices, 
            
            table2 = data2,
            headers2 = [(name, get_type(name)) for name in headers2], 
            name_of_spare = name_of_spare,
            cat_part_no = cat_part_no,
            section_no = section_no,

            title = " ".join(name.split("_")).upper(), 
            name = name,
            search_key = request.args.get("search", "")
        )
    
    return render_template(
        "spares.html",
        table = data, 
        headers = [(name, get_type(name)) for name in headers], 
        choices = choices, 
        headers_all = [(name, get_type(name)) for name in headers_all],
        
        title = " ".join(name.split("_")).upper(), 
        name = name,
        search_key = request.args.get("search", "")
    )

@app.route("/battle_board", methods = ["PUT", "GET", "POST"])
@app.route("/record_of_work", methods = ["PUT", "GET", "POST"])
@app.route("/repair_state", methods = ["PUT", "GET", "POST"])
@app.route("/rec_state", methods = ["PUT", "GET", "POST"])
@app.route("/vor_eoa_state", methods = ["PUT", "GET", "POST"])
@app.route("/recurring_fault_db", methods = ["PUT", "GET", "POST"])
@login_required
def tables_db():
    name = list(request.path.split('/'))[-1]
    headers = tables[name]['columns']
    
    if request.method == "POST":
        if "ADD" in request.form:
            add(table_name = name, keys = headers, dict = request.form)
        if "DELETE" in request.form:
            remove(
                table_name = name, 
                prime_key = request.form.get("DELETE", -1)
            )
    
    
    data = load(
        table_name = name,
        keys = headers,
        value = request.args.get('search', '')
    )
    print(data)
    
    return render_template(
        "table.html",
        table = data, 
        headers = [(name, get_type(name)) for name in headers], 
        title = " ".join(name.split("_")).upper(), 
        name = name,
        choices = choices,
        update_form = (name == "spares"),
        search_key = request.args.get("search", "")
    )

@app.route("/download/<name>")
@login_required
def download_file(name):
    if name not in tables:
        return redirect("/")

    path = 'static/files/csv/download.csv'
    
    return send_file(
        path, 
        as_attachment = True, 
        mimetype='text/csv', 
        download_name = f"{name}.csv"
    )

@app.route("/print/<name>")
@login_required
def print_file(name):
    if name not in tables:
        return redirect("/")
    
    path = 'static/files/pdf/download.pdf'
    pdf_generate()

    return send_file(
        path, 
        as_attachment = True, 
        mimetype='text/pdf', 
        download_name = f"{name}.pdf"
    )

@app.route("/<name>_map")
@login_required
def battle_map(name):
    return render_template("map.html", name = (" ".join(name.split('_')).upper() + " MAP"))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

if __name__ == "__main__":
    app.run(debug = True)