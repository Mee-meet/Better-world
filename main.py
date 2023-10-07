from flask import Flask,render_template,request,redirect,session
import mysql.connector
from urllib.parse import urlparse
import os
import hashlib
from imgurpython import ImgurClient
import requests
from flask_session import Session
import glob
from jinja2 import Environment, BaseLoader
import json
import ast


app = Flask(__name__)
app.secret_key = 'ihyfhbhbfrfbiihrewuibwe5436889'

@app.template_filter('string_to_list')
def string_to_list(s):
    return s.split(',')

def compute_sha256_hash(data):

    sha256_hash = hashlib.sha256()
    if isinstance(data, str):
        data = data.encode('utf-8')

    sha256_hash.update(data)
    hash_value = sha256_hash.hexdigest()
    return hash_value


@app.route('/logout')
def logout():
    try:
        session.clear()
    except:
        return redirect('/')
    
    return redirect('/')

@app.route('/super_admin2')
def super_admin2():
    return render_template("admin_2.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/petition')
def petition():
    try:
        if session['user_data']:
            show_login_signup="False"
            role = session['user_data']['role']
            if role == "user":

                dataBase  = mysql.connector.connect(host="localhost", user="root", password="", database="betterworld")
                cursorObject  = dataBase.cursor()
                cursorObject.execute("select * from petition")
                events = cursorObject.fetchall()
                print(events)
                return render_template('petition.html', show_login_signup=show_login_signup,events=events)

        else:
            print("hhhhhh")
            show_login_signup="True"
        return render_template('petition.html',show_login_signup=show_login_signup,role=role)

    except Exception as e:
        print(e)
        return render_template('petition.html', show_login_signup=show_login_signup, role=role)

@app.route('/super_admin')
def super_admin():


            dataBase = mysql.connector.connect(host="localhost", user="root", password="", database="betterworld")
            cursorObject = dataBase.cursor()


            cursorObject.execute("select * from organization")
            data = cursorObject.fetchall()
            cursorObject.execute("select * from user")
            data2 = cursorObject.fetchall()
            cursorObject.execute("select * from community")
            community = cursorObject.fetchall()
            cursorObject.execute("select * from petition")
            petition = cursorObject.fetchall()

            return render_template('super_admin.html',event_data=data,event_data2=data2,community=community,petition=petition)

@app.route('/community/<slog1>/<slog2>',methods=['GET','POST'])
def community_chatting(slog1, slog2):
        invite = request.args.get('invite')
        url = request.args.get('url')

        if invite == "True":
            if session['user_data']:
                dataBase = mysql.connector.connect(host="localhost", user="root", password="", database="betterworld")
                cursorObject = dataBase.cursor()
                # http://127.0.0.1:5000/community/fulijipyv@mailinator.com/tyvapesi@mailinator.com?invite=True
                url = url.replace("http://127.0.0.1:5000/community/",'')
                url = url.replace("?invite=True",'')
                newlist = url.split('/')




                data = (session['user_data']['email'],)
                cursorObject.execute("select user_name from user where email=%s",data)
                user_user_name = cursorObject.fetchone()
                data = (session['user_data']['email'],user_user_name[0],newlist[1],newlist[0])
                cursorObject.execute("INSERT INTO community_members (email, username, name_of_community, email_of_community) VALUES (%s, %s, %s, %s)",data)
                dataBase.commit()
                data = (newlist[0],)
                
            else:
                return 'Login First To Join The Community'
        
        
        
        dataBase = mysql.connector.connect(host="localhost", user="root", password="", database="betterworld")
        cursorObject = dataBase.cursor()
        data = (slog2,slog1)
        cursorObject.execute("select * from community_messages where community_name = %s  and community_email=  %s",data)
        messages =cursorObject.fetchall()
        is_admin = False
        data = (slog1,slog2)
        cursorObject.execute("select cname from community where email = %s  and cname=%s",data)
        is_admin = "False"
        # total_rows = cursorObject.rowcount
        name_of_community = cursorObject.fetchone()
        if name_of_community:
            is_admin= "True"

    
        data = (slog1,)
        cursorObject.execute("select * from community_members where email_of_community=%s",data)
        members = cursorObject.fetchall()
        data = (slog1,)  
        cursorObject.execute("select * from petition where copy_email = %s",data)
        petition = cursorObject.fetchall()
        data = (slog1,)
        
        
        cursorObject.execute("select count(*) from community_members where  	email_of_community 	= %s",data)
        count_members = cursorObject.fetchall()
        

        return render_template('community_messages.html',messages=messages,is_admin=is_admin,name_of_community=name_of_community,email=slog1,cname=slog2,members=members,petition=petition,count_members=int(count_members[0][0]))


@app.route('/community')
def community():
    # try:
        show_login_signup = "False"
        if session['user_data']:
            roles = session['user_data']['role']
            email = session['user_data']['email']    
            if roles == "user" or roles == "org":
                    dataBase = mysql.connector.connect(host="localhost", user="root", password="", database="betterworld")
                    cursorObject = dataBase.cursor()
                    data = (email,)
                    cursorObject.execute("select * from community where email=%s",data)
                    his_own_community = cursorObject.fetchall()
                    cursorObject.execute("select * from community_members where email=%s",data)
                    other_community_joined = cursorObject.fetchall()
                    cursorObject.execute("select * from community_members where email_of_community=%s",data)
                    totla_member = cursorObject.rowcount

            return render_template("community.html",role=roles,other_community_joined=other_community_joined,his_own_community=his_own_community ,totla_member=totla_member)
        else:
            show_login_signup = "True"
        return render_template("community.html",show_login_signup=show_login_signup)
    # except:
        # return redirect('/')



@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/causes')
def causes():
    return render_template('causes.html')
@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/donate')
def donate():
    return render_template('donate.html')

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
                cursorObject.execute("select * from petition where copy_email=%s",email)
                petition = cursorObject.fetchall()
                return render_template('org_portal.html',name=data,event_data=event_data,petition=petition)
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
                print(interests)
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
                sql= 'SELECT * from events'
                cursorObject.execute(sql)
                events2 = cursorObject.fetchall()
            return render_template('event.html', show_login_signup=show_login_signup, role=role, email=email, events=events, events2=events2)

        else:
            print("hhhhhh")
            show_login_signup="True"
        return render_template('event.html',show_login_signup=show_login_signup,role=role,email=email)
    
    except Exception as e:
        print(e)
        return render_template('event.html', show_login_signup=show_login_signup, role=role, email=email)


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
            interests = ["hello","Programming","Cooking","Food Distribution","Cleaning","Old age home"]    
            actual_interest = []
            for i in range(0,6):
                if request.form.get(str(i)) == "on":
                    actual_interest.append(interests[i])
            actual_interest = str(actual_interest)

            dataBase  = mysql.connector.connect(host="localhost", user="root", password="", database="betterworld")
            cursorObject  = dataBase.cursor()
            data = (name,username,email,phone,city,hash_pas,actual_interest)
            cursorObject.execute("INSERT INTO user (name, user_name, email, phone, city, password,interest) VALUES (%s, %s, %s, %s, %s, %s,%s)",data)
            dataBase.commit()
            return redirect('/login')  # Add a response for POST requests



        elif slog == "petition_detail":
            title = request.form.get('title')
            cause= request.form.get('title2')
            date = request.form.get('date')
            description = request.form.get('description')
            email = session['user_data']['email']
            print(cause)

            dataBase = mysql.connector.connect(host="localhost", user="root", password="", database="betterworld")
            cursorObject = dataBase.cursor()
            data = (title,cause,description,date,email)
            cursorObject.execute("INSERT INTO petition (title, cause, description,last_date,copy_email) VALUES (%s, %s, %s, %s, %s)",data)
            dataBase.commit()
            return redirect('/org_portal')    
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


        elif slog == "create_community":
            cname = request.form.get('cname')
            email = request.form.get('email')
            phone = request.form.get('phone')
            motive  = request.form.get('motive')


            dataBase = mysql.connector.connect(host="localhost", user="root", password="", database="betterworld")
            cursorObject = dataBase.cursor()
            data = (cname,email,phone,motive)
            cursorObject.execute("INSERT INTO community (cname, email,phone , Motive) VALUES (%s, %s, %s, %s)",data)
            dataBase.commit()

            return redirect('/community')

        elif slog == "petition_detail_community":
                    title = request.form.get('title')
                    cause= request.form.get('title2')
                    date = request.form.get('date')
                    description = request.form.get('description')
                    email = session['user_data']['email']
                    print(cause)

                    dataBase = mysql.connector.connect(host="localhost", user="root", password="", database="betterworld")
                    cursorObject = dataBase.cursor()
                    data = (title,cause,description,date,email)
                    cursorObject.execute("INSERT INTO petition (title, cause, description,last_date,copy_email) VALUES (%s, %s, %s, %s, %s)",data)
                    dataBase.commit()
                    return redirect('/community')
        elif slog == "super_user":
            if request.form.get('username') == "root" and request.form.get('password') == "root":
                return redirect('super_admin')
            else:
                return 'Wrong Password'


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
    
            elif slog == "add_chat":
                dataBase = mysql.connector.connect(host="localhost", user="root", password="", database="betterworld")
                cursorObject = dataBase.cursor()
                msg = request.args.get('chat')
                community_email =session['user_data']['email']
                data = (community_email,)
                cursorObject.execute("select cname from community where email=%s",data)
                community_name = cursorObject.fetchone()
                print(community_name,community_email)
                data = (community_name[0],community_email,msg)
                cursorObject.execute("INSERT INTO community_messages (community_name,community_email,message) VALUES (%s, %s, %s)",data)
                dataBase.commit()

                return redirect(request.args.get('current_url'))
            
            

            elif slog == "super_admin_petition_delete":
                id = request.args.get("event")
                dataBase = mysql.connector.connect(host="localhost", user="root", password="", database="betterworld")
                cursorObject = dataBase.cursor()
                data = (str(id),)
                cursorObject.execute("delete from petition where id=%s",data)
                dataBase.commit()
                return redirect("/super_admin")




            elif slog == "community_petition_delete":
                id = request.args.get("event")
                dataBase = mysql.connector.connect(host="localhost", user="root", password="", database="betterworld")
                cursorObject = dataBase.cursor()
                data = (str(id),)
                cursorObject.execute("delete from petition where id=%s",data)
                dataBase.commit()
                return redirect("/community")




            elif slog == "petition_delete":
                id = request.args.get("event")
                dataBase = mysql.connector.connect(host="localhost", user="root", password="", database="betterworld")
                cursorObject = dataBase.cursor()
                data = (str(id),)
                cursorObject.execute("delete from petition where id=%s",data)
                dataBase.commit()
                return redirect("/org_portal")


            elif slog=="org_delete":
                id = request.args.get("event")
                dataBase = mysql.connector.connect(host="localhost", user="root", password="", database="betterworld")
                cursorObject = dataBase.cursor()
                data = (str(id),)
                cursorObject.execute("delete from organization where id=%s",data)
                dataBase.commit()
                return redirect("/super_admin")
            elif slog=="org_update":
                id = request.args.get("event")
                dataBase = mysql.connector.connect(host="localhost", user="root", password="", database="betterworld")
                cursorObject = dataBase.cursor()
                data = (str(id),)
                cursorObject.execute("update organization set admin=1 where id=%s",data)
                dataBase.commit()
                return redirect("/super_admin")
            elif slog=="user_delete":
                id = request.args.get("event")
                dataBase = mysql.connector.connect(host="localhost", user="root", password="", database="betterworld")
                cursorObject = dataBase.cursor()
                data = (str(id),)
                cursorObject.execute("delete from user where id=%s",data)
                dataBase.commit()
                return redirect("/super_admin")
            elif slog=="community_delete":
                id = request.args.get("event")
                dataBase = mysql.connector.connect(host="localhost", user="root", password="", database="betterworld")
                cursorObject = dataBase.cursor()
                data = (str(id),)
                cursorObject.execute("delete from community where id=%s",data)
                dataBase.commit()   
                return redirect("/super_admin")
        return 'Direct Access To API is not allowed'



@app.route('/event/<slog>')
def eventtt(slog):
    dataBase = mysql.connector.connect(host="localhost", user="root", password="", database="betterworld")
    cursorObject = dataBase.cursor()
    data = (str(slog),)
    cursorObject.execute("select * from events where id = %s",data)
    event_detail = cursorObject.fetchall()
    return render_template('actual_event.html',event_detail=event_detail)



@app.route('/event_registration/<slog>',methods = ['GET','POST'])
def eventdfdftt(slog):
    
            dataBase = mysql.connector.connect(host="localhost", user="root", password="", database="betterworld")
            cursorObject = dataBase.cursor()
            data = (str(slog),session['user_data']['email'])
            cursorObject.execute("INSERT INTO event_members (id_event, id_email) VALUES (%s, %s)",data)
            dataBase.commit()
    
            return redirect('/event')








@app.route('/user/profile/<slog>',methods = ['GET','POST'])
def profile(slog):
    
            dataBase = mysql.connector.connect(host="localhost", user="root", password="", database="betterworld")
            cursorObject = dataBase.cursor()
            data = (session['user_data']['email'],)
            cursorObject.execute("select * from user where email = %s",data)
            mydata = cursorObject.fetchall()


            data = (session['user_data']['email'],)
            cursorObject.execute("select id_event from event_members where id_email = %s",data)
            events = cursorObject.fetchall()
            actual_events =[]
            for i in events:
                data = (i[0],)
                cursorObject.execute("select * from events where id  = %s",data)
                actual_events.append(cursorObject.fetchall())
            return render_template('profile.html',mydata=mydata,events=actual_events)






@app.route('/sign_petition/<slog>',methods = ['GET','POST'])
def ksnfjknfjd(slog):
    if session['user_data']:
        dataBase = mysql.connector.connect(host="localhost", user="root", password="", database="betterworld")
        cursorObject = dataBase.cursor()
        sql = "UPDATE petition SET no_user = no_user+1 WHERE petition.id = %s"   

        data = (slog,)
        cursorObject.execute(sql,data)
      
        dataBase.commit()
        return "Petition Signed Successfully"
        
    else:
         return "Login To Sign The Petition"        
        





app.run(debug=True)
