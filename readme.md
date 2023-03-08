# AWS MongoDB Demo

## Purpose:
The purpose of this demo is to understand how to use MongoDB using AWS. 
First MongoDB is installed on an AWS EC2 instance of Ubuntu. Then create
an SSH tunnel to start interacting with the NoSQL database. I will document
all steps in this process for future implementations like a Flask app.

## Creating an AWS EC2 Instance

Log into AWS and navigate to the EC2 Dashboard.
![img.png](static/readme_images/EC2_Dashboard.png)

Select the orange button "Launch Instance". This will bring you to the
launch instance setup menu.
![img.png](static/readme_images/launch_instance.png)

The first step is naming your instance. You can name it whatever you like.
![img.png](static/readme_images/EC2_Naming.png)

Then select an Application and OS Image. For this example select Ubuntu
and make sure you have the Free tier eligible version of the server. Use
the settings from the image below.

![img.png](static/readme_images/EC2_Application_OS Image.png)

Next, instance type should be t2.micro of the Free tier eligible version.

![img.png](static/readme_images/EC2_Instance Type.png)

This part is important if you want to use SSH tunneling to interact with
the database. Make sure you create a new key pair and save the file somewhere
secure.

![img.png](static/readme_images/EC2_Key Pair.png)

You can use the defaults in the Network Settings and Configure Storage portions
of the forms and launch the instance.

![img.png](static/readme_images/EC2_Network_Storage.png)

## Access EC2 Instance through SSH

Now that you have created the EC2 instance you should see a green banner
stating that you have successfully initiated launch of instance along
with a random looking link. This link is your instance id. Go ahead and 
click it.

![img.png](static/readme_images/launch_success.png)

Clicking the link will bring you to the instance dashboard filtering only
the instance you just created. 

![img.png](static/readme_images/instance_dashboard.png)

In this view make note that the Instance State is "Running" and the 
Status Check is "2/2 checks passed". If all is good then click the 
instance ID again.

![img.png](static/readme_images/instance_details.png)

From this view select 'Connect'. This will take you to methods for 
connecting to your EC2 instance. I'll be providing the commands to SSH 
into your instance so this window isn't providing you anything new
but, this window also provides you with the command and it is always good 
to know where you can find this information.

![img.png](static/readme_images/instance_connect.png)

Now, we are ready to SSH into our EC2 instance. Windows 10 and 11 should 
come stock with an SSH client built into their command line same with
Mac. If you have an older Windows operating system I would use PuTTY 
from putty.org. 



## Installing MongoDB

Once logged into your EC2 instance through an SSH client you can start 
following steps to install MongoDB. All steps in this section follow
the tutorial by MongoDB, here: https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/

The first step is importing the public key

    wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -

You should get a response with an OK.

![img.png](static/readme_images/mongodb_install_public_key.png)

Next create a list file for MongoDB. We are using Ubuntu 22.04 in this
tutorial. If this has changed please follow the tutorial by MongoDB.

    echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list

![img.png](static/readme_images/mongodb_install_create_list_file.png)

Then reload the local pack database.

    sudo apt-get update

This will process a lot of GET responses. The end result should look
similar to the following.

![img.png](static/readme_images/mongodb_install_reload_local_package_db.png)

Now you are ready to install MongoDB. To install the latest version use
the following command. There is a method to install a specific release of
MongoDB, please reference the MongoDB tutorial for more information.

    sudo apt-get install -y mongodb-org

Assuming everything went well we can now start MongoDB and check to see
if everything is working as it should.

To start enter the following command to start MongoDB.

    sudo systemctl start mongod

Then verify Mongodb has started.

    sudo systemctl status mongod

If everything is working well you should receive a response similar to
the one below.

![img.png](static/readme_images/mongodb_install_verify_start.png)

You can stop and stop MongoDB using the following commands

    sudo systemctl stop mongod
    sudo systemctl restart mongod

To start using MongoDB and issue commands directly to the database we will
need to enter the MongoDB shell. Type in the following command to open the
shell.

    mongosh

Once loaded you can begin adding and manipulating data within MongoDB.

## Adding Data to MongoDB from MongoDB Shell

Start by typing the mongosh command. This will open the MongoDB Shell. Data
used for this section is from a Kaggle dataset from here: https://www.kaggle.com/datasets/chicago/chicago-sidewalk-cafe-permits
Download the dataset and take a look at it. We will be using this data
to insert values into our database.

![img.png](static/readme_images/mongodb_shell.png)

Create your database with the use database_name command. This will either
create or set this database as primary depending on whether it exists or
not.

    use MY_DATABASE

Then create a user account with the command below:

    db.createUser({
        user: "admin",
        pwd: "P@ssw0rd",
        roles: [
            {role : "readWrite", db : "MY_DATABASE" },
            {role : "userAdmin", db : "MY_DATABASE" },
            {role : "dbAdmin", db: "MY_DATABASE" },
        ]
    })

![img.png](static/readme_images/create_user.png)

Next, create a collection called "sidewalk_cafe_permits". Collections are
NoSQL's version of tables. This is where we will store our permit data.

    db.createCollection("sidewalk_cafe_permits")

![img.png](static/readme_images/create_collection.png)

Now we will be inserting 1 document into our database to 
demonstrate the insertOne() command. For this example we will only use the 
first 9 columns. 

Just enter each entry individually.

    db.sidewalk_cafe_permits.insertOne(
        {
            permit_number:1142666,
            account:458934,
            site_number:1,
            legal_name:"TINTO & TAPAS, LLC",
            doing_business_as_name:"TINTO & TAPAS",
            issued_date:"2019-11-25T00:00:00.000",
            expiration_date:"2020-02-29T00:00:00.000",
            payment_date:"2019-10-29T00:00:00.000",
            address:"7958 W BELMONT AVE"
        }
    )

You should receive an acknowledgment after inserting a document.

![img.png](static/readme_images/insertOne_result.png)

Next we will use insertMany() 

    db.sidewalk_cafe_permits.insertMany([
        {
            permit_number:1142290,
            account:294900,
            site_number:4,
            legal_name:"PIE CAFE, LLC",
            doing_business_as_name:"Pie cafe",
            issued_date:"2019-10-15T00:00:00.000",
            expiration_date:"2020-02-29T00:00:00.000",
            payment_date:"2019-10-15T00:00:00.000",
            address:"5357 N ASHLAND AVE"
        },
        {
            permit_number:1142132,
            account:459163,
            site_number:1,
            legal_name:"KALIFLOWER 333 NORTH MICHIGAN AVE LLC",
            doing_business_as_name:"KALIFLOWER",
            issued_date:"2019-09-20T00:00:00.000",
            expiration_date:"2020-02-29T00:00:00.000",
            payment_date:"2019-09-20T00:00:00.000",
            address:"333 N MICHIGAN AVE"
        },
        {
            permit_number:1142101,
            account:384478,
            site_number:1,
            legal_name:"1732 N MILWAUKEE RESTAURANT LLC",
            doing_business_as_name:"SMALL CHEVAL",
            issued_date:"2019-09-20T00:00:00.000",
            expiration_date:"2020-02-29T00:00:00.000",
            payment_date:"2019-09-20T00:00:00.000",
            address:"1732 N MILWAUKEE AVE"
        },
        {
            permit_number:1142100,
            account:"456144",
            site_number:"1",
            legal_name:"THE WHALE CHICAGO, LLC",
            doing_business_as_name:"THE WHALE CHICAGO",
            issued_date:"2019-09-19T00:00:00.000",
            expiration_date:"2020-02-29T00:00:00.000",
            payment_date:"2019-09-19T00:00:00.000",
            address:"2427-2431 N MILWAUKEE AVE"
        }
    ])

![img.png](static/readme_images/insertMany_results.png)

Now, let's take a look at how many documents we have in our collection.

    db.sidewalk_cafe_permits.count()

![img.png](static/readme_images/collection_count_results.png)

Using find() will print off all documents in your collection.

    db.sidewalk_cafe_permits.find()

# Import CSV to MongoDB using mongoimport

Now that we have figured out how to import single and multiple entries 
let's import an entire CSV file to MongoDB. This method is great when you
want to transition from a relational database to a NoSQL database.

First while we are still in the Mongo Shell you will want to 
use MY_DATABASE then create a new collection.

    use MY_DATABASE
    db.createCollection("earth_quakes")

Next, you will need to exit the Mongo Shell by simply entering in the Exit
command.

    exit()

Then we will need to transfer the csv file from your personal computer
to the remote EC2 instance. Do this by using the Secure Copy command to
securely transfer the file or files to the destination computer. The
command structure is below.

    scp [switch] [source content location] [destination content location]

Here is an explanation of the commands.

- **scp** will activate the Secure Transfer command
- **switch** is an optional parameter indicating whether to transfer one
file or an entire folder. You can use **-r** to transfer an entire folder.
other switch commands are available.
- **content location** syntax will be different depending on whether the file
is located o the server you are logged into or a second remote server.
    - If content on logged in server:
        * /var/www/dir
    - If content on second remote server:
        * [userid]@[remote server 2 url or ip]:[directory or file]



Next we will use mongoimport to import our data from a CSV file into a 
MongoDB database

    mongoimport --db MY_DATABASE --collection earthquakes --type csv --headerline --file="C:/Users/kdenn/OneDrive/Documents/School/CS378_NoSQL Databases/catalog.csv"

