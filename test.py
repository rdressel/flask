#!/usr/bin/env python3
import csv
import os

my_list = [120, 330, 431, 113, 13, 2, 1123]
report_data={'i-08c5bc5763cebdac5': {'AWS Account': 'lhamsbox_ro', 'Instance ID': 'i-08c5bc5763cebdac5', 'Project Tag': 'ng-infra-na', 'Name Tag': 'cloudendure replication server con17', 'Type': 't3.small', 'State': 'running', 'Private IP': '10.44.56.132', 'Public IP': None, 'IAM Profile': 'DefaultInstanceProfile'},
'i-036bd2d2b3e756890': {'AWS Account': 'lhamsbox_ro', 'Instance ID': 'i-036bd2d2b3e756890', 'Project Tag': 'ng-infra-na', 'Name Tag': 'CloudEndure Replication Server con17', 'Type': 't3.small', 'State': 'running', 'Private IP': '10.44.56.230', 'Public IP': None, 'IAM Profile': 'DefaultInstanceProfile'},
'i-03fa271b45679d6b8': {'AWS Account': 'lhamsbox_ro', 'Instance ID': 'i-03fa271b45679d6b8', 'Project Tag': 'ng-infra-na', 'Name Tag': 'amanpocinqa02.na.holcim.net', 'Type': 't3.medium', 'State': 'stopped', 'Private IP': '10.44.56.77', 'Public IP': None, 'IAM Profile': 'DefaultInstanceProfile'},
'i-0366735c10d5b998a': {'AWS Account': 'lhamsbox_ro', 'Instance ID': 'i-0366735c10d5b998a', 'Project Tag': 'ng-infra-na', 'Name Tag': 'Win2012R2NEW', 'Type': 't3a.medium', 'State': 'running', 'Private IP': '10.44.56.127', 'Public IP': None, 'IAM Profile': 'DefaultInstanceProfile'},
}


w = csv.writer(open("output.csv", "w"))
is_first_pass=True
for item in report_data.keys():
    key_list=[]
    value_list=[]
    for k, v in report_data[item].items():
        key_list.append(k)
        value_list.append(v)
    if is_first_pass:
        # write header
        is_first_pass=False
        w.writerow(key_list)
        print(key_list)
    w.writerow(value_list)
    print(values)


for key, val in dict.items():
    w.writerow([key, val])


for item in report_data.keys():
    for key, value in report_data[item].items():





csvList=''
for item in report_data.keys():
    row=''
    for key, value in report_data[item].items():
        if value is None:  # Test for NoneType
            value=''
        row+=str(value)
    csvList+=row

def generate():
    for row in report_data():
        yield ','.join(row) + '\n'

print(generate())

return Response(generate(), mimetype='text/csv')




def WriteDictToCSV(csv_file,csv_columns,dict_data):
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in dict_data:
                writer.writerow(data)
    except IOError as err:
            print("I/O error({0})".format(err)    
    return            

csv_columns = ['Row','Name', 'Age', 'Country']
dict_data = [
    {'Row': 1, 'Name': 'John', 'Age': 20, 'Country': 'Australia'},
    {'Row': 2, 'Name': 'Peter', 'Age': 20, 'Country': 'USA'},
    {'Row': 3, 'Name': 'Simon', 'Age': 25, 'Country': 'China'},
    {'Row': 4, 'Name': 'Alex', 'Age': 21, 'Country': 'Germany'},
    ]

currentPath = os.getcwd()
csv_file = currentPath + "/csv/Names.csv"

WriteDictToCSV(csv_file,csv_columns,dict_data)


def highest_even(number_list):
    highest = 0
    for number in number_list:
        if not(number % 2) and number > highest:
            highest = number
    return(highest)


print(highest_even(my_list))
