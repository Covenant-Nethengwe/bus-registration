from flask import Flask, request, render_template
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

@app.route("/")
def login():
    names = ["Covenant", "Mihlali", "Yonwaba"]
    for name in names:
        print(name)
    return render_template('login.html', names=names)

@app.route("/register/learner")
def learner_register():
    return render_template('learnerRegister.html')

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
        
        if password.count < 4:
            message = "Passwords exceed for characters or numbers!"
            return render_template('parentRegister.html', warning=message)
    
        if password == c_password:
            query = f'''
            INSERT INTO parent (parentname, parentsurname, password, cellphonenumber, parentemail) 
            VALUES('{f_name}', '{l_name}', '{password}', '{cell_no}', '{email}')'''
            
            cnxn.execute(query)
            cnxn.commit()
            cnxn.close()
            return render_template('login.html')

@app.route("/register/admin")
def admin_register():
    return render_template('adminRegister.html')

@app.route("/assign-learner/bus")
def assign_learner_bus():
    return render_template('assignLearnerBus.html')

@app.route("/send/email")
def send_email():
    return "<p>sending email...</p>"

@app.route("/cancel/application")
def cancel_application():
    query = f"SELECT * FROM learner"
    learners = []

    cursor.execute(query)

    for row in cursor:
        if row[6] == True and row[5] == 1 or row[5] == 2 or row[5] == 3:
            if row[5] == 1:
                row[5] == "Bus 1"
                row[6] = "Registered"
            elif row[5] == 2:
                row[5] == "Bus 2"
                row[6] = "Registered"
            elif row[5] == 3:
                row[5] = "Bus 3"
                row[6] = "Registered"
        else:
            row[6] = "Not Registered"
        
        learners.append(row)
    
    return render_template('cancelApplication.html', learners=learners)

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)