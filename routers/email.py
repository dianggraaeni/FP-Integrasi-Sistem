import requests
from fastapi import APIRouter
import models

router = APIRouter(prefix="/email", tags=["Email"])

@router.post("/")
def send_email(user: models.UserCreate):
    url = "https://apiconfig.mailtarget.co/v1/layang/transmissions"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer j6chvSHNh6lLnKu5n7FShAjL"
    }
    data = {
        "bodyText": f"Halo {user.name}, ini email dari API!",
        "bodyHtml": f"<h1>Halo {user.name}, ini email dari API!</h1>",
        "from": {"email": "default@sandbox.mailtarget.co", "name": "MailTarget"},
        "subject": "Test Email API",
        "to": [{"email": user.email, "name": user.name}]
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()
