from tkinter import Tk, Listbox, Label, END
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


if __name__ == '__main__':
    main()

root.mainloop()
