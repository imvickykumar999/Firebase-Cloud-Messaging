from django.shortcuts import render, get_object_or_404
from .models import FirebaseConfig
from django.http import HttpResponse
import requests
import json

from google.oauth2 import service_account
import google.auth.transport.requests

def get_access_token():
    credentials = service_account.Credentials.from_service_account_file(
        'serviceAccountKey.json',
        scopes=['https://www.googleapis.com/auth/firebase.messaging']
    )
    request = google.auth.transport.requests.Request()
    credentials.refresh(request)
    return credentials.token

def send_notification(registration_ids, message_title, message_desc):
    fcm_api = get_access_token()  # Get the OAuth 2.0 access token
    url = "https://fcm.googleapis.com/v1/projects/fir-push-notification-85613/messages:send"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": 'Bearer ' + fcm_api
    }

    payload = {
        "message": {
            "token": registration_ids,
            "notification": {
                "body": message_desc,
                "title": message_title,
            }
        }
    }

    result = requests.post(url, data=json.dumps(payload), headers=headers)
    data = result.json()

    print(data)
    return data

def index(request):
    firebase_config = get_object_or_404(FirebaseConfig, id=1)
    return render(request, 'index.html', {'firebase_config': firebase_config})

def send(request):
    if request.method == 'POST':
        registration_id = request.POST.get('registration_id')
        message_title = request.POST.get('title')
        message_desc = request.POST.get('body')
        
        result = send_notification(registration_id, message_title, message_desc)
        response_string = json.dumps(result)
        return render(request, 'result.html', {
            'registration_id': registration_id,
            'message_title': message_title,
            'message_desc': message_desc,
            'response': response_string
        })
    else:
        return HttpResponse("Invalid request method", status=405)

def showFirebaseJS(request):
    data = ('importScripts("https://www.gstatic.com/firebasejs/8.2.0/firebase-app.js");'
            'importScripts("https://www.gstatic.com/firebasejs/8.2.0/firebase-messaging.js"); '
            'var firebaseConfig = {'
            '        apiKey: "AIzaSyDEffV60DqptX5isXVzlhYp1JMKf7t2wlA",'
            '        authDomain: "fir-push-notification-85613.firebaseapp.com",'
            '        projectId: "fir-push-notification-85613",'
            '        storageBucket: "fir-push-notification-85613.appspot.com",'
            '        messagingSenderId: "279392742552",'
            '        appId: "1:279392742552:web:df183eb0e8c256fb7174ed",'
            '        measurementId: "G-TZVKHMQSRE"'
            '};'
            'firebase.initializeApp(firebaseConfig);'
            'const messaging=firebase.messaging();'
            'messaging.setBackgroundMessageHandler(function (payload) {'
            '    console.log(payload);'
            '    const notification=JSON.parse(payload);'
            '    const notificationOption={'
            '        body:notification.body,'
            '        icon:notification.icon'
            '    };'
            '    return self.registration.showNotification(payload.notification.title,notificationOption);'
            '});')

    return HttpResponse(data, content_type="text/javascript")
