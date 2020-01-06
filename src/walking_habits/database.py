from cloudant.client import Cloudant
from cloudant.result import Result
from cloudant.query import Query
import atexit

client = Cloudant.iam('x', 'y',
    url='z',
    connect=True)

traces_db = client.create_database('traces')
patients_db = client.create_database('patients')

@atexit.register
def shutdown():
   client.disconnect()