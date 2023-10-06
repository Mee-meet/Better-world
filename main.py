from flask import Flask,render_template,request,redirect,session
import mysql.connector
import os
import hashlib
from imgurpython import ImgurClient
import requests
from flask_session import Session
import glob
import json
import ast


app = Flask(__name__)
app.secret_key = 'ihyfhbhbfrfbiihrewuibwe5436889'
def compute_sha256_hash(data):

    sha256_hash = hashlib.sha256()
    if isinstance(data, str):
        data = data.encode('utf-8')

    sha256_hash.update(data)
    hash_value = sha256_hash.hexdigest()
    return hash_value
@app.route('/')
def index():
    try:
        if session['user_data']:
                show_login_signup="False"
                role = session['user_data']['role']
                email = session['user_data']['email']
        else:
            show_login_signup="True"
        return render_template('index.html',show_login_signup=show_login_signup,role=role,email=email)
    except:
        return render_template('index.html',show_login_signup="True")
        
@app.route('/org_portal')
def org_portal():
    try:
        if session['user_data']:

            check = session['user_data']
            if check['role'] == "org" and check['email']:
                dataBase = mysql.connector.connect(host="localhost", user="root", password="", database="betterworld")
                cursorObject = dataBase.cursor()
                data = (check['email'],)
                email = (check['email'],)

                cursorObject.execute("select name from organization where email=%s",data)
                data = cursorObject.fetchall()
                cursorObject.execute("select * from events where copy_email=%s",email)
                event_data = cursorObject.fetchall()
                return render_template('org_portal.html',name=data,event_data=event_data)
            else:
                return 'Unauthorised access '
        else:
            return 'Unauthorised access '
    except:
             return 'Unauthorised access '


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')




@app.route('/event')
def event():
    try:
        if session['user_data']:
            show_login_signup="False"
            role = session['user_data']['role']
            email = session['user_data']['email']
            if role == "user":

                dataBase  = mysql.connector.connect(host="localhost", user="root", password="", database="betterworld")
                cursorObject  = dataBase.cursor()
                data = (email,)
                cursorObject.execute("select interest from user where email=%s",data)
                interests = str(cursorObject.fetchall())
                    # [("['Cooking']",)]
                    
                print(interests)
                interests = interests.replace(')','')
                interests = interests.replace('(','')
                interests = interests.replace('"','')
                interests = list(interests)
                interests[-1] = ''
                interests[-2] = ''
                interests[0] = ''
                newstr = ''
                for i in interests:
                    newstr += i
                print(interests )
                print(newstr)
                aa = ast.literal_eval(newstr)

                count = len(aa)
                sql = 'SELECT * FROM events where '
                print(sql)
                print(sql)
                print(sql)
                count1=0
                for i in aa:
                    if count1 < count-1:
                        sql = sql + f" interest LIKE '%{i}%'"
                        sql = sql + f" or "
                    else:
                        sql  = sql + f" interest LIKE '%{i}%'"
                    count1= count1+ 1


                cursorObject  = dataBase.cursor()
                cursorObject.execute(sql)
                events = cursorObject.fetchall()
                return render_template('event.html',show_login_signup=show_login_signup,role=role,email=email,events=events)

        else:
            show_login_signup="True"
        return render_template('event.html',show_login_signup=show_login_signup,role=role,email=email)
    except:
        return render_template('event.html',show_login_signup="True")


@app.route('/logout')
def logout():
    try:
        session.clear()
    except:
        return redirect('/')
    
    return redirect('/')
@app.route('/api/<slog>',methods=['POST','GET'])
def api(slog):
    if request.method=="POST":
        if slog=="signup-user":
   
            name = request.form.get('name')
            username = request.form.get('username')
            email = request.form.get('email')
            phone = request.form.get('phone')
            email = request.form.get('email')
            city = request.form.get('city')
            password = request.form.get('password')
            hash_pas= compute_sha256_hash(password)
            interests = ["Programming","Cooking","Food Distribution","Cleaning","Old age home"]    
            actual_interest = []
            for i in range(1,5):
                if request.form.get(str(i)) == "on":
                    actual_interest.append(interests[i])
            actual_interest = str(actual_interest)

            dataBase  = mysql.connector.connect(host="localhost", user="root", password="", database="betterworld")
            cursorObject  = dataBase.cursor()
            data = (name,username,email,phone,city,hash_pas,actual_interest)
            cursorObject.execute("INSERT INTO user (name, user_name, email, phone, city, password,interest) VALUES (%s, %s, %s, %s, %s, %s,%s)",data)
            dataBase.commit()
            return redirect('/login')  # Add a response for POST requests
        elif slog =="sign_organization":
                name = request.form.get('name')
                email = request.form.get('email')
                phone = request.form.get('phone')
                address = request.form.get('address')
                iso = request.form.get('iso')
                password = request.form.get('password')
                about = request.form.get('about')
                hash_pas= compute_sha256_hash(password)

                print(about,about)
                dataBase  = mysql.connector.connect(host="localhost", user="root", password="", database="betterworld")
                cursorObject  = dataBase.cursor()
                data = (name,email,phone,address,hash_pas,iso,about)
                cursorObject.execute("INSERT INTO organization (name, email, phone, address, password, iso,about) VALUES (%s, %s, %s, %s, %s, %s,%s)",data)
                dataBase.commit()
                return 'Wait until admin approves your application'  # Add a response for POST requests
        
        elif slog == "user-login":
            email = request.form.get('email')
            password = request.form.get('password')
            dataBase = mysql.connector.connect(host="localhost", user="root", password="", database="betterworld")
            cursorObject = dataBase.cursor()
            cursorObject.execute("select email, password from user")
            result = cursorObject.fetchall()
            hash_pas= compute_sha256_hash(password)
            status = False

            for x in result:
                if x[0] == email and x[1] == hash_pas:
                    status = True
                    break
            if status:
                session['user_data'] = {
                'email': email,  # Add more user data as needed
                'role': 'user'  # Example: User role
                    }
                return redirect('/')
            else:
                return "Wrong Password"
            
        elif slog == "organization-login":
            email = request.form.get('email')
            password = request.form.get('password')
            dataBase = mysql.connector.connect(host="localhost", user="root", password="", database="betterworld")
            cursorObject = dataBase.cursor()
            cursorObject.execute("select email, password from organization")
            result = cursorObject.fetchall()
            hash_pas= compute_sha256_hash(password)
            status = False

            for x in result:
                if x[0] == email and x[1] == hash_pas:
                    status = True
                    break
            if status:
                data = (email,)
                cursorObject.execute("select admin from organization where email=%s",data)
                result = cursorObject.fetchall()
                if result[0][0] == 0:
                    return 'Wait until admin approves your application'  # Add a response for POST requests
                else:

                    session['user_data'] = {
                'email': email,  # Add more user data as needed
                'role': 'org'  # Example: User role
                    }
                    return redirect('/org_portal')      
        elif slog == "event_detail":
            name = request.form.get('name')
            title = request.form.get('title')
            date = request.form.get('date')
            time = request.form.get('time')
            city = request.form.get('city')
            google_map = request.form.get('google_map')
            description = request.form.get('description')
            interests = ["hello","Programming","Cooking","Food Distribution","Cleaning","Old age home"]    
            actual_interest = []
            for i in range(0,6):
                print(actual_interest)
                if request.form.get(str(i)) == "on":
                    print(request.form.get(str(i))) 
                    actual_interest.append(interests[i])
            actual_interest = str(actual_interest)
            
            email = session['user_data']['email']

            dataBase = mysql.connector.connect(host="localhost", user="root", password="", database="betterworld")
            cursorObject = dataBase.cursor()
            data = (name,date,title,time,city,google_map,description,actual_interest,email)
            cursorObject.execute("INSERT INTO events (organization, date,title, time, city, google_map,description,interest,copy_email) VALUES (%s, %s, %s, %s, %s, %s,%s,%s,%s)",data)
            dataBase.commit()
            return redirect('/org_portal')


            
        else:
            return 'Direct Access To API is not allowed'
                


    else:
        if request.method=="GET":
            if slog=="event_delete":
                id = request.args.get("event")
                dataBase = mysql.connector.connect(host="localhost", user="root", password="", database="betterworld")
                cursorObject = dataBase.cursor()
                data = (str(id),)
                cursorObject.execute("delete from events where id=%s",data)
                dataBase.commit()
                return redirect("/org_portal")
        return 'Direct Access To API is not allowed'
    





app.run(debug=True)