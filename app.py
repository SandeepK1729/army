from flask import Flask, request, render_template, send_file, session, redirect
from csv import DictReader, DictWriter
from flask_session import Session

app = Flask(__name__)

# session config
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
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

battle_board_table = {
    "SER" : [], 
    "REC VEH" : [], 
    "BA NO/ REGD NO" : [], 
    "LOC" : [],
    "CDR" : [], 
    "MOB NO CDR" : [], 
    "GROUPING" : [], 
    "PRESENT TASK" : [] , 
    "EXPECTED TIME OF COMPLETION" : [], 
    "REMARKS" : []
} 
record_of_work = {
    "SER NO" : [],
    "REGN NO" : [], 
    "UNIT" : [], 
    "LOC OF CAS" : [], 
    "TIME REPORTED" : [], 
    "TIME REC VEH REPORTED" : [], 
    "TIME COMPLETED" : [], 
    "CL" : [], 
    "CAS DISPOSAL" : [], 
    "IF UNRECOVERED, REPORTED TO" : [], 
    "REMARKS" : []
}
repair_state = {
    "SER" : [],
    "DATE IN" : [], 
    "BA NO/REGD NO" : [],
    "MAKE & TYPE OF EQPT" : [], 
    "NATURE OF DEFECT" : [], 
    "REPAIR ACTIVITY" : [], 
    "NOMENCLATURE": [],	
    "QTY USED" : [], 
    "DATE OUT" : [], 
    "REMARKS" : [],
}
rec_state = {
    "S NO" : [],
    "DATE" : [], 
    "UNIT, REG/DBA NO MAKE & TYPE OF CAS" : [], 
    "TIME INFO RECD BY REC" : [], 
    "INFO RECD BY (TELE/RADIO/SIG/COURSE)" : [], 
    "TIME RECOVERY VEH REACHED SITE OF REC" : [], 
    "TIME REQD FOR REC(HRS)" : [], 
    "MANPOWER EQPT TRADEWISE" : [], 
    "NO & TYPE OF REC VEHS USED" : [], 
    "CAS REPAIRED AFTER REC(YES/NO)" : [] ,
    "DETAILS OF SPARES FITTED IN CAS" : [], 
    "SIT REP RAISED(YES/NO)(SIT REP NO, IF RAISED)" : [], 
    "REMARKS" : []
}
vor_eoa_state = {
    "SER" : [], 
    "DATE IN" : [], 
    "BA NO/ REGD NO" : [], 
    "MAKE & TYPE" : [], 
    "NATURE OF DEFECT" : [], 
    "MUA DEMANDED" : [], 
    "PRESENT STATE" : [], 
    "REMARKS" : []
}
recurring_fault_db = {
    "SER" : [], 
    "MAKE & TYPE OF EQPT" : [], 
    "FAULT OBSERVED" : [], 
    "SYSTEM" : [], 
    "NO OF INCIDENCE" : [], 
    "PROBABLE REASON" : [], 
    "ACTION TAKEN" : [], 
    "REMARKS" : []
}
tables = { 
    "battle_board" : battle_board_table, 
    "record_of_work" : record_of_work, 
    "repair_state" : repair_state,
    "rec_state" : rec_state, 
    "vor_eoa_state" : vor_eoa_state, 
    "recurring_fault_db" : recurring_fault_db, 
}
@app.route("/<name>", methods = ("POST", "GET"))
def battle_board(name):
    user = session.get("name", "newbie")
    if user == "newbie":
        return redirect("/login")
    if user != "admin":
        return "Your Not Admin"
    
    table = tables[name]
    headers = list(table.keys())

    if request.method == "POST":
        delete_key = int(request.form.get("DELETE", -1))
        if delete_key != -1:
            for header in headers:
                table[header].pop(delete_key) 
        else:
            for header in headers:
                table[header].append(request.form.get(header))

    return render_template(
        "table.html",
        table = table,  
        headers = headers, 
        n = len(table[headers[0]]), 
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