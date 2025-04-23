import requests
import os
import random
from dotenv import load_dotenv


load_dotenv()



def send_photo_telegram(doc_path, caption, chat_id=""):
    token = os.getenv("TELE_TOKEN")
    url = f"https://api.telegram.org/bot{token}/sendDocument"
    print(url)
    document = open(doc_path, "rb")

    files = {
        "document": document,
    }

    if chat_id is None:
        if "_" in os.getenv("TELEGRAM_CHAT_ID"):
            ids = os.getenv("TELEGRAM_CHAT_ID").split("_")

            body = {
                "chat_id": ids[0],
                "message_thread_id": ids[1],
                "caption": caption,
            }
        else:
            body = {
                "chat_id": os.getenv("TELEGRAM_CHAT_ID"),
                "caption": caption,
            }
    else:
        if "_" in chat_id:
            ids = chat_id.split("_")

            body = {
                "chat_id": ids[0],
                "message_thread_id": ids[1],
                "caption": caption,
            }
        else:
            body = {
                "chat_id": chat_id,
                "caption": caption,
            }

    print(body)

    response = requests.post(url, data=body, files=files)

    print(response.text)