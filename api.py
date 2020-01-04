import requests

def call_api(patient):
    response = requests.get(f'http://tesla.iem.pw.edu.pl:9080/v2/monitor/{patient}') 
    return response.json()