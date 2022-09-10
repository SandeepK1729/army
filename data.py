battle_board_table = [
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
]
record_of_work = [
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
]
repair_state = [
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
]
rec_state = [
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
]
vor_eoa_state = [
    "SER", 
    "DATE IN", 
    "BA NO/ REGD NO", 
    "MAKE & TYPE", 
    "NATURE OF DEFECT", 
    "MUA DEMANDED", 
    "PRESENT STATE", 
    "REMARKS"
]
recurring_fault_db = [
    "SER", 
    "MAKE & TYPE OF EQPT", 
    "FAULT OBSERVED", 
    "SYSTEM", 
    "NO OF INCIDENCE", 
    "PROBABLE REASON", 
    "ACTION TAKEN", 
    "REMARKS"
]
avr_lr = [
    "ARMY NO", 
    "RANK", 
    "NAME", 
    "TRADE", 
    "MOB NO", 
    "REMARKS",
]
tables = { 
    "battle_board" : battle_board_table, 
    "record_of_work" : record_of_work, 
    "repair_state" : repair_state,
    "rec_state" : rec_state, 
    "vor_eoa_state" : vor_eoa_state, 
    "recurring_fault_db" : recurring_fault_db,
    "avt_lr" : avr_lr,
}
