from datetime import datetime
from app import db
from sqlalchemy.dialects.postgresql import UUID, JSONB


class Event(db.Model):
    __tablename__ = 'evento'
    id = db.Column('codigo_id', db.BigInteger, primary_key=True)
    method = db.Column('metodo_http', db.String(), nullable=False)
    request_time = db.Column('horario', db.DateTime(), nullable=False)
    full_url = db.Column('url_completo', db.String(), nullable=False)
    url = db.Column('url_base', db.String(), nullable=False)

    headers = db.Column('headers', db.String(), nullable=False)

    status_code = db.Column('status_http', db.Integer(), nullable=False)
    response_time = db.Column('tempo_resposta', db.BigInteger(), nullable=False)

    def __init__(self, data):
        for key in data.keys():
            if hasattr(self, key):
                setattr(self, key, data.get(key, None))
        db.session.add(self)
        db.session.commit()
