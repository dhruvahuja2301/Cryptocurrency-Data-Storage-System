from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from env import api_key

def getData(curr=None, datatype=None, start=1, limit=5000):
    parameters = {
        'convert': 'INR'
    }

    if datatype is None:
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        parameters['start'] = str(start)
        parameters['limit'] = str(limit)
    elif datatype == "id":
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?id='+curr
    elif datatype == "slug":
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?slug='+curr
    else:
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol='+curr

    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key,
    }
    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        if data['status']['error_code'] != 0:
            raise Exception(data['status']['error_message'])

        return data['data']

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        # print(e)
        return e


def getDict(str1):
    try:
        data = getData()
        dicts = {}

        for curr in data:
            dicts[curr["id"]] = curr[str1]

        return dicts

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
        return e
# print(getData(curr='1',datatype="id"))
