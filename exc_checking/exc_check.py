import sys
sys.path.append("./exc_checking")

from gerber_file import *
from flask import session
        
#########exc1 specific code#########################       
def passed_exc1():
    gerber_file = GerberFile("upload_folder/sol_"+session['username']+".txt")
    resulted_aps = gerber_file.process_aps_with_connection()
    if not(len(resulted_aps) == 5):#check 5 shapes, as instructed
        return False
    for ap in resulted_aps:
        if not( ap.type == 11 or ap.type == 12):
            return False
        if ap.type == 11:#ap is one of the 2 circles
            if not( len(ap.ap_connected_to) == 2):
                return False
            for ap_connected in ap.ap_connected_to:
                if not( ap_connected.type == 11): #check circles are only connected to circles
                    return False
        if ap.type == 12:#ap is one of the 3 squares
            if not( len(ap.ap_connected_to) == 3):
                return False
            for ap_connected in ap.ap_connected_to:
                if not( ap_connected.type == 12): #check squares are only connected to squares
                    return False
    return True   

#########exc2 specific code#########################       
def passed_exc2():
    return False #TODO: implement test logic later
        
#########exc3 specific code#########################       
def passed_exc3():
    return False #TODO: implement test logic later
           
#########exc4 specific code#########################       
def passed_exc4():
    return False #TODO: implement test logic later

test_func_list = [passed_exc1, passed_exc2, passed_exc3, passed_exc4]
  
    