from flask import Flask,render_template,request,redirect
import mysql.connector
import os
from imgurpython import ImgurClient
import requests
import glob


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

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
            file_pattern = 'static/temp_images/*'
            file_list = glob.glob(file_pattern)
            for file_path in file_list:
                os.remove(file_path)
            temp_files = []

            name = request.form.get('name')
            username = request.form.get('username')
            email = request.form.get('email')
            phone = request.form.get('phone')
            email = request.form.get('email')
            city = request.form.get('city')
            password = request.form.get('password')
            profile = request.files.getlist('files')
            imgur_urls = []

            client_id = '30ff7f70bc4036d'  # Replace with your Imgur client ID
            url = 'https://api.imgur.com/3/image'
            headers = {
                'Authorization': f'Client-ID {client_id}'
            }

            # Create an empty list to store the Imgur URLs
            imgur_urls = []

            # Loop through the uploaded files in 'profile'
            for file in request.files.getlist('files'):
                with open(file.filename, 'rb') as f:
                    files = {'image': (file.filename, f)}
                    response = requests.post(url, headers=headers, files=files)

                if response.status_code == 200:
                    # Image uploaded successfully
                    imgur_data = response.json()
                    imgur_url = imgur_data['data']['link']
                    imgur_urls.append(imgur_url)
                    print("Image uploaded. Imgur URL:", imgur_url)
                else:
                    print("Image upload failed. Status code:", response.status_code)
                    print(response.text)

            # Now imgur_urls contains the list of Imgur URLs for the uploaded images
            actual_url = ''
            for i in imgur_urls:
                actual_url = actual_url + i

            dataBase  = mysql.connector.connect(host="localhost", user="root", password="", database="betterworld")
            cursorObject  = dataBase.cursor()
            data = (name,username,email,phone,city,actual_url,password)
            cursorObject.execute("INSERT INTO user (name, user_name, email, phone, city, profile_photo, password) VALUES (%s, %s, %s, %s, %s, %s, %s)",data)
            dataBase.commit()
            return 'Data successfully processed'  # Add a response for POST requests
    else:
        return 'Direct Access To API is not allowed'



app.run(debug=True)