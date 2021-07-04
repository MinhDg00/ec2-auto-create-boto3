import boto3
import yaml 
import os
import sys 

class Client:

    def __init__(self, yml_file):
        
        with open(yml_file, 'r') as f:
            file = yaml.load(f, Loader = yaml.FullLoader)
            config = file['server']

            self.instance_type = config['instance_type']
            self.ami_type = config['ami_type']
            self.architecture = config['architecture']
            self.root_device_type = config['root_device_type']
            self.virtualization_type = config['virtualization_type']
            self.min_count = config['min_count']
            self.max_count = config['max_count']
            self.volumes = config['volumes']
            self.users = config['users']
                
            self.block_device_mapping = [
                {
                    'DeviceName': volume['device'],
                    'VirtualName': volume['mount'],
                    'Ebs': {
                        'DeleteOnTermination': True, 
                        'VolumeSize': volume['size_gb'],
                        'VolumeType':'gp2'
                    }
                }

                for volume in self.volumes
            ]
            
            self.key_name = 'ec2_keypair' 
            self.user_data = "#!/bin/bash \n"
            self.imageId = ''

    def create_client(self, access_key, secret, region):

        self.ec2 = boto3.client('ec2', aws_access_key_id = access_key, aws_secret_access_key = secret, region_name = region)
        self.ssm = boto3.client('ssm', aws_access_key_id = access_key, aws_secret_access_key = secret, region_name = region)


    def get_imageId(self):

        query = '/aws/service/ami-amazon-linux-latest/'+self.ami_type+'-ami-'+self.virtualization_type+'-'+self.architecture+'-'+self.root_device_type
        self.imageId = self.ssm.get_parameter(Name=query)['Parameters']['Value']

    def create_userData(self):
        for volume in self.volumes:
            self.user_data += f"mkfs.{volume['type']} {volume['device']}\n"
            self.user_data += f"mkdir {volume['mount']}\n"
            self.user_data += f"mount {volume['device']} {volume['mount']}\n"
            self.user_data += f"chmod 707 /{volume['mount']}\n"
        for user in self.users:
            self.user_data += f"adduser {user['login']} \n"
            self.user_data +=  f"mkdir /home/{user['login']}/.ssh \n"
            self.user_data += f"chmod 700 /home/{user['login']}/.ssh/authorized_keys\n"
            self.user_data += f"echo {user['ssh_key']} > /home/{user['login']}/.ssh/authorized_keys\n"
        
            

    def create_key_pair(self):
        key_pair = self.ec2.create_key_pair(KeyName = self.key_name)
        private_key = key_pair['KeyMaterial']
        with os.fdopen(os.open("aws_ec2_key.pem", os.O_WRONLY | os.O_CREAT, 0o400), "w+") as pem_file:
            pem_file.write(private_key)

        return private_key

    def create_instance(self):
        instances = self.ec2.run_instances(
            BlockDeviceMappings = self.block_device_mapping,
            ImageId = self.imageId, 
            InstanceType = self.instance_type,
            MaxCount =self.max_count,
            MinCount = self.min_count, 
            UserData = self.user_data,
            KeyName = self.key_name
        )

        return instances

if __name__ == '__main__':
    aws_access_key_id = sys.argv[1]
    aws_secret_access_key = int(sys.argv[2])
    region = int(sys.argv[3])
    
    client = Client('config.yml')
    client.create_client(aws_access_key_id, aws_secret_access_key, region)
    client.create_key_pair()
    client.get_imageId()
    client.create_userData()
    client.create_instance()

