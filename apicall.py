from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import numpy

def getData(curr=None,datatype=None,start=1,limit=5000):  
  url=''
  parameters = {
    'convert':'INR'
  }

  if(datatype==None):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters['start']=str(start)
    parameters['limit']=str(limit)
  elif(datatype=="id"):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?id='+curr
  elif(datatype=="slug"):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?slug='+curr
  else:
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol='+curr

  headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': '0a8b0953-ff76-4d78-a5da-09f26feaec17',
  }
  session = Session()
  session.headers.update(headers)
  
  try:
    response = session.get(url, params=parameters)
    data = json.loads(response.text)
    if(data['status']['error_code']!=0):
      raise Exception(data['status']['error_message'])

    return data['data']

  except (ConnectionError, Timeout, TooManyRedirects) as e:
    # print(e)
    return e

def getDict(str):
  try:
    data = getData()
    dicts = {}

    for curr in data:
      dicts[curr["id"]]=curr[str]

    return dicts    

  except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)
    return e
