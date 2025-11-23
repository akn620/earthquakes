# The Python standard library includes some functionality for communicating
# over the Internet.
# However, we will use a more powerful and simpler library called requests.
# This is external library that you may need to install first.
import requests
import json

def get_data():
    # With requests, we can ask the web service for the data.
    # Can you understand the parameters we are passing here?
    response = requests.get(
        "http://earthquake.usgs.gov/fdsnws/event/1/query.geojson",
        params={
            'starttime': "2000-01-01",
            "maxlatitude": "58.723",
            "minlatitude": "50.008",
            "maxlongitude": "1.67",
            "minlongitude": "-9.756",
            "minmagnitude": "1",
            "endtime": "2018-10-11",
            "orderby": "time-asc"}
    )

    # The response we get back is an object with several fields.
    # The actual contents we care about are in its text field:
    text = response.json()
    # To understand the structure of this text, you may want to save it
    # to a file and open it in VS Code or a browser.
    # See the README file for more information.
    
    with open("my_data.json", 'w') as f:
        json.dump(text, f, indent=4)

    # We need to interpret the text to get values that we can work with.
    # What format is the text in? How can we load the values?
    return text

data = json.load(open("my_data.json"))

#print(data["features"][])



def count_earthquakes(x):
    return sum(1 for item in x["features"] if item["properties"]["type"] == "earthquake")

print(count_earthquakes(data))

def get_magnitude(z,y):
    return [item["properties"]["mag"] for item in z["features"] if item["properties"]["title"] == y]
print(get_magnitude(data, "M 4.0 - 38 km NNE of Cromer, United Kingdom"))

def get_location(a,b):
    """Retrieve the latitude and longitude of an earthquake item."""
    return [(item["geometry"]["coordinates"][0], item["geometry"]["coordinates"][1]) for item in a["features"] if item["properties"]["title"] == b]
    
print(get_location(data,"M 4.0 - 38 km NNE of Cromer, United Kingdom"))

def get_maximum(q):
    """Get the magnitude and location of the strongest earthquake in the data."""
    return [(item["properties"]["mag"], item["properties"]["place"]) for item in q["features"] if item["properties"]["mag"] == max([i["properties"]["mag"] for i in q["features"]])][0]
print(get_maximum(data))

# With all the above functions defined, we can now call them and get the result
#data = get_data()
#print(data)
#print(f"Loaded {count_earthquakes(data)}")
##max_magnitude, max_location = get_maximum(data)
#print(f"The strongest earthquake was at {max_location} with magnitude {max_magnitude}")