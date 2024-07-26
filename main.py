import json
import requests
from google.oauth2 import service_account
import google.auth.transport.requests

def get_access_token(secret):
    credentials = service_account.Credentials.from_service_account_file(
    	secret, scopes=['https://www.googleapis.com/auth/firebase.messaging']
    )
    request = google.auth.transport.requests.Request()
    credentials.refresh(request)
    return credentials.token


def send_push_notification(token, title, body, image_url, ProjectID, secret):
    access_token = get_access_token(secret)
    url = f"https://fcm.googleapis.com/v1/projects/{ProjectID}/messages:send"
    
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
                "image": image_url
            },
            "android": {
                "notification": {
                    "sound": "default"
                }
            },
            "apns": {
                "payload": {
                    "aps": {
                        "sound": "default"
                    }
                }
            }
        }
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    return response.json()

if __name__ == "__main__":
    fcm_token = 'cbpdTSSdQEeDkx9_RdYBoC:APA91bHo5uFHWVSwMUpLjRiy6-NN4yu1L0vj5xwHxHvBWzIL66f-tcCHZ5ckomaiyI9fR66ewoqfEjnFktkclpetIlmBRiJ6OAGnhOL3Ng6yOWiq8SgPmS9qEv0ibSOl-GhqY5mbiemW'
    ProjectID = 'influencerhiringmobilevarify'

    # https://github.com/imvickykumar999/Django-InHouse/blob/main/influencerhiringmobilevarify-firebase-adminsdk-6u3jg-71f1372357.json
    secret = 'influencerhiringmobilevarify-firebase-adminsdk-6u3jg-71f1372357.json'
    
    title = 'Hello'
    body = 'World'
    image_url = 'https://media.idownloadblog.com/wp-content/uploads/2018/07/Apple-logo-black-and-white.png'
    
    response = send_push_notification(fcm_token, title, body, image_url, ProjectID, secret)
    print('Response:', response)
