## Appendix B: Output Automater Examples

**Create a script that automatically compiles and summarizes weekly seismic activity reports from the USGS database, focusing on earthquakes above magnitude 4.0. Include data on location, magnitude, depth, and potential affected areas. Output the summary in a CSV format. \[March 15, 2024\]**

ChatGPT

Below is a Python script that automates the process of fetching weekly seismic activity reports from the USGS database, focusing on earthquakes above magnitude 4.0, and then summarizes the data into a CSV format:

python

Copy code

import requests

import csv

from datetime import datetime, timedelta

def fetch_weekly_seismic_activity(start_date):

\# Calculate the end date (7 days after the start date)

end_date = start_date + timedelta(days=7)

\# Format dates for the USGS API

start_date_str = start_date.strftime('%Y-%m-%d')

end_date_str = end_date.strftime('%Y-%m-%d')

\# Define the USGS API URL for earthquake data

usgs_url = f"<https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={start_date_str}&endtime={end_date_str}&minmagnitude=4.0>"

\# Fetch earthquake data from USGS

response = requests.get(usgs_url)

if response.status_code == 200:

data = response.json()

return data\['features'\]

else:

print("Failed to fetch earthquake data")

return None

def summarize_earthquake_data(earthquake_data):

summary = \[\]

for event in earthquake_data:

location = event\['properties'\]\['place'\]

magnitude = event\['properties'\]\['mag'\]

depth = event\['geometry'\]\['coordinates'\]\[2\]

affected_areas = event\['properties'\]\['place'\]

summary.append({

'Location': location,

'Magnitude': magnitude,

'Depth': depth,

'Affected Areas': affected_areas

})

return summary

def save_summary_to_csv(summary, filename):

with open(filename, 'w', newline='') as csvfile:

fieldnames = \['Location', 'Magnitude', 'Depth', 'Affected Areas'\]

writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

writer.writeheader()

for row in summary:

writer.writerow(row)

def main():

\# Define the start date for the weekly report (assuming the current date)

start_date = datetime.now().date() - timedelta(days=datetime.now().weekday())

\# Fetch seismic activity data

earthquake_data = fetch_weekly_seismic_activity(start_date)

if earthquake_data:

\# Summarize the data

summary = summarize_earthquake_data(earthquake_data)

\# Save the summary to a CSV file

save_summary_to_csv(summary, 'weekly_seismic_activity_summary.csv')

print("Weekly seismic activity summary saved to 'weekly_seismic_activity_summary.csv'")

else:

print("No seismic activity data found for the week")

if \__name__ == "\__main_\_":

main()

This script fetches seismic activity data from the USGS database for the current week (assuming the current date) and summarizes earthquakes with a magnitude above 4.0. It then saves the summary into a CSV file named weekly_seismic_activity_summary.csv. You can adjust the filename and path as needed.

**Create a script that automatically compiles and summarizes the number of new planets confirmed in the previous week using the NASA exoplanet archive data. Include data on planet name, host name and discovery method. Output the summary in a CSV format. \[March 15, 2024\]**

ChatGPT

To automate the task of compiling and summarizing the number of new planets confirmed in the previous week using the NASA exoplanet archive data, you can use Python along with libraries like requests for fetching data and csv for handling CSV output. Here's a script that does exactly that:

python

Copy code

import requests

import csv

from datetime import datetime, timedelta

\# Function to fetch data from NASA Exoplanet Archive

def fetch_exoplanet_data():

\# Define URL for the API

url = '<https://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?table=exoplanets>'

\# Make a request to the API

response = requests.get(url)

\# Check if the request was successful

if response.status_code == 200:

\# Return the JSON data

return response.json()

else:

\# If request failed, print an error message

print("Failed to fetch data from NASA Exoplanet Archive.")

return None

\# Function to filter planets discovered in the previous week

def filter_new_planets(data, days=7):

\# Calculate date of a week ago

end_date = datetime.now()

start_date = end_date - timedelta(days=days)

\# Filter planets discovered in the previous week

new_planets = \[\]

for planet in data:

discovery_date = datetime.strptime(planet\['pl_disc'\], '%Y-%m-%d')

if start_date <= discovery_date <= end_date:

new_planets.append(planet)

return new_planets

\# Function to save data to CSV file

def save_to_csv(data, filename):

with open(filename, 'w', newline='') as csvfile:

fieldnames = \['Planet Name', 'Host Name', 'Discovery Method'\]

writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

writer.writeheader()

for planet in data:

writer.writerow({'Planet Name': planet\['pl_name'\], 'Host Name': planet\['pl_hostname'\], 'Discovery Method': planet\['pl_discmethod'\]})

\# Main function

def main():

\# Fetch data from NASA Exoplanet Archive

exoplanet_data = fetch_exoplanet_data()

if exoplanet_data:

\# Filter new planets discovered in the previous week

new_planets = filter_new_planets(exoplanet_data)

\# Save filtered data to CSV file

save_to_csv(new_planets, 'new_planets_summary.csv')

print(f"Summary of {len(new_planets)} new planets discovered in the previous week saved to 'new_planets_summary.csv'.")

if \__name__ == "\__main_\_":

main()

This script retrieves data from the NASA Exoplanet Archive, filters out the planets discovered in the previous week, and then saves the summary to a CSV file named new_planets_summary.csv. The summary includes information such as the planet name, host name, and discovery method.

**Create a script that uses the HAPI API to store data from the Parker Solar Probe in an array. Output the summary in a JSON format. \[March 15, 2024\]**

ChatGPT

Below is a Python script that uses the HAPI API to fetch data from the Parker Solar Probe and stores it in an array. The script then outputs the summary in JSON format:

python

Copy code

import requests

import json

def fetch_data():

\# Define HAPI API URL

url = "<https://api.nasa.gov/heliophysics/hapi/dataset?spase_id=urn:nasa:pds:psi:parker_solar_probe::&parameters=epoch_\_CDET_PLUS_V&start=2024-01-01T00:00:00Z&end=2024-01-02T00:00:00Z&format=json&api_key=YOUR_API_KEY>"

try:

response = requests.get(url)

if response.status_code == 200:

data = response.json()

return data

else:

print("Error fetching data. Status code:", response.status_code)

return None

except Exception as e:

print("Error fetching data:", e)

return None

def parse_data(data):

parsed_data = \[\]

if data:

for entry in data\['data'\]:

timestamp = entry\['Epoch_\_CDET_PLUS_V'\]

\# Assuming there's only one parameter in this example

parameter_value = entry\['data'\]\[0\]

parsed_data.append({'timestamp': timestamp, 'parameter_value': parameter_value})

return parsed_data

def main():

fetched_data = fetch_data()

if fetched_data:

parsed_data = parse_data(fetched_data)

summary = {'data': parsed_data}

\# Output summary in JSON format

print(json.dumps(summary, indent=4))

if \__name__ == "\__main_\_":

main()

Make sure to replace "YOUR_API_KEY" in the URL with your actual NASA API key. This script fetches data from the Parker Solar Probe for a specific date range (in this case, January 1st, 2024, to January 2nd, 2024), and it fetches data for the parameter epoch_\_CDET_PLUS_V. You can modify the URL parameters according to your requirements.