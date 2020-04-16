import sys
sys.path.append("./exc_checking")

from gerber_file import *
from flask import session
        
#########exc1 specific code#########################       
def passed_exc1():
    try:
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
    except Exception:
        return False
    

#########exc2 specific code#########################       
def passed_exc2():
    try:
        correct_res = open("exc_checking/sol2.txt","r").read().split()
        user_res = open("upload_folder/sol_" + session['username'] + ".txt", "r").read().split()
        for ind in range(len(correct_res)):
            if correct_res[ind] != user_res[ind]:
                return False
        return True
    except Exception:
        return False
        
#########exc3 specific code#########################       
def passed_exc3():
    try:
        correct_res = open("exc_checking/sol3.txt","r").read().split()
        user_res = open("upload_folder/sol_" + session['username'] + ".txt", "r").read().split()
        for ind in range(len(correct_res)):
            if correct_res[ind] != user_res[ind]:
                return False
        return True
    except Exception:
        return False
           
#########exc4 specific code######################### 
def get_canonic_sol4_rep(sol4_lines):
    """
    get a solution for exc4 and return a canonic single form of this solution.
    the idea is that the test shouldn't take into consideration the nets order or the order of points inside the net.
    """
    result = []
    for line in sol4_lines:
        result.append([])
        line_nums = line.split()
        for ind in range(0, len(line_nums), 2):
            result[-1].append( (line_nums[ind], line_nums[ind + 1]) )#add points as a tipple
        result[-1].sort()#sort the points in the net
    result.sort()#sort the nets
    return result
      
def passed_exc4():
    try:
        correct_res = open("exc_checking/sol4.txt","r").read().split("\n")
        user_res = open("upload_folder/sol_" + session['username'] + ".txt", "r").read().split("\n")
        if correct_res[0].split()[0] != user_res[0].split()[0]:#check num nets is the correct one in a space-immune check
            return False
        correct_res = correct_res[1::]#remove first line. it is already tested.
        user_res = user_res[1::]
        return get_canonic_sol4_rep(correct_res) == get_canonic_sol4_rep(user_res)
    except Exception:
        return False
  
    