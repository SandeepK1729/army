battle_board_table = {
    'columns' : [
        "SER", 
        "REC VEH", 
        "BA NO / REGD NO", 
        "LOC",
        "CDR", 
        "MOB NO CDR", 
        "GROUPING", 
        "PRESENT TASK", 
        "EXPECTED TIME OF COMPLETION", 
        "REMARKS"
    ], 
    'search_column' : 0,
}
record_of_work = {
    'columns' : [
        "SER NO",
        "REGN NO", 
        "UNIT", 
        "LOC OF CAS", 
        "TIME REPORTED", 
        "TIME REC VEH REPORTED", 
        "TIME COMPLETED", 
        "CL", 
        "CAS DISPOSAL", 
        "IF UNRECOVERED, REPORTED TO", 
        "REMARKS"
    ], 
    'search_column' : 0,
}
repair_state = {
    'columns' : [
        "SER",
        "DATE IN", 
        "BA NO/REGD NO",
        "MAKE & TYPE OF EQPT", 
        "NATURE OF DEFECT", 
        "REPAIR ACTIVITY", 
        "NOMENCLATURE",	
        "QTY USED", 
        "DATE OUT", 
"REMARKS",
    ], 
    'search_column' : 0,
}
rec_state = {
    'columns' : [
        "S NO",
        "DATE", 
        "UNIT, REG/DBA NO MAKE & TYPE OF CAS", 
        "TIME INFO RECD BY REC", 
        "INFO RECD BY (TELE/RADIO/SIG/COURSE)", 
        "TIME RECOVERY VEH REACHED SITE OF REC", 
        "TIME REQD FOR REC(HRS)", 
        "MANPOWER EQPT TRADEWISE", 
        "NO & TYPE OF REC VEHS USED", 
        "CAS REPAIRED AFTER REC(YES/NO)" ,
        "DETAILS OF SPARES FITTED IN CAS", 
        "SIT REP RAISED(YES/NO)(SIT REP NO, IF RAISED)", 
        "REMARKS"
    ], 
    'search_column' : 0,
}
vor_eoa_state = {
    'columns' : [
        "SER", 
        "DATE IN", 
        "BA NO/ REGD NO", 
        "MAKE & TYPE", 
        "NATURE OF DEFECT", 
        "MUA DEMANDED", 
        "PRESENT STATE", 
        "REMARKS"
    ], 
    'search_column' : 0,
}
recurring_fault_db = {
    'columns' : [
        "SER", 
        "MAKE & TYPE OF EQPT", 
        "FAULT OBSERVED", 
        "SYSTEM", 
        "NO OF INCIDENCE", 
        "PROBABLE REASON", 
        "ACTION TAKEN", 
        "REMARKS"
    ], 
    'search_column' : 0,
}
dets = {
    'columns' : [
        "DET NAME",
        'DET TYPE',
        'VEHICLE TYPE',
        'LANGITUDE', 
        'LATITUDE',
        "ARMY NO", 
        "DATE",
        "RANK", 
        "NAME", 
        "TRADE",
        "MOB NO",
        "REMARKS",
    ], 
    'search_column' : 2,
    #'primary_key' : 1,
}
spares = {
    'columns' : [
        'DET NAME',
        'NAME OF SPARE', 
        'SECTION NO', 
        'CAT PART NO', 
        'QTY', 
    ], 
    'search_column' : 3,
    'primary_key' : 3,
}
tables = { 
    "battle_board" : battle_board_table, 
    "record_of_work" : record_of_work, 
    "repair_state" : repair_state,
    "rec_state" : rec_state, 
    "vor_eoa_state" : vor_eoa_state, 
    "recurring_fault_db" : recurring_fault_db,
    "dets" : dets,
    'spares' : spares,
}
type = { 
    "REC VEH" : 'number', 
    "SER" : 'number',
    "UNIT" : 'number', 
    'DET TYPE' : 'select',
    'SER NO' : 'text',
    'QTY' : 'number',
    'CAT PART NO' : 'text',
}
def get_type(name, production = False):
    
    Opts = {'select' : 'text', 'number' : 'integer'}
    
    if name not in type:
        if "DATE" in name:
            return "date"
    
        if "NO" in name:
            return "integer" if production else "number"

        return "text"

    c_type = type[name]
    return Opts[c_type] if production and c_type in Opts else c_type