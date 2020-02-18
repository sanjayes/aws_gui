import sys
from tkinter import Label, Button, Tk, Listbox, END, Frame, LEFT, simpledialog, messagebox, BOTTOM
import boto3
import threading

root = Tk()
root.title("Amazon Web Services")

frame = Frame(root)
frame.pack(side=BOTTOM)

label = Label(root)
label.pack()

listbox = Listbox(root, width=85)
listbox.pack(side=LEFT)

statebox = Listbox(root)
statebox.pack(side=LEFT)


def create():
    img_id = simpledialog.askstring("Instance Details", "Image ID (ami-0123b531fc646552f):")
    # if img_id is None:
    #     breakpoint(None)
    inst_type = simpledialog.askstring("Instance Details", "Instance type (t2.micro):")
    # if inst_type is ' ':
    #     inst_type = "t2.micro"
    key = simpledialog.askstring("Instance Details", "Key:")
    # if key is ' ':
    #     key = "key"
    tag = simpledialog.askstring("Instance Details", "Tag:")
    # if tag is ' ':
    #     tag = " "
    s_g = simpledialog.askstring("Instance Details", "Security Group (default):")
    # if s_g is ' ':
    #     s_g = "default"
    c = simpledialog.askinteger("Instance Details", "Max Count (1):", initialvalue=1)
    # if c is ' ':
    #     c = 1
    if img_id is None or inst_type is None or key is None or c is None:
        messagebox.showwarning("Error", "Incomplete Information")
        breakpoint(None)

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

    messagebox.showinfo("Information", "Instance Created Successful")


def describe():
    listbox.delete(0, END)
    ec2 = boto3.client('ec2')
    # print(ec2.describe_instances()['Reservations'][0]['Instances'][0]['InstanceId'])
    # print(ec2.describe_instances()['Reservations'][0]['Instances'][0]['SecurityGroups'][0]['GroupId'])
    # print(ec2.describe_instances()['Reservations'][0]['Instances'][0]['State']['Name'])
    label.config(text=(
        "         Instance ID         |      Public IP      |                                        Public DNS                                 |    State    "))
    for a in ec2.describe_instances()['Reservations']:
        # pprint.pprint(a)
        for b in a['Instances']:
            # pprint.pprint(b)
            for c in b['NetworkInterfaces']:
                # pprint.pprint(c)
                try:
                    # listbox.insert(END, "| " + b['InstanceId'] + " | " + b['PublicIpAddress'] + "|  " + b['State'][
                    #     'Name'] + " | " + c['Association']['PublicDnsName'] + " |")
                    listbox.insert(END,
                                   "   " + b['InstanceId'] + "   |   " + b['PublicIpAddress'] + "    |    " +
                                   c['Association'][
                                       'PublicDnsName'])
                except Exception:
                    # listbox.insert(END, "| " + b['InstanceId'] + " | -------------- |  " + b['State']['Name'] +
                    #                " | -------------------------------------------------- |")
                    listbox.insert(END, b[
                        'InstanceId'] + " | -------------- | -------------------------------------------------- ")

    def state():
        for d in ec2.describe_instances()['Reservations']:
            # pprint.pprint(a)
            for e in d['Instances']:
                # pprint.pprint(b)
                for f in e['NetworkInterfaces']:
                    # pprint.pprint(c)
                    statebox.insert(END, "      " + e['State']['Name'])

    t = threading.Timer(2.0, state)
    t.setDaemon(True)
    t.start()


def close():
    sys.exit()


close = Button(root, text="x", command=close)
cre = Button(root, text="Create", command=create)

close.pack()
cre.pack()

describe()

root.mainloop()
