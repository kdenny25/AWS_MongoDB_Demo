from sshtunnel import SSHTunnelForwarder, open_tunnel
from pymongo import MongoClient
import pprint

EC2_URL = "ec2-52-205-78-57.compute-1.amazonaws.com"

# create tunnel
server = open_tunnel(
    (EC2_URL, 22),
    ssh_pkey="C:/Users/kdenn/OneDrive/Documents/School/CS378_NoSQL Databases/Ubuntu_MongoDB.pem",
    ssh_username='ubuntu',
    remote_bind_address=('172.31.60.120', 22),
)

# start the tunnel
server.start()

mongo = MongoClient('mongodb://127.0.0.1:27017/'
)

db = mongo['MY_DATABASE']
data = db['sidewalk_cafe_permits'].find()
print(data)
# close the tunnel
server.stop()