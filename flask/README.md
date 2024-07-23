    Here is a basic structure for your Flask application:

### Directory Structure
```
flask_app/
│
├── app.py
├── templates/
│   └── index.html
└── static/
    └── firebase-messaging-sw.js
```

### Step-by-Step Guide

1. **Create the Flask App (`app.py`)**

```python
from flask import Flask, render_template, jsonify
import requests
import json
from google.oauth2 import service_account
import google.auth.transport.requests

app = Flask(__name__)

def get_access_token():
    credentials = service_account.Credentials.from_service_account_file(
        'path/to/your/serviceAccountKey.json',
        scopes=['https://www.googleapis.com/auth/firebase.messaging']
    )
    request = google.auth.transport.requests.Request()
    credentials.refresh(request)
    return credentials.token

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_notification', methods=['POST'])
def send_notification():
    registration_id = request.json.get('token')
    message_title = 'Hello'
    message_desc = 'World'
    
    fcm_api = get_access_token()  # Get the OAuth 2.0 access token
    url = "https://fcm.googleapis.com/v1/projects/fir-push-notification-85613/messages:send"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": 'Bearer ' + fcm_api
    }

    payload = {
        "message": {
            "token": registration_id,
            "notification": {
                "title": message_title,
                "body": message_desc,
            }
        }
    }

    result = requests.post(url, data=json.dumps(payload), headers=headers)
    data = result.json()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
```

2. **Create the HTML Template (`templates/index.html`)**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FCM Notification</title>
    <script src="https://www.gstatic.com/firebasejs/8.6.3/firebase-app.js"></script>
    <script src="https://www.gstatic.com/firebasejs/8.6.3/firebase-analytics.js"></script>
    <script src="https://www.gstatic.com/firebasejs/8.6.3/firebase-messaging.js"></script>

    <script>
        // Your web app's Firebase configuration
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

        // Request permission and get the token
        function getFCMToken() {
            messaging.requestPermission()
            .then(() => {
                console.log("Notification permission granted.");
                return messaging.getToken({ vapidKey: 'BI_V_6JdbJ6jpCBSLqZHyhA6r96BG5qa3RbvNz5mq20MYSkFmzt5rDTtrZ6Z6PoaOrYp3REDVpIlu5uzNIxCqEk' });
            })
            .then((currentToken) => {
                if (currentToken) {
                    console.log("FCM Token:", currentToken);
                    // Send the token to your server to store and use for sending push notifications
                    fetch('/send_notification', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ token: currentToken })
                    })
                    .then(response => response.json())
                    .then(data => console.log(data))
                    .catch(error => console.error('Error:', error));
                } else {
                    console.log('No registration token available. Request permission to generate one.');
                }
            })
            .catch((err) => {
                console.log('An error occurred while retrieving token. ', err);
            });
        }

        // Call the function to get the token on page load
        window.onload = getFCMToken;
    </script>
</head>
<body>
    <h1>FCM Notification Example</h1>
</body>
</html>
```

3. **Create the Service Worker (`static/firebase-messaging-sw.js`)**

```javascript
importScripts('https://www.gstatic.com/firebasejs/8.6.3/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/8.6.3/firebase-messaging.js');

// Initialize Firebase
var firebaseConfig = {
    apiKey: "AIzaSyDEffV60DqptX5isXVzlhYp1JMKf7t2wlA",
    authDomain: "fir-push-notification-85613.firebaseapp.com",
    projectId: "fir-push-notification-85613",
    storageBucket: "fir-push-notification-85613.appspot.com",
    messagingSenderId: "279392742552",
    appId: "1:279392742552:web:df183eb0e8c256fb7174ed",
    measurementId: "G-TZVKHMQSRE"
};
firebase.initializeApp(firebaseConfig);

const messaging = firebase.messaging();

messaging.setBackgroundMessageHandler(function(payload) {
    console.log('[firebase-messaging-sw.js] Received background message ', payload);
    const notificationTitle = 'Background Message Title';
    const notificationOptions = {
        body: 'Background Message body.',
        icon: '/firebase-logo.png'
    };

    return self.registration.showNotification(notificationTitle, notificationOptions);
});
```

### Running the Flask App

1. **Install Flask and required libraries**:
   ```bash
   pip install flask requests google-auth google-auth-oauthlib google-auth-httplib2
   ```

2. **Run the Flask application**:
   ```bash
   python app.py
   ```

### Summary

- **app.py**: The main Flask application that serves the HTML file and handles the notification sending logic.
- **index.html**: The HTML file that includes the Firebase configuration and JavaScript code to request notification permission and obtain the FCM token.
- **firebase-messaging-sw.js**: The service worker for handling background messages.

This setup will generate the FCM token when the user grants notification permissions, send it to your server, and use it to send push notifications.
