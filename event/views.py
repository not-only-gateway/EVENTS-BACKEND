from flask import request
from api.api import ApiView
from app import app, db, authorize
from event.models import Event

api = ApiView(
    class_instance=Event,
    identifier_attr='id',
    relationships=[],
    db=db,
    on_before_call=authorize
)

@app.route('/api/list/effective', methods=['GET'])
def list_event():
    return api.list(request.args)