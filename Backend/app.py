from flask import Flask, render_template, request, redirect, url_for, session, send_file
from flask_mysqldb import MySQL
import hashlib
import bleach
import base64
import io


app = Flask(__name__,template_folder='../Frontend',static_folder='../Frontend/Static', static_url_path='/Static')
app.secret_key = '1234'

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'OnlineClassTrackerDB'

mysql = MySQL(app)

# Set a secret key for the session
# app.secret_key = 'your_secret_key'

# generate an MD5 hash of the password string
def generate_password_hash(password):
    return hashlib.md5(password.encode('utf-8')).hexdigest()

# check if a password matches its hashed value
def check_password_hash(password, hash):
    return generate_password_hash(password) == hash

# define a registration route

@app.route('/',methods=['GET'])
def redirect_page():

    if "uid" in session:
        return redirect(url_for('home'))
    else:
        return redirect(url_for('register'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get the form data
        email = request.form['email']
        password = request.form['password']
        hassed_password = generate_password_hash(password)
        try:
            #db cursor
            cur = mysql.connection.cursor()

            check_email_query = ("SELECT * FROM user WHERE email = %s")
            cur.execute(check_email_query,(email,))  # single value needs to pass like this (value,)

            email_exist = cur.fetchone()

            if email_exist != None:
                cur.close()
                msg = "Email already exists"
                return render_template('/Signup/signup.html',msg = msg)
            else:
                insert_query = "INSERT INTO user VALUES (%s, %s, %s)"
                data = (None,email,hassed_password)
                cur.execute(insert_query,data)
                mysql.connection.commit()

                # setting session variable of uid
                check_email_query = ("SELECT * FROM user WHERE email = %s")
                cur.execute(check_email_query,(email,))
                user_details = cur.fetchone()
                uid = user_details[0]
                email = user_details[1]

                # inserting (emai,uid) to the info table

                info_table_query = "INSERT INTO Info VALUES (%s, %s, %s, %s, %s, %s)"
                info_table_data = (None,None,email,None,None,uid)
                cur.execute(info_table_query,info_table_data)
                mysql.connection.commit()

                # setting up the session variables
                session['uid'] = uid

                #closing the cursor
                cur.close()

                # session msg as flash

                session['flash_message'] = 'Registration Successfully' 
                session['alert'] = 'success'

                return render_template('/Home/home.html')
        except:
            msg = "Sorry Database is Offline. Try Again later."
            return render_template('/Signup/signup.html',msg=msg)
    elif "uid" in session:
        return redirect(url_for('home'))
    else:
        return render_template("/Signup/signup.html")
        
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # get the data

        email = request.form['email']
        password = request.form['password']

        try:

            #db cursor
            cur = mysql.connection.cursor()

            check_email_query = ("SELECT * FROM user WHERE email = %s")
            cur.execute(check_email_query,(email,))  # single value needs to pass like this (value,)

            user_details = cur.fetchone()
            hashed_password = user_details[2] if user_details != None else ""

            if(check_password_hash(password,hashed_password) ==True):
                uid = user_details[0]
                session['uid'] = uid
                cur.close()

                # flash msg

                session['flash_message'] = 'Login Successfully' 
                session['alert'] = 'success'
                return redirect(url_for('home'))
            
            else:
                return render_template("/Login/login.html",msg="Email or Password incorrect")
        except:
            return render_template("/Login/login.html",msg="Database is offline, Please Try again later!")

    elif "uid" in session:
        return redirect(url_for('home'))
    else:
        return render_template("/Login/login.html")  


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('uid',None)
    return redirect(url_for('login'))

@app.route('/home', methods=['GET', 'POST'])
def home():
    if "uid" in session:
        try:
            cur = mysql.connection.cursor()
            query = ("SELECT * FROM course_table WHERE uid = %s")
            uid = session['uid']
            cur.execute(query,(uid,))
            data = cur.fetchall()
            
            # checking if there is any data in the database
            if len(data) > 0:
        
                return render_template('/Home/home.html',data=data,dataExist=True) 
            else:
                return render_template('/Home/home.html',dataExist=False)
        except:
            return render_template('/Login/login.html',msg="Server is Offline! Please Try Again later.")
    else:
        return redirect(url_for('login'))


@app.route("/addCourse",methods=["POST"])
def addCourse():

    # bleach clean is sanitizing the inputs

    course_name = bleach.clean(request.form['course_name'])
    course_code = bleach.clean(request.form['course_id'])
    inst_name = bleach.clean(request.form['instructor_id'])

    uid = session['uid']

    try:

        cur = mysql.connection.cursor()
        # first check if course_code exists or not
        search_query = "SELECT course_code FROM course_table WHERE uid = %s AND course_code = %s"
        search_query_values = (uid,course_code)

        cur.execute(search_query,search_query_values)  # single value needs to pass like this (value,)

        course_exist = cur.fetchone()

        if course_exist != None:
            cur.close()
            # flash msg
            session['flash_message'] = 'Course Already Exist' 
            session['alert'] = 'danger'
            return redirect(url_for('home'))
        else:

            insert_query = "INSERT INTO course_table VALUES (%s, %s, %s, %s, %s)"
            data = (None,course_name,course_code,inst_name,uid)
            cur.execute(insert_query,data)
            mysql.connection.commit()
            cur.close()
            # flash msg
            session['flash_message'] = 'Course Added Successfully' 
            session['alert'] = 'success'

            return redirect(url_for('home'))
    except:
        # flash msg
        session['flash_message'] = 'Unable to Add Course' 
        session['alert'] = 'danger'
        return redirect(url_for('home'))
        

@app.route("/updateCourse",methods=["POST"])
def updateCourse():

    # bleach clean is sanitizing the inputs

    updated_course_name = bleach.clean(request.form['update_course_name'])
    updated_inst_name = bleach.clean(request.form['update_instructor_id'])
    course_code = request.form.get('update_course_id')

    uid = session['uid']

    try:
        cur = mysql.connection.cursor()
        update_query = "UPDATE course_table SET course_name = %s, Ins_name = %s WHERE uid = %s AND course_code = %s"
        data = (updated_course_name,updated_inst_name,uid,course_code)
        cur.execute(update_query,data)
        mysql.connection.commit()
        cur.close()
        # flash msg
        session['flash_message'] = 'Course Info Updated Successfully' 
        session['alert'] = 'info'
        return redirect(url_for('home'))
    except:
        # exception
        session['flash_message'] = 'Unable to Update Course' 
        session['alert'] = 'danger'
        return redirect(url_for('home'))

@app.route("/deleteCourse",methods=["POST"])
def deleteCourse():

    # bleach clean is sanitizing the inputs

    course_code_to_delete = request.form['code']
    uid = session['uid']

    try:

        cur = mysql.connection.cursor()
        update_query = "DELETE FROM course_table WHERE course_code = %s AND uid = %s"
        data = (course_code_to_delete,uid)
        cur.execute(update_query,data)
        mysql.connection.commit()
        cur.close()
        # flash msg
 
        session['flash_message'] = 'Course Deleted Successfully' 
        session['alert'] = 'danger'
    
        return redirect(url_for('home'))
    

    except:
        # flash msg
  
        session['flash_message'] = 'Uanble to delete course' 
        session['alert'] = 'danger'
    
        return redirect(url_for('home'))



@app.route('/profile',methods=['GET'])
def profile():

    if 'uid'in session:
        try:
            cur = mysql.connection.cursor()
            profile_data_query = "SELECT * FROM Info WHERE uid = %s"
            uid = session['uid']
            cur.execute(profile_data_query,(uid,))
            data = cur.fetchall()
            return render_template('/Profile/UserProfile.html',data=data[0])
        except:
            # server down redirect
  
            return render_template('/Login/login.html',msg="Server is Offline! Please Try Again later.")
    else:
        return render_template('/Login/login.html')
    
@app.route('/updateProfile',methods=['POST'])
def updateProfile():

    uid = session['uid']

    # getting the data
    name = bleach.clean(request.form['name'])
    university = bleach.clean(request.form['university'])
    department = bleach.clean(request.form['department'])


    try:
        ## query the info table
        cur = mysql.connection.cursor()
        update_profile_data_query = "UPDATE Info SET name = %s, university = %s, department = %s WHERE uid = %s"
        data = (name,university,department,uid)
        cur.execute(update_profile_data_query,data)
        mysql.connection.commit()
        cur.close()
        
        # falsh msg
        session['flash_message'] = 'Updated Info Successfully!' 
        session['alert'] = 'success'

        return redirect(url_for('profile'))
    except:
        # falsh msg
        session['flash_message'] = 'Unable to Update Info' 
        session['alert'] = 'danger'

        return redirect(url_for('profile'))


@app.route('/updatePassword',methods=['POST'])
def updatePassword():

    # get the data

    cur_pass = bleach.clean(request.form['current_pass'])
    new_pass = bleach.clean(request.form['new_pass'])

    # set uid
    uid = session['uid']

    try:
        #db cursor
        cur = mysql.connection.cursor()

        check_query = ("SELECT * FROM user WHERE uid = %s")
        cur.execute(check_query,(uid,))  # single value needs to pass like this (value,)

        user_details = cur.fetchone()
        hashed_password = user_details[2]

        if(check_password_hash(cur_pass,hashed_password) ==True):

            new_pass_query = ("UPDATE user SET password = %s WHERE uid = %s")
            new_hassed_password = generate_password_hash(new_pass)

            data = (new_hassed_password,uid)
            cur.execute(new_pass_query,data)
            mysql.connection.commit()
            cur.close()

            # falsh msg
            session['flash_message'] = 'Password Updated Successfully!' 
            session['alert'] = 'success'

            return redirect(url_for('profile'))

        
        else:
            # falsh msg
            session['flash_message'] = 'Current Password is Wrong!' 
            session['alert'] = 'danger'

            return redirect(url_for('profile'))
    except:
        # falsh msg
        session['flash_message'] = 'Unable to Update Password' 
        session['alert'] = 'danger'

        return redirect(url_for('profile'))



# getting the course code
@app.route('/courseCodeAjax',methods=['POST'])
def courseCodeAjax():
    course_code_json = request.get_json(force=True)
    course_code = course_code_json['course_code']
    session['course_code'] = course_code

    return redirect(url_for('courseInfo'))

@app.route('/courseInfo',methods=['GET'])
def courseInfo():
    if 'uid' in session:
        try:
            course_code = session['course_code']
            uid = session['uid']
            cur = mysql.connection.cursor()
            query = "SELECT fileTitle, date, fileType from course_materials WHERE course_code = %s AND uid = %s"
            values = (course_code,uid)
            cur.execute(query,values)
            data = cur.fetchall()
            cur.close()
            if(len(data)>0):
                return render_template('/CourseInfo/CourseInfo.html',course_code=course_code,data=data,dataExist=True)
            else:
                return render_template('/CourseInfo/CourseInfo.html',course_code=course_code,dataExist=False)
        except:
            # falsh msg
            session['flash_message'] = 'Please Update User Information to view this course.' 
            session['alert'] = 'danger'
            return redirect(url_for('home'))
        
    else:
        return redirect(url_for('login'))
    


# getting file type func
def get_file_type(filename):
    filetype = filename.split('.')[-1]
    if len(filename.split('.'))>1:
        return filetype
    else:
        return None

@app.route('/uploadFile',methods=['POST'])
def uploadFile():
    fileTitle = request.form['file_name']
    date = request.form['date']
    file = request.files['file']
    fileData = file.read()
    fileName = file.filename
    uid = session['uid']
    course_code = session['course_code']

    # getting file type
    fileType = get_file_type(fileName)

    if(fileType):

        # unique file name
        file_name = fileTitle+'_'+date+'_'+str(uid)+"_"+course_code+'.'+fileType
        try:
            # checking same file exists or not
            cur = mysql.connection.cursor()
            query = "SELECT fileId FROM course_materials WHERE file_name = %s"
            value= (file_name,)
            cur.execute(query, value)
            validName = cur.fetchone()

            if validName == None:
                # insert the data
                # conver to base64 string

                fileBase64 = base64.b64encode(fileData).decode('utf-8')
                
                

                # inserting the data
                query = "INSERT INTO course_materials VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                values = (None,fileTitle,date,uid,course_code,fileType,file_name,fileBase64)
                cur.execute(query,values)
                mysql.connection.commit()
                cur.close()
                # falsh msg
                session['flash_message'] = 'File Added Successfully!' 
                session['alert'] = 'success'
                return redirect(url_for('courseInfo'))
            else:
                cur.close()
                # falsh msg
                session['flash_message'] = 'File name with name same name already Exist!' 
                session['alert'] = 'danger'
                return redirect(url_for('courseInfo'))
        except:
            # falsh msg
            session['flash_message'] = 'Unable to Add file' 
            session['alert'] = 'danger'
            return redirect(url_for('courseInfo'))
    else:
        session['flash_message'] = 'Not a valid file type!' 
        session['alert'] = 'danger'
        return redirect(url_for('courseInfo'))

    
@app.route('/updteFile',methods=['POST'])
def updteFile():
    existingfileTitle = request.form['existing_course_name']
    updatefileTitle = request.form['update_course_name']
    date = request.form['update_date']
    file = request.files['fileUpdate']

    fileData = file.read()
    fileName = file.filename
    uid = session['uid']
    course_code = session['course_code']

    # getting file type
    fileType = get_file_type(fileName)

    if(fileType):

        # unique file name
        file_name = updatefileTitle+'_'+date+'_'+str(uid)+"_"+course_code+'.'+fileType
        fileBase64 = base64.b64encode(fileData).decode('utf-8')
        try:
            # checking same file exists or not
            cur = mysql.connection.cursor()
            query = "UPDATE course_materials SET fileTitle = %s, date = %s, fileType = %s, file_name = %s, file = %s  WHERE fileTitle = %s AND uid = %s AND course_code = %s"
            value= (updatefileTitle,date,fileType,file_name,fileBase64,existingfileTitle,uid,course_code)
            cur.execute(query, value)
            mysql.connection.commit()
            cur.close()  

            # falsh msg
            session['flash_message'] = 'File Updated Successfully!' 
            session['alert'] = 'success'
            return redirect(url_for('courseInfo'))
            
        except:
            # falsh msg
            session['flash_message'] = 'Unable to Update file' 
            session['alert'] = 'danger'
            return redirect(url_for('courseInfo'))
    else:
        session['flash_message'] = 'Not a valid file type!' 
        session['alert'] = 'danger'
        return redirect(url_for('courseInfo'))
    
@app.route('/downloadFile',methods=['POST'])
def downloadFile():
    downloadfileTitle = request.form['downloadName']
    date = request.form['fileDateD']
    uid = session['uid']
    course_code = session['course_code']

    try:
        cur = mysql.connection.cursor()
        query = "SELECT file, file_name FROM course_materials WHERE fileTitle = %s AND date = %s AND uid = %s AND course_code = %s"
        value= (downloadfileTitle,date,uid,course_code)
        cur.execute(query, value)
        file = cur.fetchone()
        cur.close()
        if file:
            file_data = file[0]
            file_name = file[1]
            file_binary = base64.b64decode(file_data)
            file_object = io.BytesIO(file_binary)
            file_object.seek(0)
            return send_file(file_object, as_attachment=True, download_name=file_name)  # attachment_filename is being replaced with download_name

        else:
            session['flash_message'] = 'Unable to Downlaod file!' 
            session['alert'] = 'danger'
            return redirect(url_for('courseInfo'))
    except:
        return redirect(url_for('courseInfo'))


@app.route('/deleteFile',methods=['POST'])
def deleteFile():
    deletefileTitle = request.form['deleteName']
    date = request.form['fileDateDelete']
    uid = session['uid']
    course_code = session['course_code']

    try:
        cur = mysql.connection.cursor()
        delete_query = "DELETE FROM course_materials WHERE fileTitle = %s AND date = %s AND uid = %s AND course_code = %s"
        value= (deletefileTitle,date,uid,course_code)
        cur.execute(delete_query, value)
        mysql.connection.commit()
        cur.close()

        # falsh msg
        session['flash_message'] = 'File Deleted Successfully!' 
        session['alert'] = 'danger'
        return redirect(url_for('courseInfo'))
    except:
        # falsh msg
        session['flash_message'] = 'Unable to Delete file!' 
        session['alert'] = 'danger'
        return redirect(url_for('courseInfo'))
    

@app.route('/recordInfo',methods=['GET','POST'])
def recordInfo():
    if 'uid' in session:
        try:
            course_code = session['course_code']
            uid = session['uid']
            cur = mysql.connection.cursor()
            query = "SELECT name, date, url from recording_table WHERE course_code = %s AND uid = %s"
            values = (course_code,uid)
            cur.execute(query,values)
            data = cur.fetchall()
            cur.close()
            if(len(data)>0):
                return render_template('/RecordingInfo/RecordingInfo.html',course_code=course_code,data=data,dataExist=True)
            else:
                return render_template('/RecordingInfo/RecordingInfo.html',course_code=course_code,dataExist=False)


        except:
            # falsh msg
            session['flash_message'] = 'Unable to Load Recording!' 
            session['alert'] = 'danger'
            return redirect(url_for('home'))
        
    else:
        return redirect(url_for('login'))
    

@app.route('/uploadRecording',methods=['POST'])
def uploadRecording():
    recordTitle = request.form['file_name']
    date = request.form['date']
    url = request.form['url']
    uid = session['uid']
    course_code = session['course_code']
    


    # unique record name
    record_name_unique = recordTitle+'_'+date+'_'+str(uid)+"_"+course_code
    try:
    # checking same file exists or not
        cur = mysql.connection.cursor()
        query = "SELECT uniqueName FROM recording_table WHERE uniqueName = %s"
        value= (record_name_unique,)
        cur.execute(query, value)
        validName = cur.fetchone()

        if validName == None:
            
            # inserting the data
            query = "INSERT INTO recording_table VALUES (%s, %s, %s, %s, %s, %s, %s)"
            values = (None,recordTitle,date,record_name_unique,uid,course_code,url)
            cur.execute(query,values)
            mysql.connection.commit()
            cur.close()
            # falsh msg
            session['flash_message'] = 'Record Uploaded Successfully!' 
            session['alert'] = 'success'
            return redirect(url_for('recordInfo'))
        else:
            cur.close()
            session['flash_message'] = 'Recording Name Already Exist!' 
            session['alert'] = 'danger'
            return redirect(url_for('recordInfo'))
    except:
        session['flash_message'] = 'Unable to Load Recording!' 
        session['alert'] = 'danger'
        return redirect(url_for('home'))
    

@app.route('/updateRecording',methods=['POST'])
def updateRecording():
    existingRecordTitle = request.form['existing_recording_name']
    NewrecordTitle = request.form['update_recording_name']
    date = request.form['update_date']
    url = request.form['url_update']
    uid = session['uid']
    course_code = session['course_code']
    
    # unique record name
    record_name_unique = existingRecordTitle+'_'+date+'_'+str(uid)+"_"+course_code
    new_record_name_unique = NewrecordTitle+'_'+date+'_'+str(uid)+"_"+course_code
    try:
        cur = mysql.connection.cursor()
        query = "UPDATE recording_table SET name = %s, date = %s, uniqueName = %s, url = %s WHERE uniqueName = %s"
        value= (NewrecordTitle,date,new_record_name_unique,url,record_name_unique)
        cur.execute(query, value)
        mysql.connection.commit()
        cur.close()
        # falsh msg
        session['flash_message'] = 'Record Updated Successfully!' 
        session['alert'] = 'success'
        return redirect(url_for('recordInfo'))
    except:
        session['flash_message'] = 'Unable to Load Recording!' 
        session['alert'] = 'danger'
        return redirect(url_for('home'))
    
@app.route('/deleteRecording',methods=['POST'])
def deleteRecording():
    deleterecordTitle = request.form['deleteName']
    date = request.form['DateDelete']
    uid = session['uid']
    course_code = session['course_code']
    unique_name = deleterecordTitle+'_'+date+'_'+str(uid)+"_"+course_code

    try:
        cur = mysql.connection.cursor()
        delete_query = "DELETE FROM recording_table WHERE uniqueName = %s"
        value= (unique_name,)
        cur.execute(delete_query, value)
        mysql.connection.commit()
        cur.close()
        # falsh msg
        session['flash_message'] = 'Record Deleted Successfully!' 
        session['alert'] = 'danger'
        return redirect(url_for('recordInfo'))
    except:
        session['flash_message'] = 'Unable to Load Recording!' 
        session['alert'] = 'danger'
        return redirect(url_for('home'))

if __name__== '__main__':
    app.run(debug=True)