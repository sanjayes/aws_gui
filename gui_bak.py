import sys
from tkinter import Label, Button, Tk, Listbox, END, Frame, LEFT, BOTTOM, simpledialog
import boto3
import threading

root = Tk()
root.title("Amazon Web Services")

frame = Frame(root)
frame.pack(side=BOTTOM)

label = Label(root)
label.pack()

listbox = Listbox(root, width=85)
listbox.pack()


def create():
    img_id = simpledialog.askstring("Instance Details", "Image ID (ami-0123b531fc646552f):")
    if img_id is None:
        sys.exit()
    # else:
    #     img_id = "ami-0123b531fc646552f"
    inst_type = simpledialog.askstring("Instance Details", "Instance type (t2.micro):")
    if inst_type is ' ':
        inst_type = "t2.micro"
    key = simpledialog.askstring("Instance Details", "Key:")
    if key is ' ':
        key = "key"
    tag = simpledialog.askstring("Instance Details", "Tag:")
    if tag is ' ':
        tag = " "
    s_g = simpledialog.askstring("Instance Details", "Security Group (default):")
    if s_g is ' ':
        s_g = "default"
    c = simpledialog.askinteger("Instance Details", "Max Count (1):", initialvalue=1)
    if c is ' ':
        c = 1

    print(img_id)
    print(inst_type)
    print(key)
    print(tag)
    print(s_g)
    print(c)

    # ec2 = boto3.resource('ec2')
    # ec2.create_instances(
    #     ImageId=img_id,
    #     InstanceType=inst_type,
    #     KeyName=key,
    #     TagSpecifications=(
    #         {
    #             'ResourceType': 'instance',
    #             'Tags': [
    #                 {
    #                     'Key': 'Name',
    #                     'Value': tag
    #                 },
    #             ]
    #         },
    #     ),
    #     SecurityGroups=[
    #         s_g,
    #     ],
    #     MinCount=1,
    #     MaxCount=c
    # )


def describe():
    listbox.delete(0, END)
    ec2 = boto3.client('ec2')
    # print(ec2.describe_instances()['Reservations'][0]['Instances'][0]['InstanceId'])
    # print(ec2.describe_instances()['Reservations'][0]['Instances'][0]['SecurityGroups'][0]['GroupId'])
    # print(ec2.describe_instances()['Reservations'][0]['Instances'][0]['State']['Name'])
    label.config(text=(
        "|         Instance ID         |      Public IP      |    State    |                                        Public DNS                                 |"))
    for a in ec2.describe_instances()['Reservations']:
        # pprint.pprint(a)
        for b in a['Instances']:
            # pprint.pprint(b)
            for c in b['NetworkInterfaces']:
                # pprint.pprint(c)
                try:
                    listbox.insert(END, "| " + b['InstanceId'] + " | " + b['PublicIpAddress'] + "|  " + b['State'][
                        'Name'] + " | " + c['Association']['PublicDnsName'] + " |")
                except Exception:
                    listbox.insert(END, "| " + b['InstanceId'] + " | -------------- |  " + b['State']['Name'] +
                                   " | -------------------------------------------------- |")
    threading.Timer(5.0, describe).start()


desc = Button(frame, text="Instances", command=describe)
cre = Button(frame, text="Create", command=create)

desc.pack(side=LEFT)
cre.pack(side=LEFT)

describe()

root.mainloop()
