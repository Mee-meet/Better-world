from flask import Flask,render_template,request,redirect
import mysql.connector
import os
import hashlib
from imgurpython import ImgurClient
import requests
import glob
import json


app = Flask(__name__)

def compute_sha256_hash(data):

    sha256_hash = hashlib.sha256()
    if isinstance(data, str):
        data = data.encode('utf-8')

    sha256_hash.update(data)
    hash_value = sha256_hash.hexdigest()
    return hash_value
@app.route('/')
def index():
    return render_template('index.html')

<<<<<<< HEAD
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/causes')
def causes():
    return render_template('causes.html')
@app.route('/home')
def home():
    return render_template('index.html')
@app.route('/contact')
def contact():
    return render_template('contact.html')
@app.route('/event')
def event():
    return render_template('event.html')

app.run(debug=True)
=======
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/api/<slog>',methods=['POST'])
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

            dataBase  = mysql.connector.connect(host="localhost", user="root", password="", database="betterworld")
            cursorObject  = dataBase.cursor()
            data = (name,username,email,phone,city,hash_pas)
            cursorObject.execute("INSERT INTO user (name, user_name, email, phone, city, password) VALUES (%s, %s, %s, %s, %s, %s)",data)
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
                    return redirect('/')      
            else:
                return "Wrong Password"
        else:
            return 'Direct Access To API is not allowed'

    else:
        return 'Direct Access To API is not allowed'





app.run(debug=True)
>>>>>>> 7d403c7cfa6287cba2bbec87694179e2b1faca74
