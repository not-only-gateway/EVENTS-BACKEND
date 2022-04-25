import sys
import pika, json

from sqlalchemy.exc import SQLAlchemyError, PendingRollbackError

from app import db
from event.models import Event
from api.consumer import consumer

def callback(ch, method, properties, body):
    try:
        data = json.loads(body)
        if properties.content_type == 'request':
            try:
                serializer = Event({
                    'method': data.get('method', None),
                    'request_time': data.get('request_time', None),
                    'full_url': data.get('full_url', None),
                    'url': data.get('url', None),

                    'headers': json.dumps(data.get('headers', None)),
                    'status_code': data.get('status_code', None),
                    'response_time': data.get('response_time', None)
                })
                db.session.add(serializer)
                db.session.commit()
            except SQLAlchemyError:
                pass
    except json.JSONDecodeError:
        pass


consumer(callback=callback, queue='request')
