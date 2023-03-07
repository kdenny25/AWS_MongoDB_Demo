import boto3
import paramiko
import time
import pymongo

instance_id = 'i-0b850256c1dc59029'
ip_address = "ec2-52-205-78-57.compute-1.amazonaws.com"

def ssh_connect_with_retry(ssh, ip_address, retries):
    if retries > 3:
        return False
    privkey = paramiko.RSAKey.from_private_key_file(
        "C:/Users/kdenn/OneDrive/Documents/School/CS378_NoSQL Databases/Ubuntu_MongoDB.pem")
    interval = 5

    try:
        retries += 1
        print('SSH into the instance: {}'.format(ip_address))
        ssh.connect(hostname=ip_address,
                    username='ubuntu',
                    pkey=privkey)
        return True
    except Exception as e:
        print(e)
        time.sleep(interval)
        print('Retrying SSH connection to {}'.format(ip_address))
        ssh_connect_with_retry(ssh, ip_address, retries)

# get instance ID from AWS dashboard
# ec2 = boto3.resource('ec2', region_name='us-east-1e')
# instance = ec2.Instance(id=instance_id)
# instance.wait_until_running()
# current_instance = list(ec2.instances.filter(InstanceIDs=[instance_id]))
# ip_address = current_instance[0].public_ip_address

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh_connect_with_retry(ssh, ip_address, 0)

stdin, stdout, stderr = ssh.exec_command("mongosh")


print('stdout: ', stdout.read())
print('stderr: ', stderr.read())