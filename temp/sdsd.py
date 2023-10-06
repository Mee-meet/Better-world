from flask import Flask, render_template, request,redirect,Response,make_response,session,url_for
from urllib.parse import urlparse, urlunparse
import hashlib
from datetime import time
import json
import os
from flask_mail import Mail
import base64
import ast
from imgurpython import ImgurClient
import base45
import glob
import openpyxl
import requests
from io import BytesIO
import mysql.connector
from flask_mail import Message
import threading
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import random
from datetime import timedelta

app = Flask(__name__)
data = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
sec = ''
for i in range(0,10):
    sec = sec + data[random.randint(0,35)]
app.secret_key = sec
limiter = Limiter(get_remote_address,app=app)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)
# Configure Flask-Mail


#OTHER FUNCTION START
def fetch_child_links(parent_id, cursor):
    query = f"SELECT * FROM home WHERE parent_id = '{parent_id}'"
    cursor.execute(query)
    child_links = cursor.fetchall()

    for link in child_links:
        link['children'] = fetch_child_links(link['id'], cursor)

    return child_links




def fetch_child_links_products(parent_id, cursor):
    query = f"SELECT * FROM products WHERE navid = {parent_id}"
    cursor.execute(query)
    child_links = cursor.fetchall()

    for link in child_links:
        link['children'] = fetch_child_links(link['id'], cursor)

    return child_links


def calculate_md5(string):
    md5_hash = hashlib.md5()
    md5_hash.update(string.encode('utf-8'))
    return md5_hash.hexdigest()


def send_mail(ip):
        with open("static/cred/cred.json","r") as c:
            creds = c.read()
        data = json.loads(creds)
        temp = data["jbdjsbdjsbd"]
        base1 = base45.b45decode(temp.encode()).decode()
        base2 = base64.b85decode(base1.encode()).decode()
        app.config['MAIL_SERVER'] = 'smtp.gmail.com'
        app.config['MAIL_PORT'] = 587
        app.config['MAIL_USE_TLS'] = True
        app.config['MAIL_USERNAME'] = 'cnjinst03@gmail.com'
        app.config['MAIL_PASSWORD'] = base2        
        app.config['MAIL_DEFAULT_SENDER'] = 'cnjinst03@gmail.com'
        mail = Mail(app)
        recipient = 'cnjinst03@gmail.com'
        subject = 'Alert ⚠️'
        body = f'''<!DOCTYPE html>
<html>
<head>
    <title>Login Page Access Alert</title>
</head>
<body style="font-family: Arial, sans-serif; background-color: #f5f5f5; padding: 20px;">
    <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border: 1px solid #cccccc; border-radius: 4px; padding: 20px;">
        <h2 style="color: #333333;">Login Page Access Alert</h2>
        <p style="color: #555555; line-height: 1.5;">Someone is trying to access the login page.</p>
        <p style="color: #555555; line-height: 1.5;">IP Address:{ip}</p>
        <p style="color: #555555; line-height: 1.5;">Please take appropriate action to ensure the security of your account.</p>
    </div>
</body>
</html>
'''
        message = Message(subject=subject, recipients=[recipient], html=body)
        try:
            mail.send(message)
        except Exception as e:
            pass

      






#END

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404



@app.route('/')
def index():
        success = request.args.get('success')
        emailexists = request.args.get('emailexists')
        subscription = request.args.get('subscription')
        try:
            dataBase  = mysql.connector.connect(host="localhost", user="root", password="", database="cnjinst")
            cursorObject  = dataBase.cursor()
            cursorObject.execute("SELECT * FROM HOME")
            data = cursorObject.fetchall()
            cursorObject.execute("SELECT * FROM products where sub_sub_category !='Yes' order by id desc limit 4")
            slidebar = cursorObject.fetchall()
            sql = "SELECT * FROM products where sub_sub_category !='Yes' ORDER BY id DESC LIMIT 5"
            cursorObject.execute(sql)
            listing_data = cursorObject.fetchall()
            return render_template('index.html', data=data,slidebar=slidebar,success=success,emailexists=emailexists,subscription=subscription,listing_data=listing_data)
        except mysql.connector.Error as error:
            # Handle the database connection error
            print(f"Database Error: {error}")
            return redirect('/')
        finally:
            cursorObject.close()
            dataBase.close()
            return render_template('index.html',data=data,slidebar=slidebar,success=success,emailexists=emailexists,subscription=subscription,listing_data=listing_data)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        username = calculate_md5(username)
        password=  calculate_md5(password)
        with open("static/cred/cred.json","r") as c:
            creds = c.read()
        data = json.loads(creds)
        if data["username"]  == str(username) and str(data["password"]) == password:
            print("Login Successfull")
            session['username'] = 'dilip shah admin'
            session['login'] = True            
            return redirect('cygfngfynnyfgygfyfc456789fdffdbhfdbhfdjbhf')
        else:
            print("bad creds")     
            session['login'] = False      
            return redirect('admin?counter=1')
    
    return render_template('admin.html')

@app.route('/alretmailsenderemergancy',methods=['GET','POST'])
# @limiter.limit('3 per day')
def alerter():  
    if request.method == "POST":
        print("IP ADDRESS ISSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS", request.remote_addr)
        # send_mail(request.remote_addr)
    return 'Method Not Allowed'
    


@app.route('/cygfngfynnyfgygfyfc456789fdffdbhfdbhfdjbhf')
def cygfngfynnyfgygfyfc456789fdffdbhfdbhfdjbhf():
    if session.get('username') == 'dilip shah admin' and session.get('login') == True:
        try:
            dataBase  = mysql.connector.connect(host="localhost", user="root", password="", database="cnjinst")
            cursorObject  = dataBase.cursor()
            cursorObject.execute("SELECT * FROM HOME")
            data = cursorObject.fetchall()
            cursorObject.execute("SELECT * FROM `subscription` LIMIT 5;")
            emails = cursorObject.fetchall()
            cursorObject.execute("SELECT * FROM products")
            allproducts = cursorObject.fetchall()
            cursorObject.execute("SELECT * FROM `subscription`")
            emailscount = cursorObject.fetchall()
            emailscount = cursorObject.rowcount            
            cursorObject.close()
            slog_exist= request.args.get('slog_exist')
# product_added
            product_added= request.args.get('product_added')
            # slog= request.args.get('slog')


     
            return render_template('cygfngfynnyfgygfyfc456789fdffdbhfdbhfdjbhf.html', data=data,emails=emails,emailscount=emailscount,slog_exist=slog_exist,product_added=product_added,allproducts=allproducts)
        except mysql.connector.Error as error:
            # Handle the database connection error
            print(f"Database Error: {error}")
            return redirect('/admin')
        finally:
            cursorObject.close()
            dataBase.close()
    else:
        return redirect('/admin')


@app.template_global()
def get_children(parent_id):
    conn = mysql.connector.connect(host="localhost", username="root", password="", database="cnjinst")
    cur = conn.cursor()
    cur.execute("SELECT * FROM home WHERE parent_id = %s", (parent_id,))
    children = cur.fetchall()
    cur.close()
    conn.close()
    return children













@app.route('/cygfngfynnyfgygfyfc456789submit',methods=['POST'])
def cygfngfynnyfgygfyfc456789fdffdbhfdbhfdjbhfsubmit():
    if request.method == "POST":
        if session.get('username') == 'dilip shah admin' and session.get('login') == True:
            whichfrom = request.form.get('whichfrom')
            if whichfrom == "add":
                addlabelname = request.form.get('addlabelname')
                addurl = request.form.get('addurl')
                addparentid = request.form.get('addparentid')
                try:

                    dataBase  = mysql.connector.connect(host="localhost", user="root", password="", database="cnjinst")
                    cursorObject  = dataBase.cursor()
                    data = (addlabelname,addurl,addparentid)
                    sql = "INSERT INTO home (label, url, parent_id) VALUES (%s, %s, %s)"
                    cursorObject.execute(sql,data)
                    dataBase.commit()
                    return redirect('/cygfngfynnyfgygfyfc456789fdffdbhfdbhfdjbhf')
                except mysql.connector.Error as error:
                    # Handle the database connection error
                    print(f"Database Error: {error}")
                    return redirect('/cygfngfynnyfgygfyfc456789fdffdbhfdbhfdjbhf')
                finally:
                    cursorObject.close()
                    dataBase.close()

            if whichfrom == "update":
                updateid = request.form.get('updateid')
                updatelabel = request.form.get('updatelabel')
                updateurl = request.form.get('updateurl')
                updateparentid = request.form.get('updateparentid')




                try:

                    dataBase  = mysql.connector.connect(host="localhost", user="root", password="", database="cnjinst")
                    cursorObject  = dataBase.cursor()
                    data = (updatelabel,updateurl,updateparentid,updateid)
                    sql = "UPDATE home SET label = %s,url = %s,parent_id=%s WHERE id = %s;"
                    cursorObject.execute(sql,data)
                    dataBase.commit()
                    return redirect('/cygfngfynnyfgygfyfc456789fdffdbhfdbhfdjbhf')
                except mysql.connector.Error as error:
                    # Handle the database connection error
                    print(f"Database Error: {error}")
                    return redirect('/cygfngfynnyfgygfyfc456789fdffdbhfdbhfdjbhf')
                finally:
                    cursorObject.close()
                    dataBase.close()

            if whichfrom == "delete":
                deleteid = request.form.get('deleteid')

                try:

                    dataBase  = mysql.connector.connect(host="localhost", user="root", password="", database="cnjinst")
                    cursorObject  = dataBase.cursor()
                    data = (deleteid,)
                    sql = "DELETE FROM home WHERE id = %s"
                    cursorObject.execute(sql,data)
                    dataBase.commit()
                    return redirect('/cygfngfynnyfgygfyfc456789fdffdbhfdbhfdjbhf')
                except mysql.connector.Error as error:
                    # Handle the database connection error
                    print(f"Database Error: {error}")
                    return redirect('/cygfngfynnyfgygfyfc456789fdffdbhfdbhfdjbhf')
                finally:
                    cursorObject.close()
                    dataBase.close()

            if whichfrom == "instrumentadd":
                file_pattern = 'static/temp_images/*'
                file_list = glob.glob(file_pattern)
                for file_path in file_list:
                    os.remove(file_path)
                temp_files = []
                
                title = request.form.get('title')
                navid = int(request.form.get('navid'))
                files = request.form.get('files')
                description = request.form.get('description')
                specification = request.form.get('specification')
                files1 = request.files.getlist('files')
                print("my files areeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",files)
              # Imgur API credentials
                CLIENT_ID = '3d2201c3a9fb502'
                CLIENT_SECRET = '3e9b4e7e0b41542cbef90e53a32812093d086909'
                REFRESH_TOKEN = 'a11a722549fea11022e016d809f570c49f030f5b'

                # Token URL
                token_url = 'https://api.imgur.com/oauth2/token'

                # Request data
                data = {
                    'client_id': CLIENT_ID,
                    'client_secret': CLIENT_SECRET,
                    'grant_type': 'refresh_token',
                    'refresh_token': REFRESH_TOKEN
                }

                # Send the POST request to generate access token
                response = requests.post(token_url, data=data)

                # Check the response status code
                if response.status_code == 200:
                    # Successful response
                    token_data = response.json()
                    access_token = token_data['access_token']
                    print('Access Token:', access_token)
                else:
                    # Failed response
                    print('Failed to generate access token')

                for file in files1:
                    save_path = os.path.join('static/temp_images', file.filename)
                    with open(save_path, 'wb') as f:
                        f.write(file.read())



                myfiles_in_temp = os.listdir('static/temp_images')
                for file in myfiles_in_temp:
                        client_id = '3d2201c3a9fb502'
                        client_secret = '3e9b4e7e0b41542cbef90e53a32812093d086909'
                        access_token = access_token
                        refresh_token = 'a11a722549fea11022e016d809f570c49f030f5b'

                        client = ImgurClient(client_id, client_secret, access_token, refresh_token)
                        image_path = f'static/temp_images/{file}'
                        image = client.upload_from_path(image_path,anon=False)
                        image_url = image['link']
                        print("Image uploaded successfully! URL:", image_url)

                        temp_files.append(image_url)
                    
                file_pattern = 'static/temp_images/*'
                file_list = glob.glob(file_pattern)
                for file_path in file_list:
                    os.remove(file_path)

                temp_files = str(temp_files)


                specification = str(specification.split(','))
                slog  = title.replace(' ','-')
                slog  = slog.replace('/','-')
                slog  = slog.replace('!','-')
                slog  = slog.replace(')','-')
                slog  = slog.replace('\\','-')
                slog  = slog.replace('(','-')

                try:
                    dataBase  = mysql.connector.connect(host="localhost", user="root", password="", database="cnjinst")
                    cursorObject  = dataBase.cursor()
                    data = (slog,)
                    sql = "SELECT * FROM PRODUCTS WHERE slog = %s"
                    cursorObject.execute(sql,data)
                    temp = cursorObject.fetchall()
                    if cursorObject.rowcount > 0:
                        redirect_url = url_for('cygfngfynnyfgygfyfc456789fdffdbhfdbhfdjbhf', slog_exist="True")
                        return redirect(redirect_url)    

                    data = (title,navid,description,specification,slog,temp_files,'No')
                    sql = "INSERT INTO products (title,navid, description, specification, slog,images,sub_sub_category) VALUES (%s, %s, %s, %s, %s,%s,%s)"
                    cursorObject.execute(sql,data)
                    dataBase.commit()

                except Exception as error:
                    redirect_url = url_for('cygfngfynnyfgygfyfc456789fdffdbhfdbhfdjbhf', product_added="False",slog=slog)
                    print(error)
                    return redirect(redirect_url)
                else:
                    redirect_url = url_for('cygfngfynnyfgygfyfc456789fdffdbhfdbhfdjbhf', product_added=slog)
                    return redirect(redirect_url)
                finally:
                    dataBase.close()
                    cursorObject.close()

        
            if whichfrom == "industryadd":
                title = str(request.form.get('title'))
                description =request.form.get('description')
                navid = request.form.get('navid')
                hastag = title.replace(' ','-')
                dataBase  = mysql.connector.connect(host="localhost", user="root", password="", database="cnjinst")
                cursorObject  = dataBase.cursor()
                data = (title,hastag)
                sql = "SELECT * FROM INDUSTRIES WHERE title = %s or hastag=%s"
                cursorObject.execute(sql,data)
                if cursorObject.rowcount > 0:
                    redirect_url = url_for('cygfngfynnyfgygfyfc456789fdffdbhfdbhfdjbhf', industry_exits = "True")
                    return redirect(redirect_url)
                cursorObject.fetchall()

                data = (title,description,hastag)
                sql = "insert into industries(title,description,hastag) values(%s,%s,%s)"
                cursorObject.execute(sql,data)
                dataBase.commit()
                data = ("/industries#" + hastag + "-content",int(navid))
                sql = "UPDATE home SET url = %s WHERE id = %s"
                cursorObject.execute(sql,data)
                dataBase.commit()
                return redirect("/cygfngfynnyfgygfyfc456789fdffdbhfdbhfdjbhf")
            if whichfrom == "industrydelete":
                hash = request.form.get("hash")
                dataBase  = mysql.connector.connect(host="localhost", user="root", password="", database="cnjinst")
                cursorObject  = dataBase.cursor()
                data = (hash,)
                sql = "DELETE FROM industries WHERE hastag = %s"
                cursorObject.execute(sql,data)
                dataBase.commit()
                return redirect("/cygfngfynnyfgygfyfc456789fdffdbhfdbhfdjbhf")
            if whichfrom == 'categoryadd':
                categoryname = request.form.get("categoryname")
                categoryparent = request.form.get("categoryparent")
                slog  = categoryname.replace(' ','-')
                slog  = slog.replace('/','-')
                slog  = slog.replace('!','-')
                slog  = slog.replace(')','-')
                slog  = slog.replace('\\','-')


                dataBase  = mysql.connector.connect(host="localhost", user="root", password="", database="cnjinst")
                cursorObject  = dataBase.cursor()
                data = (categoryname,categoryparent,'Yes',slog)
                sql = "insert into products(`title`,`navid`, `sub_sub_category` ,`slog`) values(%s,%s,%s,%s)"
                cursorObject.execute(sql,data)
                dataBase.commit()
                return redirect("/cygfngfynnyfgygfyfc456789fdffdbhfdbhfdjbhf")


        else:
            return redirect('/admin')
        
        
    return 'Method Not Allowed'

















@app.route('/products/<slog>',methods=['GET'])
def products(slog):
        success = request.args.get('success')
        emailexists = request.args.get('emailexists')
        subscription = request.args.get('subscription')
        try:
            dataBase  = mysql.connector.connect(host="localhost", user="root", password="", database="cnjinst")
            cursorObject  = dataBase.cursor()
            
            cursorObject.execute("SELECT * FROM HOME")
            data = cursorObject.fetchall()
           
            # return render_template('products.html', data=data,success=success,emailexists=emailexists,subscription=subscription)
        except mysql.connector.Error as error:
            # Handle the database connection error
            pass
        finally:
            cursorObject.close()
            dataBase.close()
        



        # slog logic.
        try:
            dataBase  = mysql.connector.connect(host="localhost", user="root", password="", database="cnjinst")
            cursorObject  = dataBase.cursor()
            dataofslog = (slog,)
            cursorObject.execute("SELECT * FROM products where slog = %s",dataofslog)
            slog_data = cursorObject.fetchone()

            sql = "SELECT * FROM products where sub_sub_category !='Yes' ORDER BY id DESC LIMIT 5"
            cursorObject.execute(sql)
            listing_data = cursorObject.fetchall()
            sql = "SELECT * FROM products where sub_sub_category !='Yes' LIMIT 7"
            cursorObject.execute(sql)
            slideshow_data = cursorObject.fetchall()
            
            cursorObject.execute("SELECT * FROM products where sub_sub_category !='Yes' order by id desc limit 4")
            slidebar = cursorObject.fetchall()
            cursorObject.close() 

            cursorObject.close()
            images_slog = ast.literal_eval(slog_data[2])
            specification_slog = ast.literal_eval(slog_data[4])

     
            return render_template('products.html', data=data,success=success,emailexists=emailexists,subscription=subscription,slog_data=slog_data,images_slog=images_slog,specification_slog=specification_slog,listing_data=listing_data,slideshow_data=slideshow_data,slidebar=slidebar)
        except mysql.connector.Error as error:
            # Handle the database connection error
            pass
        finally:
            cursorObject.close()
            dataBase.close()
        


            return render_template('products.html',data=data,success=success,emailexists=emailexists,subscription=subscription,slog_data=slog_data,images_slog=images_slog,specification_slog=specification_slog,listing_data=listing_data,slideshow_data=slideshow_data,slidebar=slidebar)




@app.route('/send-enquiry',methods=['POST'])
def send_enquiry():
        if request.method == "POST":
            hiddenurl = str(request.form.get('hiddenurl'))
            name = request.form.get('name')
            email = request.form.get('email')
            website = request.form.get('website')
            message = request.form.get('message')
            with open("static/cred/cred.json","r") as c:
                creds = c.read()
            data = json.loads(creds)
            temp = data["jbdjsbdjsbd"]
            base1 = base45.b45decode(temp.encode()).decode()
            base2 = base64.b85decode(base1.encode()).decode()
            app.config['MAIL_SERVER'] = 'smtp.gmail.com'
            app.config['MAIL_PORT'] = 587
            app.config['MAIL_USE_TLS'] = True
            app.config['MAIL_USERNAME'] = 'cnjinst03@gmail.com'
            app.config['MAIL_PASSWORD'] = base2        
            app.config['MAIL_DEFAULT_SENDER'] = 'cnjinst03@gmail.com'
            mail = Mail(app)
            recipient = 'cnjinst03@gmail.com'
            subject = 'New Enquiry From C&J Insturments'
            body = f'''<!DOCTYPE html>
    <html>
    <head>
        <title>Login Page Access Alert</title>
    </head>
    <body style="font-family: Arial, sans-serif; background-color: #f5f5f5; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border: 1px solid #cccccc; border-radius: 4px; padding: 20px;">
            <h2 style="color: #333333;">New Enquiry From C&J Insturments</h2>
            <p style="color: #555555; line-height: 1.5;">Url: {hiddenurl}</p>
            <p style="color: #555555; line-height: 1.5;">Name: {name}</p>
            <p style="color: #555555; line-height: 1.5;">Email: {email}</p>
            <p style="color: #555555; line-height: 1.5;">Website: {website}</p>

        </div>
    </body>
    </html>
    '''
            message = Message(subject=subject, recipients=[recipient], html=body)
            hiddenurl = urlparse(hiddenurl)
            hiddenurl = hiddenurl._replace(query='')
            hiddenurl = urlunparse(hiddenurl)
            try:
                mail.send(message)
            except Exception as e:
                pass
            else:
                return redirect(hiddenurl + "?success=True")     








        return 'Method Not Allowed'



















@app.route('/subscribe-newsletter',methods=['POST'])
def subscribe_newsletter():
        if request.method == "POST":
            hiddenurl = str(request.form.get('hiddenurl'))
            email = request.form.get('email')
            try:

                    dataBase  = mysql.connector.connect(host="localhost", user="root", password="", database="cnjinst")
                    cursorObject  = dataBase.cursor()
                    data = (email,)
                    sql = "SELECT * FROM subscription where email = %s"
                    cursorObject.execute(sql,data)
                    data1 = cursorObject.fetchone()

                    rownum = cursorObject.rowcount
                    if rownum>0:
                        hiddenurl = urlparse(hiddenurl)
                        hiddenurl = hiddenurl._replace(query='')
                        hiddenurl = urlunparse(hiddenurl)
                        return redirect(hiddenurl + "?emailexists=True")
                    sql = "INSERT INTO subscription (email) VALUES (%s)"
                    cursorObject.execute(sql,data)
                    dataBase.commit()
                    hiddenurl = urlparse(hiddenurl)
                    hiddenurl = hiddenurl._replace(query='')
                    hiddenurl = urlunparse(hiddenurl)
                    return redirect(hiddenurl + "?subscription=True")
            finally:
                    cursorObject.close()
                    dataBase.close()

            

















@app.route('/download-subscription-emails',methods=['POST'])
def download():
    if request.method == "POST":
        if session.get('username') == 'dilip shah admin' and session.get('login') == True:

            # Connect to your MySQL database
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='cnjinst'
            )

            # Retrieve data from the database
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM subscription')
            data = cursor.fetchall()

            # Create an Excel workbook and sheet
            wb = openpyxl.Workbook()
            sheet = wb.active

            # Write the data to the sheet
            for row in data:
                sheet.append(row)

            # Save the workbook in memory
            in_memory_file = BytesIO()
            wb.save(in_memory_file)
            in_memory_file.seek(0)

            # Close the database connection
            cursor.close()
            connection.close()

            # Create a response with the Excel file
            response = make_response(in_memory_file.getvalue())
            response.headers['Content-Disposition'] = 'attachment; filename=subscription.xlsx'
            response.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

            return response




















@app.route('/contact',methods=['GET','POST'])
def contact():

        send = request.args.get('send')
        if request.method == "POST":
            name = request.form.get('name')
            email = request.form.get('email')
            subject_form = request.form.get('subject')
            message = request.form.get('message')

            name = request.form.get('name')
            with open("static/cred/cred.json","r") as c:
                creds = c.read()
            data = json.loads(creds)
            temp = data["jbdjsbdjsbd"]
            base1 = base45.b45decode(temp.encode()).decode()
            base2 = base64.b85decode(base1.encode()).decode()
            app.config['MAIL_SERVER'] = 'smtp.gmail.com'
            app.config['MAIL_PORT'] = 587
            app.config['MAIL_USE_TLS'] = True
            app.config['MAIL_USERNAME'] = 'cnjinst03@gmail.com'
            app.config['MAIL_PASSWORD'] = base2        
            app.config['MAIL_DEFAULT_SENDER'] = 'cnjinst03@gmail.com'
            mail = Mail(app)
            recipient = 'cnjinst03@gmail.com'
            subject = 'Contact Form From C&JInstruments'
            body = f'''<!DOCTYPE html>
    <html>
    <head>
        <title>Contact Form</title>
    </head>
    <body style="font-family: Arial, sans-serif; background-color: #f5f5f5; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border: 1px solid #cccccc; border-radius: 4px; padding: 20px;">
            <h2 style="color: #333333;">Contact Form Enquiry</h2>
            <p style="color: #555555; line-height: 1.5;">Name: {name}</p>
            <p style="color: #555555; line-height: 1.5;">Email: {email}</p>
            <p style="color: #555555; line-height: 1.5;">Subject: {subject_form}</p>
            <p style="color: #555555; line-height: 1.5;">Message: {message}</p>


        </div>
    </body>
    </html>
    '''
            message = Message(subject=subject, recipients=[recipient], html=body)
            try:
                mail.send(message)
            except Exception as e:
                return redirect('contact?send=False')

            else:
                return redirect('contact?send=True')



        try:
            dataBase  = mysql.connector.connect(host="localhost", user="root", password="", database="cnjinst")
            cursorObject  = dataBase.cursor()
            
            cursorObject.execute("SELECT * FROM HOME")
            data = cursorObject.fetchall()
            cursorObject.execute("SELECT * FROM products where sub_sub_category !='Yes' order by id desc limit 4")
            slidebar = cursorObject.fetchall()
            cursorObject.close()
            return render_template('contact.html',data=data,send=send,slidebar=slidebar)
     
        except mysql.connector.Error as error:
            # Handle the database connection error
            pass
        finally:
            cursorObject.close()
            dataBase.close()






















@app.route('/about-us',methods=['GET','POST'])
def aboutus():
        success = request.args.get('success')
        try:
            dataBase  = mysql.connector.connect(host="localhost", user="root", password="", database="cnjinst")
            cursorObject  = dataBase.cursor()
            
            cursorObject.execute("SELECT * FROM HOME")
            data = cursorObject.fetchall()
            cursorObject.execute("SELECT * FROM products where sub_sub_category !='Yes' order by id desc limit 4")
            slidebar = cursorObject.fetchall()
            cursorObject.close()
            return render_template('aboutus.html',data=data,success=success,slidebar=slidebar)
     
        except mysql.connector.Error as error:
            # Handle the database connection error
            pass
        finally:
            cursorObject.close()
            dataBase.close()

        return render_template('aboutus.html',data=data,success=success,slidebar=slidebar)


@app.route('/results',methods=['GET','POST'])
def results():
        try:
            dataBase  = mysql.connector.connect(host="localhost", user="root", password="", database="cnjinst")
            cursorObject  = dataBase.cursor()
            
            cursorObject.execute("SELECT * FROM HOME")
            data = cursorObject.fetchall()
            cursorObject.execute("SELECT * FROM products where sub_sub_category !='Yes' order by id desc limit 4")
            slidebar = cursorObject.fetchall()
            # return render_template('aboutus.html',data=data)
     
        except mysql.connector.Error as error:
            # Handle the database connection error
            pass
        finally:
            cursorObject.close()
            dataBase.close()

        query = request.form.get('query')
        if request.method == "POST":
            dataBase  = mysql.connector.connect(host="localhost", user="root", password="", database="cnjinst")
            cursorObject  = dataBase.cursor()
            data_queiry = (query,query,query,query,query)
            sql = '''
            SELECT *
            FROM products
            WHERE (title LIKE CONCAT('%%', %s, '%%')
            OR images LIKE CONCAT('%%', %s, '%%')
            OR description LIKE CONCAT('%%', %s, '%%')
            OR specification LIKE CONCAT('%%', %s, '%%')
            OR slog LIKE CONCAT('%%', %s, '%%'))
            AND NOT(sub_sub_category = 'Yes' or navid='none')
            LIMIT 10
            '''


            cursorObject.execute(sql,data_queiry)
            search_result = cursorObject.fetchall()
            # print(search_result)
            cursorObject.close()
            dataBase.close()
            return render_template('search.html',direct="True",data=data,slidebar=slidebar,query= query,search_result=search_result)
            
    
        return render_template('search.html',direct="True",data=data,slidebar=slidebar)














@app.route('/products',methods=['GET','POST'])
def products_listing():
        
        try:
            dataBase  = mysql.connector.connect(host="localhost", user="root", password="", database="cnjinst")
            cursorObject  = dataBase.cursor()
            
            cursorObject.execute("SELECT * FROM HOME")
            data = cursorObject.fetchall()
            cursorObject.execute("SELECT * FROM products where sub_sub_category !='Yes' order by id desc limit 4")
            slidebar = cursorObject.fetchall()

            # products listing
            cursor = dataBase.cursor(dictionary=True)

            query = "SELECT * FROM products"
            cursor.execute(query)
            navbar_links = cursor.fetchall()

            # Fetch child links for each parent link
            for link in navbar_links:
                # print(navbar_links)
                link['children'] = fetch_child_links_products(link['id'], cursor)

            # return render_template('aboutus.html',data=data)
            # print(navbar_links)
            # return render_template('aboutus.html',data=data)
     
        except mysql.connector.Error as error:
            # Handle the database connection error
            pass
        finally:
            cursorObject.close()
            dataBase.close()



        try:
            dataBase  = mysql.connector.connect(host="localhost", user="root", password="", database="cnjinst")
            cursorObject  = dataBase.cursor()
            sql = "SELECT * FROM products where sub_sub_category !='Yes' ORDER BY id DESC LIMIT 5"
            cursorObject.execute(sql)
            listing_data = cursorObject.fetchall()
            
            # cursorObject.execute("SELECT * FROM products order by id LIMIT 2,2")
            # product_listing = cursorObject.fetchall()
            # return render_template('aboutus.html',data=data)
     
        except mysql.connector.Error as error:
            # Handle the database connection error
            pass
        finally:
            cursorObject.close()
            dataBase.close()
        



    
        return render_template('product_listing.html',direct="True",data=data,slidebar=slidebar,navbar_links=navbar_links,listing_data=listing_data)




@app.route('/industries',methods=['GET','POST'])
def industries():
        try:
            dataBase  = mysql.connector.connect(host="localhost", user="root", password="", database="cnjinst")
            cursorObject  = dataBase.cursor()
            
            cursorObject.execute("SELECT * FROM HOME")
            data = cursorObject.fetchall()
            cursorObject.execute("SELECT * FROM products where sub_sub_category !='Yes' order by id desc limit 4")
            slidebar = cursorObject.fetchall()
            cursorObject.execute("SELECT * FROM industries")
            industries = cursorObject.fetchall()



            cursor = dataBase.cursor(dictionary=True)

            # Fetch navbar links from the database
            query = "SELECT * FROM home WHERE parent_id = '17'"
            cursor.execute(query)
            navbar_links = cursor.fetchall()

            # Fetch child links for each parent link
            for link in navbar_links:
                # print(navbar_links)
                link['children'] = fetch_child_links(link['id'], cursor)

            # return render_template('aboutus.html',data=data)
           
     
        except mysql.connector.Error as error:
            # Handle the database connection error
            pass
        finally:
            cursorObject.close()
            dataBase.close()

        


    
        return render_template('industries.html',direct="True",data=data,slidebar=slidebar,navbar_links=navbar_links,industries=industries)






app.run(debug=True)
