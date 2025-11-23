from datetime import date
import requests
import matplotlib.pyplot as plt
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
    text = response.text
    return json.loads(text)

data = json.load(open("my_data.json"))

def get_year(earthquake):
    """Extract the year in which an earthquake happened."""
    timestamp = earthquake['properties']['time']
    year = date.fromtimestamp(timestamp/1000).year
    return year
print(get_year(data["features"][1]))  

def get_magnitude(earthquake):
    return earthquake["properties"]["mag"]   
print(get_magnitude(data["features"][1]))


years = {get_year(eq) for eq in data["features"]}

print(years)

def get_magnitudes_per_year(earthquakes):
    """Retrieve the magnitudes of all the earthquakes in a given year.
    
    Returns a dictionary with years as keys, and lists of magnitudes as values.
    """
    years = {get_year(x) for x in data["features"]}
    magnitudes_per_year = {year: [] for year in years}
    for y in earthquakes:
        year = get_year(y)
        magnitude = get_magnitude(y)
        magnitudes_per_year[year].append(magnitude) 
    return magnitudes_per_year
print(get_magnitudes_per_year(data["features"]))



def plot_average_magnitude_per_year(earthquakes):
    """Plot the average magnitude of earthquakes per year."""
    magnitudes_per_year = get_magnitudes_per_year(earthquakes)
    years = sorted(magnitudes_per_year.keys())
    average_magnitudes = []
    for year in years:
        magnitudes = magnitudes_per_year[year]
        average_magnitude = sum(magnitudes) / len(magnitudes)
        average_magnitudes.append(average_magnitude)
    plt.plot(years, average_magnitudes)
    plt.xlabel("Year")
    plt.ylabel("Average Magnitude")
    plt.title("Average Earthquake Magnitude per Year")
    plt.show()
    
def plot_number_per_year(earthquakes):
    """Plot the number of earthquakes per year."""
    magnitudes_per_year = get_magnitudes_per_year(earthquakes)
    years = sorted(magnitudes_per_year.keys())
    counts = [len(magnitudes_per_year[year]) for year in years]
    plt.plot(years, counts)
    plt.xlabel("Year")
    plt.ylabel("Number of Earthquakes")
    plt.title("Number of Earthquakes per Year")
    plt.show()
# Get the data we will work with
quakes = get_data()['features']

# Plot the results - this is not perfect since the x axis is shown as real
# numbers rather than integers, which is what we would prefer!
plot_number_per_year(quakes)
plt.clf()  # This clears the figure, so that we don't overlay the two plots
plot_average_magnitude_per_year(quakes)
