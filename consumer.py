import sys
import pika, json
from pika import exceptions
from sqlalchemy.exc import SQLAlchemyError, PendingRollbackError
from datetime import datetime
from app import db
from event.models import Event
from service.models import Service
from backend_utils.utils.consumer import consumer
from user.models import User

def callback(ch, method, properties, body):
    try:
        data = json.loads(body)
        if properties.content_type == 'request':
            try:
                dumped = sys.getsizeof(json.dumps(data.get('params', None)))
            except json.JSONDecodeError:
                dumped = sys.getsizeof(str(data.get('params', None)))
            try:
                dumped_response = sys.getsizeof(json.dumps(data.get('response', None)))

            except json.JSONDecodeError:
                dumped_response = sys.getsizeof(str(data.get('response', None)))

            service = Service.query.get(data.get('service_id', None))
            if service is None:
                Service(data.get('service_id', None))

            try:
                serializer = Event({
                    'method': data.get('method', None),
                    'request_time': data.get('request_time', None),
                    'full_url': data.get('full_url', None),
                    'url': data.get('url', None),
                    'service': data.get('service_id', None),
                    'headers': data.get('headers', None),
                    'status_code': data.get('status_code', None),
                    'response_time': data.get('response_time', None),
                    'request_package': data.get('params', None),
                    'response_package': data.get('response', None),
                    'request_package_size': dumped,
                    'response_package_size': dumped_response
                })
                db.session.add(serializer)
                db.session.commit()
            except SQLAlchemyError:
                pass
        elif properties.content_type == 'user':
            try:
                user = User.query.get(data.get("user_email"))
                if user is None:
                    User(data)
            except (SQLAlchemyError, PendingRollbackError):
                pass
    except json.JSONDecodeError:
        pass


consumer(callback=callback, queue='request')
