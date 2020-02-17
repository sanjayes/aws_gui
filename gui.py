from tkinter import Tk, Listbox, Label, END, simpledialog, Button
import threading

import boto3

root = Tk()
root.title("Amazon Web Services")

label = Label(root)
label.pack()

listbox = Listbox(root, width=85)
listbox.pack()


def main():
    listbox.delete(0, END)
    ec2 = boto3.client('ec2')

    # Examples
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

    # https://stackoverflow.com/questions/14694408/runtimeerror-main-thread-is-not-in-main-loop
    sync = threading.Timer(0.5, main)
    sync.setDaemon(True)
    sync.start()


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


if __name__ == '__main__':
    main()

desc = Button(root, text="Instances", command=main)
cre = Button(root, text="Create", command=create)

root.mainloop()
