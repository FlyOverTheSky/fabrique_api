from backend.celery import app
import logging
from django.utils import timezone
import requests
import os
from dotenv import load_dotenv


load_dotenv()

logger = logging.getLogger('logger')
api_url = os.getenv('API_URL')
token = os.getenv("TOKEN")

api_headers = {
    'accept': 'application/json',
    'Authorization': token,
    'Content-Type': 'application/json',
}


@app.task
def check_mailings():
    # import here to avoid NotLoadedYet error
    now = timezone.now()
    from .models import Mailing
    mailings = Mailing.objects.all()
    logger.info('Start check_mailings task')
    for mailing in mailings:
        if not mailing.start_date_time < now < mailing.end_date_time:
            continue
        logger.info('Find active mailing, call activate_mailing task')
        activate_mailing({
            'id': mailing.id,
        })


@app.task
def activate_mailing(mailing_params):
    from .models import Mailing, Message
    global api_headers
    logger.info('Start activate_mailing task')
    mailing = Mailing.objects.get(id=mailing_params['id'])
    msgs = Message.objects.filter(
        mailing=mailing
    )

    if msgs:
        logger.info('Checking messages')
        for msg in msgs:
            if msg.status == "SUCCESS":
                logger.info('Message already sended')
                continue
            logger.info("Find not sended message | making response")
            json_data = {
                'id': msg.id,
                'phone': msg.client.phone_number,
                'text': mailing.text,
             }
            response = requests.post(
                f'{api_url}/send/{msg.id}',
                headers=api_headers,
                json=json_data
            )
            logger.info(f"Response status: {response.status_code}")
            if response.ok:
                msg.send_date = timezone.now()
                msg.status = "SUCCESS"
            else:
                msg.status = "FAILED"
            msg.save()
            logger.info("Message object update")
    else:
        logger.info("No valid messages")
