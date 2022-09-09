from flask import Flask, request, render_template, send_file, session, redirect
from csv import DictReader, DictWriter
from flask_session import Session

app = Flask(__name__)

# session config
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

globeOne = '1234'

def login_required(func):
    def modified_func():
        user = session.get("name", "newbie")
        if user == "newbie":
            return redirect("/login")
        if user != "admin":
            return "Your Not Admin"
        
        return func
    return modified_func

@app.route("/login")
@login_required
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if password == globeOne:
            session['name'] = username
    return render_template("login.html")

@app.route("/")
@login_required
def home():
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
@login_required
def battle_board(name):
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
@login_required
def download_file(name):
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
@login_required
def battle_map():
    return render_template("battle_map.html")

@app.route("/tfc_control_map")
@login_required
def tfc_control_map():
    return render_template("tfc_control_map.html")

if __name__ == "__main__":
    app.run(debug = True)