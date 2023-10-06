import requests

client_id = '30ff7f70bc4036d'  # Replace with your Imgur client ID

# Endpoint for image upload
url = 'https://api.imgur.com/3/image'

headers = {
    'Authorization': f'Client-ID {client_id}'
}

with open('static/images/bg_1.jpg', 'rb') as f:
    files = {'image': ('static/images/bg_1.jpg', f)}
    response = requests.post(url, headers=headers, files=files)

if response.status_code == 200:
    # Image uploaded successfully
    imgur_data = response.json()
    print("Image uploaded. Imgur URL:", imgur_data['data']['link'])
else:
    print("Image upload failed. Status code:", response.status_code)
    print(response.text)
