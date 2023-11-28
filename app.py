from flask import Flask, render_template
app = Flask(
    __name__,
    template_folder="./pages",
    static_folder="./css"
)

@app.route("/")
def login():
    return render_template('login.html')

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
    return render_template('cancelApplication.html')