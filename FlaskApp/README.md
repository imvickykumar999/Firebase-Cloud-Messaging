# Summary of Flask Application

![image](https://github.com/user-attachments/assets/f5280059-9c92-4d77-bb35-a104a89d1304)
![image](https://github.com/user-attachments/assets/c8b4a711-1a34-4bee-8a10-85ed770ca3ea)

Here's a summary of the Flask application setup:

1. **Setup Flask Application**:
    - Created a Flask application to manage Firebase configuration and notifications.
    - Installed necessary dependencies (`flask` and `firebase-admin`).

2. **Firebase Admin SDK Initialization**:
    - Initialized Firebase Admin SDK using a service account key (`serviceAccountKey.json`) for interacting with Firebase services.

3. **Created Flask Routes**:
    - **Home Route (`/`)**:
        - Serves the main HTML template (`index.html`) to render the form for sending notifications.
    - **Firebase Config Route (`/firebase-config`)**:
        - Returns Firebase configuration details as JSON. This configuration is fetched using an AJAX request on the client side.
    - **Send Route (`/send`)**:
        - Handles form submission to send notifications.
        - Extracts `registration_id`, `title`, and `body` from the POST request.
        - Renders the `result.html` template with the notification details and a simulated response.
    - **Service Worker Route (`/firebase-messaging-sw.js`)**:
        - Serves the service worker script required for Firebase Cloud Messaging.

4. **HTML Templates**:
    - **index.html**:
        - Contains the form to input notification details (title and body).
        - Uses AJAX to fetch Firebase configuration and initialize Firebase.
        - Manages Firebase Cloud Messaging tokens and permissions.
    - **result.html**:
        - Displays the results after sending the notification, including the registration token, title, body, and response.

5. **Service Worker Script**:
    - **firebase-messaging-sw.js**:
        - Handles background notifications for Firebase Cloud Messaging.
        - Placed in the `static` directory and served via the Flask application.

### Directory Structure

```
my_flask_app/
├── static/
│   ├── firebase-messaging-sw.js
├── templates/
│   ├── index.html
│   ├── result.html
├── app.py
├── requirements.txt
├── serviceAccountKey.json
```

### Code Highlights

**app.py**:
```python
from flask import Flask, jsonify, render_template, request, send_from_directory
import firebase_admin
from firebase_admin import credentials

app = Flask(__name__)

# Initialize Firebase Admin SDK
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://fir-push-notification-85613-default-rtdb.firebaseio.com'
})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/firebase-config')
def get_firebase_config():
    config = {
        'apiKey': "AIzaSyDEffV60DqptX5isXVzlhYp1JMKf7t2wlA",
        'authDomain': "fir-push-notification-85613.firebaseapp.com",
        'projectId': "fir-push-notification-85613",
        'storageBucket': "fir-push-notification-85613.appspot.com",
        'messagingSenderId': "279392742552",
        'appId': "1:279392742552:web:df183eb0e8c256fb7174ed",
        'measurementId': "G-TZVKHMQSRE",
        'vapidKey': "BI_V_6JdbJ6jpCBSLqZHyhA6r96BG5qa3RbvNz5mq20MYSkFmzt5rDTtrZ6Z6PoaOrYp3REDVpIlu5uzNIxCqEk"
    }
    return jsonify(config)

@app.route('/send', methods=['POST'])
def send():
    registration_id = request.form.get('registration_id')
    title = request.form.get('title')
    body = request.form.get('body')
    
    print(f"Registration ID: {registration_id}")
    print(f"Title: {title}")
    print(f"Body: {body}")
    
    response = {
        "message_id": "example_message_id",
        "status": "Success",
        "info": "Notification has been sent"
    }
    
    return render_template('result.html', 
                           registration_id=registration_id, 
                           message_title=title, 
                           message_desc=body, 
                           response=response)

@app.route('/firebase-messaging-sw.js')
def service_worker():
    return send_from_directory('static', 'firebase-messaging-sw.js')

if __name__ == '__main__':
    app.run(debug=True)
```

**templates/index.html**:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Send Notification</title>
    <style>
        /* Styles omitted for brevity */
    </style>
    <script src="https://www.gstatic.com/firebasejs/8.6.3/firebase-app.js"></script>
    <script src="https://www.gstatic.com/firebasejs/8.6.3/firebase-analytics.js"></script>
    <script src="https://www.gstatic.com/firebasejs/8.6.3/firebase-messaging.js"></script>
    <script>
        document.addEventListener("DOMContentLoaded", function() {
            fetch('/firebase-config')
                .then(response => response.json())
                .then(config => {
                    if (config.error) {
                        console.error('Error fetching Firebase config:', config.error);
                        return;
                    }

                    var firebaseConfig = {
                        apiKey: config.apiKey,
                        authDomain: config.authDomain,
                        projectId: config.projectId,
                        storageBucket: config.storageBucket,
                        messagingSenderId: config.messagingSenderId,
                        appId: config.appId,
                        measurementId: config.measurementId
                    };
                    // Initialize Firebase
                    firebase.initializeApp(firebaseConfig);
                    firebase.analytics();
                  
                    const messaging = firebase.messaging();

                    function getRegistrationToken() {
                        return messaging.getToken({ vapidKey: config.vapidKey })
                            .then((currentToken) => {
                                if (currentToken) {
                                    return currentToken;
                                } else {
                                    console.log('No registration token available. Request permission to generate one.');
                                    return null;
                                }
                            })
                            .catch((err) => {
                                console.log('An error occurred while retrieving token. ', err);
                                return null;
                            });
                    }

                    document.getElementById("notificationForm").addEventListener("submit", function(event) {
                        event.preventDefault();
                        getRegistrationToken().then((token) => {
                            if (token) {
                                document.getElementById('registration_id').value = token;
                                this.submit();
                            } else {
                                alert('Unable to retrieve registration token.');
                            }
                        });
                    });

                    messaging.requestPermission().then(function () {
                        console.log("Notification permission granted.");
                    }).catch(function (err) {
                        console.log("Unable to get permission to notify.", err);
                    });

                    messaging.onMessage((payload) => {
                        console.log('Message received. ', payload);
                    });

                    navigator.serviceWorker.register('/firebase-messaging-sw.js')
                    .then((registration) => {
                        messaging.useServiceWorker(registration);
                    }).catch((err) => {
                        console.log('Service Worker registration failed: ', err);
                    });
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        });
    </script>
</head>
<body>
    <div class="container">
        <h1>Send Firebase Push Notification</h1>
        <form id="notificationForm" method="post" action="/send">
            <input type="hidden" id="registration_id" name="registration_id">
            <label for="title">Title:</label>
            <input type="text" id="title" name="title" required>
            <label for="body">Body:</label>
            <textarea id="body" name="body" required></textarea>
            <button type="submit">Send Notification</button>
        </form>
    </div>
</body>
</html>
```

**templates/result.html**:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Notification Sent</title>
    <style>
        /* Styles omitted for brevity */
    </style>
    <script>
        function copyToClipboard() {
            var token = document.getElementById("registrationToken").innerText;
            navigator.clipboard.writeText(token).then(function() {
                alert("Registration Token copied to clipboard!");
            }, function(err) {
                alert("Failed to copy Registration Token: " + err);
            });
        }
    </script>
</head>
<body>
    <div class="container">
        <h1>Notification Sent</h1>
        <hr><br>
        <p>
            <strong>Registration Token:</strong>
            <button class="copy-button" onclick="copyToClipboard()">Copy</button>  <br><br>
            <span class="highlight" id="registrationToken">{{ registration_id }}</span>
        </p> <br><br>
        <p><strong>Title:</strong> <span class="highlight">{{ message_title }}</span></p>
        <p><strong>Body:</strong> <span class="highlight">{{ message_desc }}</span></p>
        <h3 align="right">Response from FCM:</h3>
        <pre>{{ response }}</pre>


    </div>
</body>
</html>
```

**static/firebase-messaging-sw.js**:
```javascript
importScripts('https://www.gstatic.com/firebasejs/8.6.3/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/8.6.3/firebase-messaging.js');

firebase.initializeApp({
    apiKey: "AIzaSyDEffV60DqptX5isXVzlhYp1JMKf7t2wlA",
    authDomain: "fir-push-notification-85613.firebaseapp.com",
    projectId: "fir-push-notification-85613",
    storageBucket: "fir-push-notification-85613.appspot.com",
    messagingSenderId: "279392742552",
    appId: "1:279392742552:web:df183eb0e8c256fb7174ed",
    measurementId: "G-TZVKHMQSRE"
});

const messaging = firebase.messaging();

messaging.onBackgroundMessage(function(payload) {
  console.log('[firebase-messaging-sw.js] Received background message ', payload);
  const notificationTitle = 'Background Message Title';
  const notificationOptions = {
    body: 'Background Message body.',
    icon: '/firebase-logo.png'
  };

  self.registration.showNotification(notificationTitle, notificationOptions);
});
```

### Summary

This setup creates a Flask application that:
- Provides a form for sending notifications.
- Fetches Firebase configuration securely using an AJAX call.
- Registers a service worker to handle background notifications.
- Displays the notification details and response on a result page after the form submission.
