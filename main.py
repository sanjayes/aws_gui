import boto3
# import pprint
from aws import ec2


def describe():
    ec2.describe()


def create():
    client = boto3.client('ec2', region_name='ap-south-1')
    lst = []
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_security_groups
    img_id = input("\nImage ID (ami-0123b531fc646552f): ") or "ami-0123b531fc646552f"

    inst_type = input("\nInstance Type (t2.micro): ") or "t2.micro"

    key = input("\nKey (key) : ") or "key"

    print("\nSecurity Group (default) : ")
    for a in client.describe_security_groups()['SecurityGroups']:
        print(a['GroupName'])
    s_g = input() or "default"

    tag = input("\nTag Name: ")

    count = input("\nCount (1) : ") or 1
    client.create(img_id, inst_type, key, s_g, tag, count)


def terminate():
    inst_id = input("Instance ID: ")
    ec2.terminate(inst_id)


def exi():
    exit()


def aws():
    print("\n")
    describe()
    print("\n1. Describe\n2. Create\n3. Terminate\nx. Exit\n")
    i = input() or "x"
    # i = '1'
    switcher = {
        '1': describe,
        '2': create,
        '3': terminate,
        'x': exi
    }
    response = switcher.get(i, lambda: "Invalid")()
    if response == 'Invalid':
        print(response)
    print("\n")
    aws()


aws()
