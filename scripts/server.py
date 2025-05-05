from flask import Flask, request
import json
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement

server = Flask(__name__)

# Request from browser without further parameters
@server.route('/')
def index():
    message = """
    Hello to the Data Engineering Fundamentals Challenge.<br>
    To set everything up to work, you need to do the following:<br>
    - Start InfluxDB by typing ‘influxd’ into the terminal<br>
    - Start the server script by writing ‘cd def2/scripts/’ and 'python server.py' in the terminal (the server is probably already running, otherwise you wouldn't see this here)<br>
    - And finally start the generator by writing ‘cd def2/scripts/’ and 'python generator.py' in the terminal<br><br>
    Now you can analyse the data in the InfluxDB under ‘http://your-ip:8086/’
    """
    return message

# Request from Browser as: http://http://10.248.16.130:5000/generator
@server.route('/generator', methods=['POST'])
def generator():
    # InfluxDB configuration
    bucket = "challenge"
    org = "BFH"
    token = "5dALrxtzd_AeO098d22ICSYIxsmrkLhnfRBi3Lh9uGqDSRjzb4a56w3M0V_VIAgBhk_k6EgPV8HG3ddVgNKWDA=="
    url="http://localhost:8086"

    # Initialize the InfluxDB client
    client = influxdb_client.InfluxDBClient(
        url=url,
        token=token,
        org=org
    )

    # Parse the JSON data from the POST request body
    data = json.loads(request.data)

    # Create a write API instance for synchronous writes
    write_api = client.write_api(write_options=SYNCHRONOUS)

    # Create a data point for InfluxDB with the 'gyroscope' measurement
    record = influxdb_client.Point("gyroscope") \
        .field("x", data['xdata'])  \
        .field("y", data['ydata'])  \
        .field("z", data['zdata'])  \
        .time(data['tdata'], write_precision='ms')

    # Only write to InfluxDB if the timestamp is valid (greater than 0)
    if (int(data['tdata']) > 0):
        write_api.write(bucket=bucket, record=record)

    # Cassandra integration
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect()

    # Use or create the keyspace
    session.execute("""
    CREATE KEYSPACE IF NOT EXISTS sensor_data
    WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'}
    """)
    session.set_keyspace('sensor_data')

    # Create table if it doesn't exist
    session.execute("""
    CREATE TABLE IF NOT EXISTS gyroscope_data (
        tdata bigint PRIMARY KEY,
        xdata float,
        ydata float,
        zdata float
    )
    """)

    # Prepare and execute insert statement
    insert_query = SimpleStatement("""
    INSERT INTO gyroscope_data (tdata, xdata, ydata, zdata)
    VALUES (%s, %s, %s, %s)
    """)
    session.execute(insert_query, (data['tdata'], data['xdata'], data['ydata'], data['zdata']))

    if cluster:
        cluster.shutdown()

    return data

# Entry point to this script
if __name__ == '__main__':
    server.run(host='0.0.0.0', port=5000)
