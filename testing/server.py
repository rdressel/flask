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

@app.route('/download')
def download():
    report_data = request.args.get('report_data', None)
    report_columns = request.args.get('report_columns', None)
    print(report_data, report_columns)
    return render_template('index.html')


#@app.route('/submit_form', methods=['POST', 'GET'])
#def submit_form():
#    if request.method == 'POST':
#        data = request.form.to_dict()
#        write_to_file(data)
#        return redirect('/thankyou.html')
#    else:
#        return 'Something went wrong, try again.'


@app.route('/submit_report', methods=['POST', 'GET'])
def submit_report():
    if request.method == 'POST':
        data = request.form.to_dict()
        report_data, report_header = get_instances()
        # print(report_data)
        if len(report_data) > 0:
            first_item = list(report_data.keys())[0]
            columns = []
            for key, value in report_data[first_item].items():
                columns.append(key)
            return render_template('/run-reports.html', data=report_data, report_columns=report_columns, report_header=report_header)
        else:
            render_template('/error.html', data='No data to be processed.', report_header=report_header)
    else:
        render_template('/error.html', data='Something went wrong, try again.', report_header=report_header)


@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)

@app.route('/reports-<string:report_name>')
def report_page(report_name):
    """
    Dynamic html reports
    """
    print(report_name)
    html='run-reports.html'
    report_data=''
    if report_name=='ec2instances':
        report_data, report_header = get_ec2instances()
    else:
        return render_template('error.html', data='Report not found...', report_header="Report not found") # Report not defined
    if len(report_data) > 0: 
        first_item = list(report_data.keys())[0]
        report_columns = []
        for key, value in report_data[first_item].items():
            report_columns.append(key)
        return render_template(html, report_data=report_data, report_columns=report_columns, report_header=report_header)
    else:
        return render_template('error.html', data='No data to be processed.', report_header=report_header)


def write_to_file(data):
    with open(DATABASE, "a", encoding='utf-8') as f:
        f.write('{}\n'.format(data))


def get_tag(tag_name, tags):
    tagvalue = ''
    if tags is not None:  # Test for NoneType
        for tag in tags:
            if tag["Key"] == tag_name:
                tagvalue = tag["Value"]
    return tagvalue


def get_iam_profile(instance_id, session):
    ec2 = session.client('ec2')
    try:
        association_id='None'
        response = ec2.describe_iam_instance_profile_associations(
            Filters=[
                {
                'Name': 'instance-id',
                'Values': [instance_id] 
                } 
            ]
        )
        if response['IamInstanceProfileAssociations']:
            profile=response['IamInstanceProfileAssociations'][0]['IamInstanceProfile']['Arn']
            profile = profile[profile.find('/')+1:]  # strip only name
            association_id=response['IamInstanceProfileAssociations'][0]['AssociationId']
        else:
            profile="none assigned"
    except ec2.exceptions.ClientError as err:
        profile="error during lookup"
    return(profile)
    
def get_ec2instances():
    report_header='Ec2 Instances by Account'
    report_data = {}
    for account in ACCOUNTS:
        session = boto3.Session(profile_name=account)
        ec2 = session.resource('ec2')
        for instance in ec2.instances.all():
            # print(instance.id)
            report_data[instance.id] = {
                'AWS Account': account,
                'Instance ID': instance.id,
                'Project Tag': get_tag('Project', instance.tags),
                'Name Tag': get_tag('Name', instance.tags),
                'Type': instance.instance_type,
                'State': instance.state['Name'],
                'Private IP': instance.private_ip_address,
                'Public IP': instance.public_ip_address,
                'IAM Profile': get_iam_profile(instance.id, session),
                'Launch Time': instance.launch_time,
            }
    return (report_data, report_header)


