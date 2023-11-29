from flask import Flask, request, render_template, redirect, url_for
import pyodbc

cnxn = pyodbc.connect(
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=LAPTOP-1A8Q1T1G\SQLEXPRESS;"
    "Database=ImpumeleloHighSchoolBusRegistrationDB;"
    "Trusted_Connection=yes;"
)
cursor = cnxn.cursor()

app = Flask(
    __name__,
    template_folder="./pages",
    static_folder="./css"
)

session_id = 0

@app.route("/login", methods=["GET", "POST"])
def login():
    credentials = []

    if request.method == "GET":
        return render_template('login.html')
    
    if request.method == "POST":
        email = request.form.get("learnerName")
        password = request.form.get("learnerSurname")

        if email.__contains__('@gmail'):
            query = f'''SELECT (parentid, parentemail, password) FROM parent WHERE parentemail = '{email}' AND password = '{password}' '''

            cnxn.execute(query)
            cnxn.execute()

            for row in cursor:
                credentials.append(row)
        
        if email.__contains__('@admin'):
            query = f'''SELECT (adminid, email, password) FROM administrator WHERE email = '{email}' AND password = '{password}' '''

            cnxn.execute(query)
            cnxn.execute()

            for row in cursor:
                credentials.append(row)

        if not credentials:
            message = "Incorrect email or password"
            return render_template('login', warning=message)
        else:
            global session_id
            session_id = credentials[0]
            return redirect(url_for('cancel_application', parent_id=session_id))

@app.route("/register/learner", methods=["GET", "POST"])
def learner_register():
    if request.method == "GET":
        return render_template('learnerRegister.html')
    
    if request.method == "POST":
        f_name = request.form.get("learnerName")
        l_name = request.form.get("learnerSurname")
        cell_no = request.form.get("cellNumber")
        grade = request.form.get("grade")

        query = f'''
        INSERT INTO learner (learnername, learnersurname, learnercellphonenumber, grade) 
        VALUES('{f_name}', '{l_name}', '{cell_no}','{grade}')'''
        
        cnxn.execute(query)
        cnxn.commit()
    
    return redirect('/cancel/application')

@app.route("/register/parent", methods=["GET", "POST"])
def parent_register():
    if request.method == "GET":
        return render_template('parentRegister.html')
    
    if request.method == "POST":
        f_name = request.form.get("firstName")
        l_name = request.form.get("lastName")
        email = request.form.get("email")
        cell_no = request.form.get("phone")
        password = request.form.get("password")
        c_password = request.form.get("confirmPassword")

        if password != c_password:
            message = "Passwords must match!"
            return render_template('parentRegister.html', warning=message)
        
        if len(password) < 4:
            message = "Password length must be greater than 4 characters!"
            return render_template('parentRegister.html', warning=message)
    
        if password == c_password:
            query = f'''
            INSERT INTO parent (parentname, parentsurname, password, cellphonenumber, parentemail) 
            VALUES('{f_name}', '{l_name}', '{password}', '{cell_no}', '{email}')'''
            
            cnxn.execute(query)
            cnxn.commit()
            cnxn.close()
            return render_template('login.html')

@app.route("/register/admin", methods=["GET", "POST"])
def admin_register():
    if request.method == "GET":
        return render_template('adminRegister.html')
    
    if request.method == "POST":
        name = request.form.get("initials")
        l_name = request.form.get("surname")
        email = request.form.get("email")
        password = request.form.get("password")
        c_password = request.form.get("confirmPassword")

        if password != c_password:
            message = "Passwords must match!"
            return render_template('adminRegister.html', warning=message)
        
        if len(password) < 4:
            message = "Password length must be greater than 4 characters!"
            return render_template('adminRegister.html', warning=message)
    
        if password == c_password:
            query = f'''
            INSERT INTO administrator (initials, surname, password, email) 
            VALUES('{name}', '{l_name}', '{password}', '{email}')'''
            
            cnxn.execute(query)
            cnxn.commit()
            cnxn.close()
            return render_template('login.html')

@app.route("/assign-learner/bus")
def assign_learner_bus():
    return render_template('assignLearnerBus.html')

@app.route("/send/email")
def send_email():
    return "<p>sending email...</p>"

@app.route("/cancel/application/<parent_id>")
def cancel_application(parent_id):
    temp = []
    children = []

    query = f'''SELECT learnerid FROM parentlearner WHERE parentid = {parent_id}'''
    cursor.execute(query)

    for row in cursor:
        temp.append(row)

    for learnerid in temp:
        learner_id = learnerid[0]

        query_children = f'''SELECT * FROM learner WHERE learnerid = {learner_id}'''
        cursor.execute(query_children)
        for row in cursor:
            children.append(row)

    return render_template('cancelApplication.html', learners=children)
if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)