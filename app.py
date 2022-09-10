from flask import Flask, request, render_template, send_file, session, redirect
from lib import *
from flask_session import Session  
from data import tables 

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

@app.route("/")
def home():
    user = session.get("name", "newbie")
    if user == "newbie":
        return redirect("/login")
    if user != "admin":
        return "Your Not Admin"
    return render_template("home.html")

@app.route("/<name>", methods = ("POST", "GET"))
def battle_board(name):
    user = session.get("name", "newbie")
    if user == "newbie":
        return redirect("/login")
    if user != "admin":
        return "Your Not Admin"
    
    if name not in tables:
        print(name)
        return redirect("/")

    headers = tables[name]

    if request.method == "POST":
        delete_key = request.form.get("DELETE", -1)
        if delete_key != -1:
            remove(name, headers[0], delete_key)
        else:
            add(name, headers, request.form)

    data = load(name, headers[0], request.form.get('search', ''))
    return render_template(
        "table.html",
        table = data, 
        headers = headers, 
        title = " ".join(name.split("_")), 
        name = name,
    )

@app.route("/download/<name>")
def download_file(name):
    user = session.get("name", "newbie")
    if user == "newbie":
        return redirect("/login")
    if user != "admin":
        return "Your Not Admin"
    
    if name not in tables:
        return redirect("/")

    table = tables[name]
    headers = list(table.keys())
    n = len(table[headers[0]])

    file = []
    for i in range(n):
        row = {}
        for header in headers:
            row[header] = table[header][i]
        file.append(row)
    
    with open('static/files/download.csv', 'w') as csvfile:
        writer = DictWriter(csvfile, fieldnames = headers)
        writer.writeheader()
        writer.writerows(file)
    
    return send_file(
        'static/files/download.csv', 
        as_attachment = True, 
        mimetype='text/csv', 
        download_name = f"{name}.csv"
    )

@app.route("/battle_map")
def battle_map():
    user = session.get("name", "newbie")
    if user == "newbie":
        return redirect("/login")
    if user != "admin":
        return "Your Not Admin"
    
    return render_template("battle_map.html")

@app.route("/tfc_control_map")
def tfc_control_map():
    user = session.get("name", "newbie")
    if user == "newbie":
        return redirect("/login")
    if user != "admin":
        return "Your Not Admin"
    
    return render_template("tfc_control_map.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

if __name__ == "__main__":
    app.run(debug = True)