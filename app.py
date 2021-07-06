import subprocess
from flask import Flask, render_template, url_for, redirect, request, session, json, jsonify
import database
import gmail
import os
from ML_code import Classifier
from flask import cli

app = Flask(__name__)
app.secret_key = "lkSJdhspxookuybua opsoiu7pn87qpnpoin"
file = 'data/SMS.csv'
db = database.Database()
try:
    db.create_history_table()
    db.create_result_table()
except:
    pass
@app.route('/')
def index():
    return render_template("index.html")


@app.route('/SignUp', methods=['GET', 'POST'])
def Sign_up():
    errors = ""
    if request.method == 'POST':
        db = database.Database()
        try:
            db.create_user_table()
        except:
            pass
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('pwd')
        cpassword = request.form.get('cpwd')
        print(password == cpassword)
        print(len(username))
        print(len(password) > 6)
        print('@' in email)
        print('.com' in email)
        print(len(email) > 11)

        if password == cpassword and len(username) > 2 and len(password) > 6 \
                and len(cpassword) > 6 and '@' in email and '.com' in email and len(email) > 11:
            status = db.add_user(username, email, password)
            return render_template("index.html", data="success")
        else:
            errors = "invalid details"

    return render_template("Sign Up.html", errors=errors)


@app.route('/SignIn', methods=['GET', 'POST'])
def Sign_in():
    errors = ""
    print('run')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('pwd')
        if username and password:
            db = database.Database()
            userlist = db.get_user()
            # print(userlist)
            for row in userlist:
                if username in row and password in row:
                    session['id'] = row[0]
                    session['username'] = row[1]
                    message = "successfully logged in"

                    return redirect(url_for('auth', data=message))
            errors = "invalid credentials"
        else:
            errors = "please fill details"
    return render_template("Sign in.html", errors=errors)


@app.route('/logout')
def logout():
    session.clear()
    if os.path.exists('token.json'):
        os.remove('token.json')
    return redirect(url_for('index'))


@app.route('/fetch')
def fetch_email():
    return render_template('Fetch_Email.html')


@app.route('/authenticate')
def auth():
    command = f"python gmail.py"
    try:
        request_status = subprocess.check_output(command.split(), shell=True)
    except Exception as e:
        print(e)
    message = "successfully logged in"
    return redirect(url_for('fetch_email', data=message))


@app.route('/fetch_request')
def get_mails():
    max_mails = request.args.get('mails')
    service = gmail.main()
    mails = gmail.show_threads(service, max_mails)
    print(type(mails))
    session['mails']= mails
    return jsonify(mails)


@app.route('/analyzemails', methods=['POST', 'GET'])
def analyzemails():
    db=database.Database()
    cfy = Classifier(file)
    results=[]
    cfy.set_model(cfy.load_model('classifier1'), cfy.load_model('vector1'))
    spam_counter=0

    for i,ls in enumerate( session['mails']):
        #results.append({'from' : ls['from']})
        result = cfy.predict_text(ls['snippet'])
        result[ls['snippet']]+='--------------from : '+ls['from']
        results.append(result)
        spamorham = list(result.values())[0]
        db.add_history(session.get('id'), ls['snippet'], ls['subject'], spamorham)
        if spamorham == "spam":
            spam_counter+=1
    db.add_results(session.get('id'),'*******@*mail.com',i,spam_counter,i-spam_counter)

    print(results)

    return jsonify(results)
@app.route('/results')
def result():
    return render_template("results.html")

@app.route('/fetchresults')
def fetchresults():
    db = database.Database()
    userlist = db.get_results()
    result=[]
    for row in userlist:
        if session['id']==row[1]:
            result.append(row)
    return jsonify(result)
@app.route('/fetchhistory')
def fetchhistory():
    db = database.Database()
    userlist = db.get_history()
    result=[]
    for row in userlist:
        if session['id']==row[1]:
            result.append(row)
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
