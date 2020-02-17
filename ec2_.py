import boto3

from tkinter import simpledialog


# def create(img_id, inst_type, key, s_g, tag, c):
def create():
    img_id = simpledialog.askstring("Instance Details", "Image ID:")
    inst_type = simpledialog.askstring("Instance Details", "Instance type:")
    key = simpledialog.askstring("Instance Details", "Key:")
    tag = simpledialog.askstring("Instance Details", "Tag:")
    s_g = simpledialog.askstring("Instance Details", "Security Group:")
    c = simpledialog.askinteger("Instance Details", "Max Count:")

    ec2 = boto3.resource('ec2')
    ec2.create_instances(
        ImageId=img_id,
        InstanceType=inst_type,
        KeyName=key,
        TagSpecifications=(
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': tag
                    },
                ]
            },
        ),
        SecurityGroups=[
            s_g,
        ],
        MinCount=1,
        MaxCount=c
    )


def describe():
    ec2 = boto3.client('ec2')
    # print(ec2.describe_instances()['Reservations'][0]['Instances'][0]['InstanceId'])
    # print(ec2.describe_instances()['Reservations'][0]['Instances'][0]['SecurityGroups'][0]['GroupId'])
    # print(ec2.describe_instances()['Reservations'][0]['Instances'][0]['State']['Name'])
    lbl.config(text=("|    Instance ID       |   Public IP   |   State   |                     Public DNS             "
                     "      |"))
    for a in ec2.describe_instances()['Reservations']:
        # pprint.pprint(a)
        for b in a['Instances']:
            # pprint.pprint(b)
            for c in b['NetworkInterfaces']:
                # pprint.pprint(c)
                try:
                    lbl.config(text=("| " + b['InstanceId'], " | " + b['PublicIpAddress'], "|  " + b['State']['Name'],
                                     " | " + c['Association']['PublicDnsName'] + " |"))
                except BaseException:
                    lbl.config(text=("| " + b['InstanceId'], " | -------------", "|  " + b['State']['Name'],
                                     " | -------------------------------------------------- |"))


def terminate(instance_id):
    ec2 = boto3.client('ec2')
    ec2.terminate_instances(
        InstanceIds=[instance_id]
    )
