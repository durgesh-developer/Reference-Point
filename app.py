from flask import Flask, render_template, redirect, url_for, request, session
from pymongo import MongoClient
from bson.objectid import ObjectId
import bcrypt
from datetime import datetime


app = Flask(__name__)
app.secret_key = "@13@6$$#ddfccv"

clientPublic = "mongodb+srv://root:root@cluster0.woaiu.mongodb.net/auth?retryWrites=true&w=majority"
clusterPublic = MongoClient(clientPublic)
dbPublic = clusterPublic["auth"]
public=dbPublic['auth']
feed=dbPublic['feedback']


@app.route('/')
def index():
    if 'user' in session:
        a=True
        return render_template('web.html',check=a)
    else:
        return render_template('web.html')


@app.route('/courses')
def home():
    if 'user' in session:
        exist=public.find_one({'username':session['user']})
        return render_template('courses.html',name=exist['name'])
    return redirect(url_for('login'))


@app.route('/signup', methods=['GET','POST'])
def signup():
    try:
        if request.method == 'POST':
            # d, t = dt_string.split(' ')
            name = request.form['name']
            username = request.form['username']
            
            if(not name or not username):
                err = "Please fill required fields"
                return render_template('SignUp.html', err=err)
            else:

                # Registering for Customer

                exist = public.find_one({'username': username})

                if exist is None:
                     hashpass = bcrypt.hashpw(
                           request.form['password'].encode('utf-8'), bcrypt.gensalt())

                     

                     public.insert_one({ 'name': name, 'username': username,
                                        'password': hashpass,})

                     session['user'] = username

                     return redirect(url_for('login'))
                   
                err = "user already exist"
                return render_template('SignUp.html', err=err)

    except:
        err = "Something messed up!! Please Register again"
        return render_template('SignUp.html', err=err)
    return render_template('SignUp.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if request.method == 'POST':

            username = request.form['username']
            if(not username):
                err = "Please fill required fields"
                return render_template('login.html', err=err)
            else:

                userLogin = public.find_one({'username': username})
                if userLogin:
                    if bcrypt.hashpw(request.form['password'].encode('utf-8'), userLogin['password']) == userLogin['password']:
                        session['user'] = username
                        return redirect(url_for('home'))
                err = "invalid credentials"
                return render_template('login.html', err=err)

    except:
        err = "Something messed up!!"
        return render_template('login.html', err=err)

    return render_template('login.html')


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if 'user' in session:
        if request.method == 'POST':

            name = request.form['name']
            exp = request.form.get('exp')
            ask = request.form.get('ask')
            mess = request.form['message']
            if(not name or not exp or not ask or not mess):
                err = "Please fill required fields"
                return render_template('feedback.html', err=err)
            else:
                feed.insert_one({'name':name,'experience':exp,'understand':ask,'message':mess,'username':session['user']})
                return redirect(url_for('success'))

        return render_template('feedback.html')
    return redirect(url_for('login'))

@app.route('/about')
def about():
    if 'user' in session:
        return render_template('aboutus.html')
    return redirect(url_for('login'))

@app.route('/success')
def success():
    if 'user' in session:
        return render_template('success.html')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/contact')
def contact():
    if 'user' in session:
        return render_template('Contact.html')
    return redirect(url_for('login'))
    

@app.route('/11')
def tcourse():
    if 'user' in session:
        return render_template('11tcourse.html')
    return redirect(url_for('login'))

@app.route('/12')
def t2course():
    if 'user' in session:
        return render_template('12tcourse.html')
    return redirect(url_for('login'))

@app.route('/exam')
def exam():
    if 'user' in session:
        return render_template('exam.html')
    return redirect(url_for('login'))

@app.route('/11ph')
def physics11():
    if 'user' in session:
        return render_template('11physicslinks.html')
    return redirect(url_for('login'))

@app.route('/12ph')
def physics12():
    if 'user' in session:
        return render_template('12physicslinks.html')
    return redirect(url_for('login'))

@app.route('/11ma')
def maths11():
    if 'user' in session:
        return render_template('11mathslinks.html')
    return redirect(url_for('login'))

@app.route('/12ma')
def maths12():
    if 'user' in session:
        return render_template('12mathslinks.html')
    return redirect(url_for('login'))

@app.route('/11che')
def chemistry11():
    if 'user' in session:
        return render_template('11chemlinks.html')
    return redirect(url_for('login'))
    
@app.route('/12che')
def chemistry12():
    if 'user' in session:
        return render_template('12chemlinks.html')
    return redirect(url_for('login'))

@app.route('/11bio')
def biology11():
    if 'user' in session:
        return render_template('11biolinks.html')
    return redirect(url_for('login'))

@app.route('/12bio')
def biology12():
    if 'user' in session:
        return render_template('12biolinks.html')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=3000, debug=True)