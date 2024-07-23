# User Input Message
![image](https://github.com/user-attachments/assets/65a7b307-d9d9-49ae-90bc-4dc7702c2b59)
![image](https://github.com/user-attachments/assets/10a54d8e-7540-473b-b124-0a318e3da9fa)

To obtain the service account JSON file required for `service_account.Credentials.from_service_account_file`, you need to create a service account in your Firebase project and download the key. Here are the steps to do so:

![image](https://github.com/user-attachments/assets/94caac48-3947-42ef-9696-80d5a0974201)

### Steps to Create a Service Account and Download the JSON Key

1. **Go to the Firebase Console**:
   - Open the [Firebase Console](https://console.firebase.google.com/u/0/project/fir-push-notification-85613/settings/serviceaccounts/adminsdk).
   - Select your project (e.g., `fir-push-notification-85613`).

2. **Navigate to Project Settings**:
   - Click on the gear icon next to "Project Overview" and select "Project settings".

3. **Service Accounts**:
   - In the settings page, click on the "Service accounts" tab.
   - Click on the "Generate new private key" button.
   - A JSON file will be automatically downloaded to your computer. This is your service account key.

4. **Store the JSON Key Securely**:
   - Save this JSON file in a secure location on your server or development machine. The file contains sensitive information that should not be exposed publicly.

---

### Step 1: Verify URL Configuration

Make sure that your URL pattern for `send` is correctly defined and includes a name:

```python
from django.contrib import admin
from django.urls import path
from home.views import index, send, showFirebaseJS

urlpatterns = [
    path('', index, name='index'),
    path('send/', send, name='send'),
    path('firebase-messaging-sw.js', showFirebaseJS, name='show_firebase_js'),
    path('admin/', admin.site.urls),
]
```

### Step 2: Verify the Template

Ensure that your template (`index.html`) is using the correct URL name in the form action:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Send Notification</title>
    <script src="https://www.gstatic.com/firebasejs/8.6.3/firebase-app.js"></script>
    <script src="https://www.gstatic.com/firebasejs/8.6.3/firebase-analytics.js"></script>
    <script src="https://www.gstatic.com/firebasejs/8.6.3/firebase-messaging.js"></script>
    <script>
        var firebaseConfig = {
            apiKey: "AIzaSyDEffV60DqptX5isXVzlhYp1JMKf7t2wlA",
            authDomain: "fir-push-notification-85613.firebaseapp.com",
            projectId: "fir-push-notification-85613",
            storageBucket: "fir-push-notification-85613.appspot.com",
            messagingSenderId: "279392742552",
            appId: "1:279392742552:web:df183eb0e8c256fb7174ed",
            measurementId: "G-TZVKHMQSRE"
        };
        // Initialize Firebase
        firebase.initializeApp(firebaseConfig);
        firebase.analytics();
      
        const messaging = firebase.messaging();

        messaging.getToken({ vapidKey: 'BI_V_6JdbJ6jpCBSLqZHyhA6r96BG5qa3RbvNz5mq20MYSkFmzt5rDTtrZ6Z6PoaOrYp3REDVpIlu5uzNIxCqEk' }).then((currentToken) => {
            if (currentToken) {
                console.log(currentToken);
            } else {
                console.log('No registration token available. Request permission to generate one.');
            }
        }).catch((err) => {
            console.log('An error occurred while retrieving token. ', err);
        });

        messaging.requestPermission().then(function () {
            console.log("Notification permission granted.");
            return messaging.getToken();
        }).catch(function (err) {
            console.log("Unable to get permission to notify.", err);
        });

        messaging.onMessage((payload) => {
            console.log('Message received. ', payload);
        });
    </script>
</head>
<body>
    <h1>Send Firebase Push Notification</h1>
    <form method="post" action="{% url 'send' %}">
        {% csrf_token %}
        <label for="title">Title:</label>
        <input type="text" id="title" name="title" required><br><br>
        <label for="body">Body:</label>
        <textarea id="body" name="body" required></textarea><br><br>
        <button type="submit">Send Notification</button>
    </form>
</body>
</html>
```

### Step 3: Verify the View Function

Ensure that the `send` view function is correctly defined in your `home/views.py` file:

```python
from django.http import HttpResponse
from django.shortcuts import render
import requests
import json

from google.oauth2 import service_account
import google.auth.transport.requests

def get_access_token():
    credentials = service_account.Credentials.from_service_account_file(
        'fir-push-notification-85613-6988faf5d271.json',
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
                # "image": "https://i.ytimg.com/vi/m5WUPHRgdOA/hqdefault.jpg?sqp=-oaymwEXCOADEI4CSFryq4qpAwkIARUAAIhCGAE=&rs=AOn4CLDwz-yjKEdwxvKjwMANGk5BedCOXQ",
                # "icon": "https://yt3.ggpht.com/ytc/AKedOLSMvoy4DeAVkMSAuiuaBdIGKC7a5Ib75bKzKO3jHg=s900-c-k-c0x00ffffff-no-rj",
            }
        }
    }

    result = requests.post(url, data=json.dumps(payload), headers=headers)
    data = result.json()

    print(data)
    return data

def index(request):
    return render(request, 'index.html')

def send(request):
    if request.method == 'POST':
        registration_id = "dF8A2vqxUKQPjV27rLXtiO:APA91bGla1qCeVjVXTVqqnsHsPLk5N8icT1n9XzDDxlBnOWaYZmRiHtS_yPU8QzsTHVLIWT_Adu3eI3kGR4I6YWNk9DNx8NsLVy_XjhNCVltg9KQWX74Om5nPBX7Km9JSSEDDNX3IC_l"
        title = request.POST.get('title')
        body = request.POST.get('body')
        result = send_notification(registration_id, title, body)

        data = json.dumps(result)
        return HttpResponse(data)
    else:
        return HttpResponse("Invalid request method", status=405)

def showFirebaseJS(request):
    data = 'importScripts("https://www.gstatic.com/firebasejs/8.2.0/firebase-app.js");' \
           'importScripts("https://www.gstatic.com/firebasejs/8.2.0/firebase-messaging.js"); ' \
           'var firebaseConfig = {' \
           '        apiKey: "AIzaSyDEffV60DqptX5isXVzlhYp1JMKf7t2wlA",' \
           '        authDomain: "fir-push-notification-85613.firebaseapp.com",' \
           '        projectId: "fir-push-notification-85613",' \
           '        storageBucket: "fir-push-notification-85613.appspot.com",' \
           '        messagingSenderId: "279392742552",' \
           '        appId: "1:279392742552:web:df183eb0e8c256fb7174ed",' \
           '        measurementId: "G-TZVKHMQSRE"' \
           ' };' \
           'firebase.initializeApp(firebaseConfig);' \
           'const messaging=firebase.messaging();' \
           'messaging.setBackgroundMessageHandler(function (payload) {' \
           '    console.log(payload);' \
           '    const notification=JSON.parse(payload);' \
           '    const notificationOption={' \
           '        body:notification.body,' \
           '        icon:notification.icon' \
           '    };' \
           '    return self.registration.showNotification(payload.notification.title,notificationOption);' \
           '});'

    return HttpResponse(data, content_type="text/javascript")
```

After ensuring all the above steps are correct, restart your Django server and try accessing the form again. This should resolve the `NoReverseMatch` error. If you still face issues, please let me know!
