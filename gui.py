from tkinter import Label, Button, Tk, Listbox, END, Frame, LEFT, BOTTOM
import boto3

root = Tk()
root.title("AWS")
root.geometry()

frame = Frame(root)
frame.pack(side=BOTTOM)

label = Label(root, bg='white')
label.pack()

listbox = Listbox(root, width=85)
listbox.pack()


def create_data():
    pass


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


desc = Button(frame, text="Instances", command=describe)
cre = Button(frame, text="Create")

desc.pack(side=LEFT)
cre.pack(side=LEFT)

describe()

root.mainloop()
