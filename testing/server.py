#!/usr/bin/env python3

from flask import Flask, render_template, url_for, request, redirect
import boto3

DATABASE = 'database.txt'
# ACCOUNTS=('lafawsus_ro','lhamnonp_ro','lhamsbox_ro','lhamshare_ro','lhlaprod_ro','lhlanonp_ro','lhlasbox_ro')
ACCOUNTS = ('lhamsbox_ro','lhlasbox_ro')

app = Flask(__name__)


@app.route('/')
def my_home():
    return render_template('index.html')


#@app.route('/submit_form', methods=['POST', 'GET'])
#def submit_form():
#    if request.method == 'POST':
#        data = request.form.to_dict()
#        write_to_file(data)
#        return redirect('/thankyou.html')
#    else:
#        return 'Something went wrong, try again.'
#
#
#@app.route('/submit_report', methods=['POST', 'GET'])
#def submit_report():
#    if request.method == 'POST':
#        data = request.form.to_dict()
#        report_data = get_instances()
#        # print(report_data)
#        if len(report_data) > 0:
#            first_item = list(report_data.keys())[0]
#            header_data = []
#            for key, value in report_data[first_item].items():
#                header_data.append(key)
#            return render_template('/runreports.html', data=report_data, header=header_data)
#        else:
#            return 'No data to be processed.'
## return render_template('reportec2all.html',data=ec2_dict, profile_name=name_profile, profile=profile, admin="admin"==profile['role'])
#    else:
#        return 'Something went wrong, try again.'
#
#
@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)
#
#
#def write_to_file(data):
#    with open(DATABASE, "a", encoding='utf-8') as f:
#        f.write('{}\n'.format(data))
#
#
#def get_tag(tag_name, tags):
#    tagvalue = ''
#    if tags is not None:  # Test for NoneType
#        for tag in tags:
#            if tag["Key"] == tag_name:
#                tagvalue = tag["Value"]
#    return tagvalue
#
#
#def get_iam_profile(instance_id, session):
#    ec2 = session.client('ec2')
#    try:
#        association_id='None'
#        response = ec2.describe_iam_instance_profile_associations(
#            Filters=[
#                {
#                'Name': 'instance-id',
#                'Values': [instance_id] 
#                } 
#            ]
#        )
#        if response['IamInstanceProfileAssociations']:
#            profile=response['IamInstanceProfileAssociations'][0]['IamInstanceProfile']['Arn']
#            profile = profile[profile.find('/')+1:]  # strip only name
#            association_id=response['IamInstanceProfileAssociations'][0]['AssociationId']
#        else:
#            profile="none assigned"
#    except ec2.exceptions.ClientError as err:
#        profile="error during lookup"
#    return(profile)
#    
#
#def get_instances():
#    report_data = {}
#    for account in ACCOUNTS:
#        session = boto3.Session(profile_name=account)
#        ec2 = session.resource('ec2')
#        for instance in ec2.instances.all():
#            # print(instance.id)
#            report_data[instance.id] = {
#                'AWS Account': account,
#                'Instance ID': instance.id,
#                'Project Tag': get_tag('Project', instance.tags),
#                'Name Tag': get_tag('Name', instance.tags),
#                'Type': instance.instance_type,
#                'State': instance.state['Name'],
#                'Private IP': instance.private_ip_address,
#                'Public IP': instance.public_ip_address,
#                'IAM Profile': get_iam_profile(instance.id, session),
#                'Launch Time': instance.launch_time,
#            }
#    return (report_data)
#