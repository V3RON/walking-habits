import time
import schedule
from datetime import datetime
from datetime import timedelta

from cloudant.client import Cloudant
from cloudant.result import Result
from cloudant.query import Query
from flask import Flask, request
from threading import Thread
from api import call_api
import atexit

# CONSTANTS
PROBING_FREQUENCY = 2
REMOVING_TRACES_FREQUENCY = 10
PATIENTS = 6

client = Cloudant.iam('X', 'Y', url='Z', connect=True)
app = Flask(__name__)

traces_db = client.create_database('traces')
patients_db = client.create_database('patients')

def get_patients_data():
    for idx in range(1, PATIENTS + 1):
        if str(idx) not in patients_db:
            data = call_api(idx)
            data['_id'] = str(idx)
            del data['id']
            del data['trace']
            patients_db.create_document(data)

def remove_old_traces():
    print(f'[{datetime.now()}] Removing old traces...')
    current_timestamp = datetime.timestamp(datetime.now() - timedelta(seconds=REMOVING_TRACES_FREQUENCY))
    query = Query(traces_db, selector = { 'timestamp': { '$lt': current_timestamp }})()
    doc_count = len(query['docs'])

    deleted_docs = list(map(lambda doc: { '_id': doc['_id'], '_rev': doc['_rev'], '_deleted': True }, query['docs']))
    traces_db.bulk_docs(deleted_docs)
    print(f'[{datetime.now()}] Removed {doc_count} traces')

def get_probes():
    print(f'[{datetime.now()}] Fetching current probes...')
    for idx in range(1, PATIENTS + 1):
        data = call_api(idx)['trace']
        data['_id'] = str(data['id'])
        data['patient'] = str(idx)
        data['timestamp'] = datetime.timestamp(datetime.now())
        del data['id']
        traces_db.create_document(data)

def run_schedule():
    while 1:
        schedule.run_pending()
        time.sleep(1)

@atexit.register
def shutdown():
   client.disconnect()

if __name__ == '__main__':
    schedule.every(PROBING_FREQUENCY).seconds.do(get_probes)
    schedule.every(REMOVING_TRACES_FREQUENCY).seconds.do(remove_old_traces)

    t = Thread(target=run_schedule)
    t.start()

    print(f'[{datetime.now()}] Fetching patients data...')
    get_patients_data()

    print(f'[{datetime.now()}] Running...')
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)