import os
from flask import Flask, flash, request, redirect, url_for, send_file, session
#from werkzeug.utils import secure_filename
from data_base_wrapper import *
from jinja2 import Template

UPLOAD_FOLDER = 'upload_folder/'
NUM_ECXS = 4
USER_MAX_ALLOWED_EXC = {}
CURRENT_EXC = {}
EXC_TEMP = ""
TITLE_TEMP = ""
BUTTON_LINK_TEMP = ""

app = Flask(__name__)

def upload_file(request, file_name = "sol1.txt"):
    """
    upload a file.
    if an error occured return the url of the error message,
    else return none
    """
    # check if the post request has the file part
    if 'file' not in request.files:
        #flash('No file part') #flash doesn't work without secret key
        return "no file attached"
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        return "illegal file selected"
    file.save(UPLOAD_FOLDER + file_name)
    return None

def message_page_gen(msg, return_url, return_button_name):
        """
        generate a page with a single message.
        should be usefull for both errors, success messages.
        """
        msg_html = """
        <!doctype html>
        <title>"""
        msg_html += msg + "</title>\n"
        msg_html += "<h1>" + msg + "</h1>\n"
        msg_html += "<form method=get enctype=multipart/form-data>\n"
        msg_html += "   <a href=\"" + return_url +  "\">" + return_button_name + "</a>\n"
        return msg_html + "</form>\n"

def exc_page_gen(has_attached_files = True):
    """
    create the html corresponding to an exceresise get command.
    basiccaly describ what the user will see.
    """
    tm = Template(EXC_TEMP)
    return tm.render(id = str(CURRENT_EXC[session['username']]), down_inst_url=url_for("download_instruction"),  
        down_files_url=url_for("download_files"),main_menu_url=url_for("main_menu"), has_attached_files = has_attached_files)

@app.route('/main_menu', methods=['GET'])        
def main_menu():
    tm = Template(TITLE_TEMP)
    html_data = tm.render(title="gerber file excresises main menu", color = "black")
    max_allowed_exc = USER_MAX_ALLOWED_EXC[session['username']]
    for ind in range(1, max_allowed_exc + 1): #begin from 1 to match 1-base exc numbering
        tm = Template(BUTTON_LINK_TEMP)
        html_data += tm.render(url="/exc/<"+str(ind)+">", class_b="primary", disabled = "", text = "excresise "+str(ind))
        
    #add disabled button for next excersise
    if max_allowed_exc <= NUM_ECXS:
        tm = Template(BUTTON_LINK_TEMP)
        html_data += tm.render(url=request.url, class_b="secondary ", disabled = "disabled", text = "excresise "+str(max_allowed_exc+1))
    return html_data


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        #if not(session['username'] in  USER_MAX_ALLOWED_EXC):
        if not(USER_MAX_ALLOWED_EXC.key_in_db(session['username'])):
            USER_MAX_ALLOWED_EXC[session['username']] = 1
        return redirect(url_for('main_menu'))

    return '''
    <!doctype html>
    <title>gerber file excresises login</title>
    <h1>gerber file excresises login</h1>
    
    <form method="post">
        <label for="username">your full name:</label>
        <input type="username" name="username" id="username" required>
        <input type="submit" value="Register">
    </form>
    '''
        
        
@app.route("/download_inst")
def download_instruction():
    """
    downlaod the relevant instruction file
    """
    return send_file("tar_doc/exc" + str(CURRENT_EXC[session['username']])+ ".docx", as_attachment=True)
   
@app.route("/download_files")
def download_files():
    """
    download the relevant user file, if exists.
    """
    return send_file("user_files/exc" + str(CURRENT_EXC[session['username']]) + ".zip", as_attachment=True)
        
#########exc1 specific code#########################       
def passed_exc1():
    return True #TODO: implement test logic later   

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
has_files_to_download_list = [True, True, False, False]    
    

@app.route('/exc/<id>', methods=['GET', 'POST'])    
def exc(id):
    """
    function responsible for card of excersise.
    all excersise are basically with the same layout and gui.
    """
    global CURRENT_EXC
    
    id = int(id[1:-1])#convert to string and remove '<' chars.
    test_func = test_func_list[id - 1]
    has_files_to_download = has_files_to_download_list[id - 1]
    
    if request.method == 'POST':
        upload_file_ret_val = upload_file(request, "sol_"+session['username']+".txt")
        if upload_file_ret_val != None:
            return message_page_gen(upload_file_ret_val, request.url, "retry_submission")
        if test_func():#if passed test
            global USER_MAX_ALLOWED_EXC
            USER_MAX_ALLOWED_EXC[session['username']] = max(USER_MAX_ALLOWED_EXC[session['username']], id + 1)
            return message_page_gen("submission correct", url_for("main_menu"), "main_menu")
        else:
            return message_page_gen("submission incorrect", request.url, "retry_submission ")

    if USER_MAX_ALLOWED_EXC[session['username']] >= id:
        CURRENT_EXC[session['username']] = id
        return exc_page_gen(has_files_to_download)
    else:
        return message_page_gen(" you have not completed the requirments for excresise"+ str(id), url_for("main_menu"), "back to main menu")


if __name__=="__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    USER_MAX_ALLOWED_EXC = DataBaseWrapper("gerber_exc.db", "name_max_exc", int)
    
    EXC_TEMP = open("templates/exc.html", "r").read()
    TITLE_TEMP = open("templates/title.html", "r").read()
    BUTTON_LINK_TEMP = open("templates/button_link.html", "r").read()
    
    app.run("127.0.0.1", 12345)
