from typing import TypedDict
import jageocoder

jageocoder.init(url='https://jageocoder.info-proto.com/jsonrpc')

class Location(TypedDict):
    lat: float
    lon: float

def getLocation(add) -> Location:
    try:
        loc = jageocoder.search(add)
        if not loc['matched']:
            raise Exception("Address not found")
        latlon : Location = {
            "lat": loc['candidates'][0]['y'],
            "lon": loc['candidates'][0]['x']
        }
        return latlon
    except Exception as e:
        print(f"geocoding error: {e}")
        return None