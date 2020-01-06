from threading import Thread
import time
import schedule
from datetime import datetime
from datetime import timedelta

from .database import traces_db, patients_db
from .settings import REMOVING_TRACES_FREQUENCY, REQUESTS_PATHNAME_PREFIX, PATIENTS, PROBING_FREQUENCY

import requests

def call_api(patient):
    response = requests.get(f'http://tesla.iem.pw.edu.pl:9080/v2/monitor/{patient}') 
    return response.json()

def run_schedule():
    while 1:
        schedule.run_pending()
        time.sleep(1)

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


t = Thread(target=run_schedule)
t.start()

#schedule.every(PROBING_FREQUENCY).seconds.do(get_probes)
#schedule.every(REMOVING_TRACES_FREQUENCY).seconds.do(remove_old_traces)

t = Thread(target=run_schedule)
t.start()

print(f'[{datetime.now()}] Fetching patients data...')
get_patients_data()