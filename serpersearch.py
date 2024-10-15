import http.client
import json

SearchTypes = [
    'search',
    'places',
    'maps',
    'news',
    'shopping',
    'scholar',
    'patents'
]

headers = {
  'X-API-KEY': '99615f7dddbee6b6a6173f6818a04a67c12f43f7',
  'Content-Type': 'application/json'
}

def SearchWeb(Query : str, TypeOfSearch : str) -> object :
    print(f'Searching web for "{Query}" using "{TypeOfSearch}".\n')
    conn = http.client.HTTPSConnection("google.serper.dev")
    payload = json.dumps({
    'q' : Query
    })

    conn.request("POST", f"/{TypeOfSearch}", payload, headers)
    res = conn.getresponse()
    data = res.read()

    match TypeOfSearch :
        case 'search' :
            return eval(data.decode("utf-8"))['organic']
        case 'places' :
            return eval(data.decode("utf-8"))['places']
        case 'maps' :
            return eval(data.decode("utf-8"))['places']
        case 'news' :
            return eval(data.decode("utf-8"))['news']
        case 'shopping' :
            return eval(data.decode("utf-8"))['shopping']
        case 'scholar' :
            return eval(data.decode("utf-8"))['organic']
        case 'patent' :
            return eval(data.decode("utf-8"))['organic']
    
    raise NotImplementedError(TypeOfSearch)