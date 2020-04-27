import random

def draw_curve(start_point, end_point, missing_ind=-1):
    """
    draw a neptune2_like cure connecting between pins on the different fpgas.
    """
    result = "X"+str(start_point[0]) +"Y"+str(start_point[1])+"D02*\n"
    result += "D14*\n"
    result += "D03*\n"
    result += "D22*\n"
    start_cir_loc = (int((end_point[0] - start_point[0]) / 4  ), start_point[1]  ) # initial line
    result += "X"+str(start_cir_loc[0]) +"Y"+str(start_cir_loc[1])+"D01*\n"
    mid_point =  (int((end_point[0] + start_point[0]) / 2  ), int((end_point[1] + start_point[1]) / 2  )  ) # mid_point
    dist_to_mid_point = (mid_point[0] - start_cir_loc[0], mid_point[1] - start_cir_loc[1])
    #rising circ
    num_cir_lines = 120
    for ind in range(num_cir_lines):
        x = int(start_cir_loc[0] + ind * dist_to_mid_point[0] / num_cir_lines)
        x_normalized_dist = (x - start_cir_loc[0]) / dist_to_mid_point[0]
        y = mid_point[1] - int(dist_to_mid_point[1]* (1 -  (x_normalized_dist)**2  ) ** 0.5)
        if ind == missing_ind:
            x_btoken = int(start_cir_loc[0] + (ind-0.225) * dist_to_mid_point[0] / num_cir_lines)
            result += "X"+str(x_btoken) +"Y"+str(y)+"D01*\n"
        else:
            result += "X"+str(x) +"Y"+str(y)+"D01*\n"
        result += "X"+str(x) +"Y"+str(y)+"D02*\n"
    result += "X"+str(mid_point[0]) +"Y"+str(mid_point[1])+"D01*\n"#draw to mid point
    
    
    end_cir_loc = (int(3 * (end_point[0] - start_point[0]) / 4  ), end_point[1]  )
    dist_to_end_cir = (end_cir_loc[0] - mid_point[0], end_cir_loc[1] - mid_point[1])
    for ind in range(num_cir_lines):
        x = int(mid_point[0] + ind * dist_to_end_cir[0] / num_cir_lines)
        x_normalized_dist = (x - mid_point[0]) / dist_to_end_cir[0]
        y = mid_point[1] + int(dist_to_end_cir[1]* (1 -  (1 - x_normalized_dist)**2  ) ** 0.5)
        result += "X"+str(x) +"Y"+str(y)+"D01*\n"
        result += "X"+str(x) +"Y"+str(y)+"D02*\n"
    result += "X"+str(end_point[0]) +"Y"+str(end_point[1])+"D01*\n"
    result += "D14*\n"
    result += "D03*\n"
    return result
    

if __name__=="__main__":
    result_file = "%FSLAX34Y34*%\n"
    result_file += "%MOMM*%\n"
    result_file += "%ADD14C,0.5*%\n"
    result_file += "%ADD22C,0.025*%\n" #smaller 3 times than the one in neptune2, in order to allow smaller disconnection

        
    #(169, 54)-<(98,42)
    x_dis = 70 * 10**4
    y_dis = 12 * 10**4
    num_pins = 128
    
    y_jump = int(y_dis / 8)
    start_loc = (0, 0)
    curve_string_list = []
    broken_connection_indexs= [19, 57, 76, 111]
    magic_disconnection_idex_that_looks_well = int(17*16/5)
    for ind in range(num_pins):
        curve_string_list.append(draw_curve(start_loc, (start_loc[0] + x_dis, start_loc[1] + y_dis),  
            magic_disconnection_idex_that_looks_well if ind in broken_connection_indexs else -1))
        start_loc = (start_loc[0], start_loc[1] + y_jump)
    random.shuffle(curve_string_list)
    for string in curve_string_list:
        result_file += string
    result_file += "M02*"
    open("gerb_res", "w").write(result_file)