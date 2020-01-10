from cloudant.client import Cloudant
from cloudant.result import Result
from cloudant.query import Query
import atexit

client = Cloudant.iam('6171eb89-b0f0-4fa4-8472-8428c5814c05-bluemix', '9YfzrXtfRSI9wlJUnKLcSx1c2VpcgvUkUbKQxUHzH8UA',
    url='https://6171eb89-b0f0-4fa4-8472-8428c5814c05-bluemix.cloudantnosqldb.appdomain.cloud',
    connect=True)

traces_db = client.create_database('traces')
patients_db = client.create_database('patients')
anomalies_db = client.create_database('anomalies')

@atexit.register
def shutdown():
   client.disconnect()