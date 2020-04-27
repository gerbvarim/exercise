from exc_checking.gerber_file import *

from flask import session
        
#########exc1 specific code######################### 
def does_circles_overlap(center1, center2, r1, r2):
    return point_diff_by2(center1, center2) < r1**2 + r2**2

def does_squares_overlap(center1, center2, l1, l2):
    #l1, l2 is the side length of a square
    if abs(center1[0] - center2[0]) > (l1 + l2) / 2:
        return False
    if abs(center1[1] - center2[1]) > (l1 + l2) / 2:
        return False
    return True

def does_square_circle_overlap(center1, center2, l1, r2):
    """
    solution would be based on the bounding circle of the square, and on the bounding square of the circle.
    we will check if the real square overlaps with the bounding square, 
    and than we will check if the bounding square overlaps with the real square.
    
    because the bounding shapes are larger than the actual shapes, 
    it is obvious that if the actual shapes will overlap the bounding circle will overlap with the real circle, 
    and the bounding rectangle will overlap with the real rectangle.
    
    apperentely the only case where the real circle and the bounded circle could falsely overlap,
    is the case where the distance on x_axis or y_axis is larger than r2+l1/2.
    this case would never overlap between the real square and the bounding square,
    so it should be safe to say that if both the real circle and bounding circle overlaps and the real square and the bounding square overlaps,
    than the real square and the actual square overlaps.
    """
    if not(does_circles_overlap(center1, center2, l1 * 2**0.5, r2)):
        #check if bounding circle overlaps real circle
        return False
    if not(does_squares_overlap(center1, center2, l1, 2*r2) ):
        #check if bounding square overlaps real square
        return False
    return True
    
    
def passed_exc1():
    try:
        gerber_file = GerberFile("upload_folder/sol_"+session['username']+".txt")
        resulted_aps = gerber_file.process_aps_with_connection()
        if not(len(resulted_aps) == 5):#check 5 shapes, as instructed
            return ""
        square_l = 0.3 * 10**5 #side length of squares
        circle_r = (0.3 * 10**5) / 2 #radius of circles
        for ap in resulted_aps:
            if not( ap.type == 11 or ap.type == 12):
                return " : illegal shape type"
            if ap.type == 11:#ap is one of the 2 circles
                if not( len(ap.ap_connected_to) == 2):
                    return " : wrong amount fo connected circles"
                for ap_connected in ap.ap_connected_to:
                    if not( ap_connected.type == 11): #check circles are only connected to circles
                        return " : illegal connection of circle to non-circle"
            if ap.type == 12:#ap is one of the 3 squares
                if not( len(ap.ap_connected_to) == 3):
                    return " : wrong amount of connected squares"
                for ap_connected in ap.ap_connected_to:
                    if not( ap_connected.type == 12): #check squares are only connected to squares
                        return " : illegal connection of square to non-circle"
            #check shape overlapping
            for ap2 in resulted_aps:
                if ap2 != ap:
                    if ap.type == 11: #if ap circle
                        if ap2.type == 11:
                            if does_circles_overlap(ap.location, ap2.location, circle_r, circle_r):
                                return " : shapes overllap"
                        else:
                            if does_square_circle_overlap(ap2.location, ap.location, square_l, circle_r):
                                return " : shapes overllap"               
                    else: #if ap square
                        if ap2.type == 11:
                            if does_square_circle_overlap(ap.location, ap2.location, square_l, circle_r):
                                return " : shapes overllap"
                        else:
                            if does_squares_overlap(ap2.location, ap.location, square_l, square_l):
                                return " : shapes overllap"               
        return None   
    except Exception:
        return ""
    

#########exc2 specific code#########################       
def passed_exc2():
    try:
        correct_res = open("exc_checking/sol2.txt","r").read().split()
        user_res = open("upload_folder/sol_" + session['username'] + ".txt", "r").read().split()
        for ind in range(len(correct_res)):
            if correct_res[ind] != user_res[ind]:
                return ""
        return None
    except Exception:
        return ""
        
#########exc3 specific code#########################       
def passed_exc3():
    try:
        correct_res = open("exc_checking/sol3.txt","r").read().split("\n")
        user_res = open("upload_folder/sol_" + session['username'] + ".txt", "r").read().split("\n")
        for ind in range(len(correct_res)):
            if correct_res[ind].split() != user_res[ind].split():
                return ": error in section" + str(ind + 1)
        return None
    except Exception:
        return ""
        
#########exc4 specific code######################### 
def passed_exc4():
    try:
        correct_res = open("exc_checking/sol4.txt","r").read().split("\n")
        user_res = open("upload_folder/sol_" + session['username'] + ".txt", "r").read().split("\n")
        if len(correct_res) != len(user_res):
            return ": incorrect amount of pins"
        if correct_res != user_res:
            return ": incorrect pin locations"
        return None
    except Exception:
        return ""
           
#########exc5 specific code######################### 
def get_canonic_sol5_rep(sol5_lines):
    """
    get a solution for exc4 and return a canonic single form of this solution.
    the idea is that the test shouldn't take into consideration the nets order or the order of points inside the net.
    """
    result = []
    for line in sol5_lines:
        result.append([])
        line_nums = line.split()
        for ind in range(0, len(line_nums), 2):
            result[-1].append( (line_nums[ind], line_nums[ind + 1]) )#add points as a tipple
        result[-1].sort()#sort the points in the net
    result.sort()#sort the nets
    return result
      
def passed_exc5():
    try:
        correct_res = open("exc_checking/sol5.txt","r").read().split("\n")
        user_res = open("upload_folder/sol_" + session['username'] + ".txt", "r").read().split("\n")
        if correct_res[0].split()[0] != user_res[0].split()[0]:#check num nets is the correct one in a space-immune check
            return ": incorrect amount of nets"
        correct_res = correct_res[1::]#remove first line. it is already tested.
        user_res = user_res[1::]
        if get_canonic_sol5_rep(correct_res) == get_canonic_sol5_rep(user_res):
            return None
        else:
            return ": incorrect nets"
    except Exception:
        return ""
  
    