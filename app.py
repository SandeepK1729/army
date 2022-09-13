from flask import Flask, request, render_template, send_file, session, redirect
from lib import *
from flask_session import Session  
from data import tables 
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

@app.route('/avt_lr')
@app.route('/avt_fr')
@app.route('/mrt')
def conncec():
    name = list(request.path.split('/'))[-1]
    headers = tables[name]['columns']

    if request.method == "POST":
        add(table_name = name, keys = headers, dict = request.form)

    data = load(
        table_name = name,
        value = request.args.get('search', '')
    )
    return render_template(
        "table.html",
        table = data, 
        headers = headers, 
        title = " ".join(name.split("_")).upper(), 
        name = name,
        update_form = (name == "spares")
    )

@app.route("/")
@login_required
def home():
    return render_template("home.html")

@app.route("/<name>", methods = ("POST", "GET"))
@login_required
def tables_db(name):
    headers = tables[name]['columns']

    if request.method == "POST":
        add(table_name = name, keys = headers, dict = request.form)

    data = load(
        table_name = name,
        value = request.args.get('search', '')
    )
    return render_template(
        "table.html",
        table = data, 
        headers = headers, 
        title = " ".join(name.split("_")).upper(), 
        name = name,
        update_form = (name == "spares")
    )

@app.route('/<name>/delete', methods = ("POST", "GET"))
@login_required
def delete_rec(name):
    remove(
        table_name = name, 
        value = request.form.get("DELETE", -1)
    )
    root = list(request.path.split('/'))[1]
    return redirect(f'/{root}')

@app.route("/update", methods = ("POST", "GET"))
@login_required
def cat_pat(name = "spares"):
    if name not in tables:
        print(name)
        return redirect("/")

    headers = tables[name]['columns']

    if request.method == "POST":
        update(table_name = name, col = 'CAT PART NO', dict = request.form)
    return redirect(f'/{name}')

@app.route("/download/<name>")
@login_required
def download_file(name):
    if name not in tables:
        return redirect("/")

    path = 'static/files/csv/download.csv'
    csv_generate(name)

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
    
    csv_generate(name)
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