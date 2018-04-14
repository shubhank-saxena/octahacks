import json
import requests

def get_url(srcpin, dstpin):
    KEY = "AIzaSyD9Aj0faCbo20sIhn1RmSQczoKYOe9JuRs"
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&origins=%s&destinations=%s&key=%s" %(srcpin, dstpin, KEY)
    return url

def parse_url(srcpin, dstpin):
    response=requests.get(get_url(srcpin, dstpin))
    content=json.loads(response.content.decode("utf8"))
    main = content['rows'][0]['elements'][0]
    dist= main['distance']["value"]
    time= main['duration']["value"]
    return (dist, time)