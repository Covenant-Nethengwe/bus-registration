from flask import Flask, render_template
import pyodbc

# cnxn = pyodbc.connect(
#     "Driver={ODBC Driver 17 for SQL Server};"
#     "Server=LAPTOP-1A8Q1T1G\SQLEXPRESS;"
#     "Database=ImpumeleloHighSchoolBusRegistrationDB;"
#     "Trusted_Connection=yes;"
# )

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

@app.route("/register/parent")
def parent_register():
    return render_template('parentRegister.html')

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
    learners = []

    # cursor = cnxn.cursor()
    # cursor.execute('SELECT * FROM learner')

    # for row in cursor:
    #     print(learners)

    return render_template('cancelApplication.html', learners=learners)

if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=3000)