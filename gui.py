from tkinter import Label, Button, Tk, Listbox, END
import boto3

window = Tk()
window.title("AWS")
window.geometry()
label = Label(window, bg='white')
listbox = Listbox(window, width=85)


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


label.pack()
listbox.pack()

btn = Button(window, text="Instances", command=describe)
btn.pack()

describe()

window.mainloop()
