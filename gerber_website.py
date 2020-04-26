import os
from flask import Flask, flash, request, redirect, url_for, send_file, session
#from werkzeug.utils import secure_filename
from data_base_wrapper import *
from jinja2 import Template
import threading
from exc_checking.exc_check import *

UPLOAD_FOLDER = 'upload_folder/'
NUM_ECXS = 5
USER_MAX_ALLOWED_EXC = {}
USER_PWDS = {}
CURRENT_EXC = {}
EXC_TEMP = ""
TITLE_TEMP = ""
BUTTON_LINK_TEMP = ""
LOG_REG_TEMP = ""

REGISTER_LOCK = None


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

def message_page_gen(msg, return_url, return_button_name, color = 'black'):
    """
    generate a page with a single message.
    should be usefull for both errors, success messages.
    """
    tm = Template(TITLE_TEMP)
    html_data = tm.render(title=msg, color = color)
    tm = Template(BUTTON_LINK_TEMP)
    html_data += tm.render(url=return_url, class_b="primary ", text = return_button_name)
    return html_data

def exc_page_gen(has_attached_files = True):
    """
    create the html corresponding to an exceresise get command.
    basiccaly describ what the user will see.
    """
    tm = Template(EXC_TEMP)
    return tm.render(id = str(CURRENT_EXC[session['username']]), down_inst_url="/download_inst/<"+str(CURRENT_EXC[session['username']])+">",  
        down_files_url="/download_files/<"+str(CURRENT_EXC[session['username']])+">",main_menu_url=url_for("main_menu"), has_attached_files = has_attached_files)

@app.route('/main_menu', methods=['GET'])        
def main_menu():
    tm = Template(TITLE_TEMP)
    html_data = tm.render(title="gerber file excresises main menu", color = "black")
    max_allowed_exc = min(NUM_ECXS, USER_MAX_ALLOWED_EXC[session['username']])
    for ind in range(1, max_allowed_exc + 1): #begin from 1 to match 1-base exc numbering
        tm = Template(BUTTON_LINK_TEMP)
        html_data += tm.render(url="/exc/<"+str(ind)+">", class_b="primary", text = "exercise "+str(ind))
        
    #add disabled button for next excersise
    if max_allowed_exc < NUM_ECXS:
        tm = Template(BUTTON_LINK_TEMP)
        html_data += tm.render(url=request.url, class_b="disabled ", text = "exercise "+str(max_allowed_exc+1))
    return html_data

@app.route('/register', methods=['GET', 'POST'])
def register():
    global USER_PWDS
    global USER_MAX_ALLOWED_EXC
    if request.method == 'POST':
        session['username'] = request.form['username']
        session['password'] = request.form['password']
        with REGISTER_LOCK:#section of registreation is the only possible section when 2 user can collide
            if USER_PWDS.key_in_db(session['username']):
                html_data =  message_page_gen("username already exists, please try other name or login with current name", request.url, "retry_registreation")
                tm = Template(BUTTON_LINK_TEMP)
                html_data += tm.render(url=url_for("login"), class_b="primary ", text = "login")
                return html_data
                
            USER_PWDS[session['username']] = session['password']
            USER_MAX_ALLOWED_EXC[session['username']] = 1
        return redirect(url_for('main_menu'))
    
    tm = Template(LOG_REG_TEMP)
    return tm.render(log_reg="register")
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        session['password'] = request.form['password']
        if not(USER_PWDS.key_in_db(session['username'])):
            html_data =  message_page_gen("username doesnt exists, please try other name or register with current name", request.url, "retry_login")
            tm = Template(BUTTON_LINK_TEMP)
            html_data += tm.render(url=url_for("register"), class_b="primary ", text = "register")
            return html_data
        if session['password'] != USER_PWDS[session['username']]:
            return message_page_gen("incorrect password, please try again", request.url, "retry_login")
        return redirect(url_for('main_menu'))
    
    tm = Template(LOG_REG_TEMP)
    return tm.render(log_reg="login")

@app.route('/', methods=['GET'])
def enter_screen():
    tm = Template(TITLE_TEMP)
    html_data = tm.render(title="welcome to gerber excersise")
    tm = Template(BUTTON_LINK_TEMP)
    html_data += tm.render(url=url_for("register"), class_b="primary ", text = "register")
    tm = Template(BUTTON_LINK_TEMP)
    html_data += tm.render(url=url_for("login"), class_b="primary ", text = "login")
    return html_data
        
        
@app.route("/download_inst/<id>")
def download_instruction(id):
    """
    downlaod the relevant instruction file
    """
    return send_file("tar_doc/exc" + id[1:-1]+ ".docx", as_attachment=True)
 
exc_file_extention = [".txt", ".zip", None, ".txt", None] 
@app.route("/download_files/<id>")
def download_files(id):
    """
    download the relevant user file, if exists.
    """
    return send_file("user_files/exc" + id[1:-1] + exc_file_extention[CURRENT_EXC[session['username']] - 1], as_attachment=True)

test_func_list = [passed_exc1, passed_exc2, passed_exc3, passed_exc4, passed_exc5]
has_files_to_download_list = [True, True, False, True, False]    
    

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
            return message_page_gen(upload_file_ret_val, request.url, "retry_submission", "red")
        test_error_msg = test_func()
        if test_error_msg == None:#if passed test
            global USER_MAX_ALLOWED_EXC
            USER_MAX_ALLOWED_EXC[session['username']] = max(USER_MAX_ALLOWED_EXC[session['username']], id + 1)
            return message_page_gen("submission correct", url_for("main_menu"), "main_menu", "LimeGreen")
        else:
            return message_page_gen("submission incorrect" + test_error_msg, request.url, "retry_submission ", "red")
            
    if USER_MAX_ALLOWED_EXC[session['username']] >= id:
        CURRENT_EXC[session['username']] = id
        return exc_page_gen(has_files_to_download)
    else:
        return message_page_gen(" you have not completed the requirments for excresise"+ str(id), url_for("main_menu"), "back to main menu")

        
if __name__=="__main__":
    app.secret_key = os.urandom(1024)
    app.config['SESSION_TYPE'] = 'filesystem'
    USER_MAX_ALLOWED_EXC = DataBaseWrapper("gerber_exc.db", "name_max_exc", int)
    USER_PWDS = DataBaseWrapper("pwd.db", "pwds", str)
    
    EXC_TEMP = open("templates/exc.html", "r").read()
    TITLE_TEMP = open("templates/title.html", "r").read()
    BUTTON_LINK_TEMP = open("templates/button_link.html", "r").read()
    LOG_REG_TEMP = open("templates/log_reg.html", "r").read()
    
    REGISTER_LOCK = threading.Lock()
    
    app.run(host="0.0.0.0", port=12345, debug=False)
