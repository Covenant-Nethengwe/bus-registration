from flask import Flask, request, render_template, redirect, url_for
from flask_mail import Mail, Message
import pyodbc
from dotenv import load_dotenv
load_dotenv()
import os

cnxn = pyodbc.connect(
    f'Driver={os.getenv('DRIVER')};'
    f'Server={os.getenv('SERVER')};'
    f'Database={os.getenv('DATABASE')};'
    'Trusted_Connection=yes;'
)
cursor = cnxn.cursor()

app = Flask(
    __name__,
    template_folder="./pages",
    static_folder="./css"
)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEBUG'] = True
app.config['MAIL_SUPPRESS_SEND'] = False
app.config['TESTING'] = False
mail = Mail(app)

session_id = 0

@app.route("/")
def home():
    return render_template('index.html')

@app.route('/logout')
def logout():
    global session_id
    session_id = 0
    return redirect(url_for('login'))

@app.route("/login", methods=["GET", "POST"])
def login():
    credentials = []

    if request.method == "GET":
        return render_template('login.html')
    
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if email.__contains__('@gmail'):
            query = f'''SELECT parentid, parentemail, password FROM parent WHERE parentemail = '{email}' AND password = '{password}' '''

            cursor.execute(query)

            for row in cursor:
                credentials.append(row)
        
        if email.__contains__('@admin'):
            query = f'''SELECT adminid, email, password FROM administrator WHERE email = '{email}' AND password = '{password}' '''

            cursor.execute(query)

            for row in cursor:
                credentials.append(row)

        if not credentials:
            message = "Incorrect email or password"
            return render_template('login.html', warning=message)
        
        global session_id
        
        if credentials[0][1].__contains__('@gmail'):
            session_id = credentials[0][0]

            return redirect(url_for('cancel_application', parent_id=session_id))
        
        if credentials[0][1].__contains__('@admin'):
            session_id = credentials[0][0]

            return redirect(url_for('assign_bus', admin_id=session_id))
        else:
            message = "Email must contain @admin or @gmail"
            return render_template('login.html', warning=message)


@app.route("/register/learner", methods=["GET", "POST"])
async def learner_register():
    
    if session_id == 0:
        message = 'Please login!'
        return render_template('login.html', warning=message)

    if request.method == "GET":
        return render_template('learnerRegister.html')
    
    if request.method == "POST":
        f_name = request.form.get("learnerName")
        l_name = request.form.get("learnerSurname")
        cell_no = request.form.get("cellNumber")
        grade = request.form.get("grade")

        query = f'''
        INSERT INTO learner (learnername, learnersurname, learnercellphonenumber, grade) 
        VALUES('{f_name}', '{l_name}', '{cell_no}', '{grade}')'''
        
        cursor.execute(query)
        cursor.commit()

        recently_added_learner_query = '''SELECT TOP 1 learnerid FROM learner ORDER BY learnerid DESC'''
        cursor.execute(recently_added_learner_query)
        
        learner_id = []
        for row in cursor:
            learner_id.append(row)
    
        assign_learner_parent_query = f'''
        INSERT INTO parentlearner (parentid, learnerid) 
        VALUES('{session_id}', '{learner_id[0][0]}')'''

        cursor.execute(assign_learner_parent_query)
        cursor.commit()
    
        body = f'''
        Congradulations 🎉, You have successfully registerd a bus for {f_name} {l_name}.'''
        await send_email(body)

    return redirect(url_for('cancel_application', parent_id=session_id))

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
            return redirect(url_for('login'))

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

@app.route("/assign/bus/<admin_id>", methods=["GET", "POST"])
def assign_bus(admin_id):
    if session_id == 0:
        message = 'Please login!'
        return render_template('login.html', warning=message)

    learners = []

    query = f'''SELECT * FROM learner'''

    cursor.execute(query)

    for row in cursor:
        if row[6] == True and row[5] == 1 or row[5] == 2 or row[5] == 3:
            if row[5] == 1:
                row[5] = "Bus 1"
                row[6] = "Registered"
            elif row[5] == 2:
                row[5] = "Bus 2"
                row[6] = "Registered"
            elif row[5] == 3:
                row[5] = "Bus 3"
                row[6] = "Registered"
        else:
            row[6] = "Not Registered"
    
        learners.append(row)

    return render_template('assignBus.html', learners=learners)

@app.route("/assign-learner/bus/<learner_id>", methods=["GET" ,"POST"])
def assign_learner_bus(learner_id):

    if session_id == 0:
        message = 'Please login!'
        return render_template('login.html', warning=message)

    if request.method == "GET":
        global learner_id_name
        query = f'''SELECT learnerid, learnername FROM learner WHERE learnerid = {learner_id}'''
        cursor.execute(query)
        
        for row in cursor:
            learner_id_name = row
        
        return render_template('assignLearnerBus.html', learner=learner_id_name)

    if request.method == "POST":

        bus_name = request.form.get('bus')
        pick_up_time = request.form.get('pickupTime')
        drop_off_time = request.form.get('dropoffTime')

        print(f'''{bus_name} {pick_up_time} {drop_off_time}''')

        if bus_name == 'Bus 1':
            query = f'''
            INSERT INTO busschedule (pickuptime, dropofftime, pickupname, dropoffname, pickupnumber, dropoffnumber, learnerid) 
            VALUES ('{pick_up_time}', '{drop_off_time}', '{bus_name}', '{bus_name}', '{35}', '{35}', {learner_id})'''
            cursor.execute(query)
            cursor.commit()
            
            update_learner_query = f'''
            UPDATE learner SET busid={1}, registrationstatus={1}, adminid={session_id} 
            WHERE learnerid = {learner_id}'''
            cursor.execute(update_learner_query)
            cursor.commit()

        elif bus_name == 'Bus 2':
            query = f'''
            INSERT INTO busschedule (pickuptime, dropofftime, pickupname, dropoffname, pickupnumber, dropoffnumber, learnerid) 
            VALUES ('{pick_up_time}', '{drop_off_time}', '{bus_name}', '{bus_name}', '{15}', '{15}', {learner_id})'''
            cursor.execute(query)
            cursor.commit()
            
            update_learner_query = f'''
            UPDATE learner SET busid={2}, registrationstatus={1}, adminid={session_id} 
            WHERE learnerid = {learner_id}'''
            cursor.execute(update_learner_query)
            cursor.commit()

        elif bus_name == 'Bus 3':
            query = f'''
            INSERT INTO busschedule (pickuptime, dropofftime, pickupname, dropoffname, pickupnumber, dropoffnumber, learnerid) 
            VALUES ('{pick_up_time}', '{drop_off_time}', '{bus_name}', '{bus_name}', '{15}', '{15}', {learner_id})'''
            cursor.execute(query)
            cursor.commit()
            
            update_learner_query = f'''
            UPDATE learner SET busid={3}, registrationstatus={1}, adminid={session_id} 
            WHERE learnerid = {learner_id}'''
            cursor.execute(update_learner_query)
            cursor.commit()

    return redirect(url_for('assign_bus', admin_id=session_id))

@app.route("/send/email")
async def send_email(body):

    message = Message('Impumelelo Bus Application', sender='noreply@impumelelo.com', recipients=['mihlalilindwanyaza@gamil.com'])
    message.body = body
    mail.send(message)

    return 'Mail sent.'

@app.route("/cancel/application/<parent_id>")
def cancel_application(parent_id):
    if session_id == 0:
        message = 'Please login!'
        return render_template('login.html', warning=message)

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

            if row[6] == True and row[5] == 1 or row[5] == 2 or row[5] == 3:
                if row[5] == 1:
                    row[5] = "Bus 1"
                    row[6] = "Registered"
                elif row[5] == 2:
                    row[5] = "Bus 2"
                    row[6] = "Registered"
                elif row[5] == 3:
                    row[5] = "Bus 3"
                    row[6] = "Registered"
            else:
                row[6] = "Not Registered"

            children.append(row)

    return render_template('cancelApplication.html', learners=children)

@app.route('/cancel/<learner_id>', methods=["DELETE"])
def cancel_learner(learner_id):
    
    unassign_bus_query = f'''DELETE FROM busschedule WHERE learnerid = {learner_id}'''
    cursor.execute(unassign_bus_query)
    cursor.commit()

    unassign_learner_to_parent_query = f'''DELETE FROM parentlearner WHERE learnerid = {learner_id}'''
    cursor.execute(unassign_learner_to_parent_query)
    cursor.commit()

    query = f'''DELETE FROM learner WHERE learnerid = {learner_id}'''
    cursor.execute(query)
    cursor.commit()

    return f'''Leaner with id: {learner_id} was successfully cancelled.'''
        
if __name__ == "__main__":
    app.run(debug=True)