# coding: utf-8

__doc__ = ""
__author__ = "Jonathon Wong"
__date__ = "2016-09-07"

import db
import json
import redis


def ops_record(subsys_name='ops_app'):
    """closure return a deco"""
    r = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT,
                          db=REDIS_DB, socket_timeout=3000)

    def deco(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            response_data = func(*args, **kwargs)
            if request.environ['REQUEST_METHOD'] == 'GET':
                return response_data
            resp_status = True if json.loads(response_data)['code'] == 1000 else False
            token = request.values.get('token')
            fk_user_id = r.hgetall(token)['id']
            action = request.values.get('comt_type', '')
            operator_ip = request.environ['REMOTE_ADDR']
            url = request.url
            # request_data = request.values
            
            return response_data
        return wrapper
    return deco




id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
fk_user_id = db.Column('fk_user_id', db.Integer, db.ForeignKey("User.id"))
subsys_name = db.Column('business', db.String(
    32), nullable=False)  # web_operation
action = db.Column('action', db.String(32))  # update, create, delete
# module = db.Column('modlule',db.String(32)    #eg,transport_protocol
#operate_time = db.Column('operate_time',db.TIMESTAMP,default=datetime.datetime.now())
request_data = db.Column('resquest', db.TEXT)
response_data = db.Column('response', db.TEXT)
operator_ip = db.Column('operator_ip', db.STRING(20))
resp_status = db.Column('status_check', db.STRING(20))
url = db.Column('url', db.TEXT)


from models import OpsStat
from local_settings import db_config
import datetime
report = OpsStat(db_config)
start_date = "2016-09-01"
end_date = "2016-09-04"
resp = report.get_fixed_reports(start_date, end_date)
