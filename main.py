import json
import requests
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

def send_push_notification(token, title, body):
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

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    return response.json()

if __name__ == "__main__":
    fcm_token = 'dF8A2vqxUKQPjV27rLXtiO:APA91bGla1qCeVjVXTVqqnsHsPLk5N8icT1n9XzDDxlBnOWaYZmRiHtS_yPU8QzsTHVLIWT_Adu3eI3kGR4I6YWNk9DNx8NsLVy_XjhNCVltg9KQWX74Om5nPBX7Km9JSSEDDNX3IC_l'
    title = 'Hello'
    body = 'World'
    response = send_push_notification(fcm_token, title, body)
    print('Response:', response)
