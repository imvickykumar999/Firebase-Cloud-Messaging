from flask import Flask, render_template, request, jsonify
import json
import requests
from google.oauth2 import service_account
import google.auth.transport.requests

app = Flask(__name__)

def get_access_token():
    credentials = service_account.Credentials.from_service_account_file(
        'serviceAccountKey.json',
        scopes=['https://www.googleapis.com/auth/firebase.messaging']
    )
    request = google.auth.transport.requests.Request()
    credentials.refresh(request)
    return credentials.token

def send_push_notification(token, title, body, image=None):
    access_token = get_access_token()
    url = "https://fcm.googleapis.com/v1/projects/fir-push-notification-85613/messages:send"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    payload = {
        "message": {
            "token": token,
            "notification": {
                "title": title,
                "body": body,
            }
        }
    }

    if image:
        payload["message"]["notification"]["image"] = image

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    return response.json()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_notification', methods=['POST'])
def send_notification():
    fcm_token = request.form.get('fcm_token')
    title = request.form.get('title')
    body = request.form.get('body')
    image = request.form.get('image')
    
    response = send_push_notification(fcm_token, title, body, image)
    return render_template('result.html', registration_id=fcm_token, message_title=title, message_desc=body, image=image, response=response)

if __name__ == '__main__':
    app.run(debug=True)

