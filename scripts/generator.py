import requests
import pytz
import time

# Path to the directory containing the data file
path = '/home/bfh/def2/data-engineering-challenge/data/'

# Open the file named 'Gyroscope.csv' for reading
with open (path+'Gyroscope.csv') as f:
    # Read all lines from the file into a list
    lines = [line for line in f]

# Get the current timestamp in seconds
ts = time.time()

# Iterate through all lines in the file except the first (header)
for line in lines[1:]:
    # Extract data values from the line, assuming a comma-separated format
    tdata = float(line.split(',')[0])
    xdata = float(line.split(',')[1])
    ydata = float(line.split(',')[2])
    zdata = float(line.split(',')[3])

    # Prepare a JSON payload with the data to send in the POST request
    data = {
        'tdata': int((ts+tdata)*1000),
        'xdata': xdata,
        'ydata': ydata,
        'zdata': zdata,
    }

    # Send the data to the specified endpoint via a POST request
    response = requests.post('http://10.248.16.130:5000/generator', json=data)

    print("-----------------------------------")

    if response.ok:
        print(response.content)
    else:
        print("Something went wrong :(")

    print(response.status_code)

    print("-----------------------------------")
