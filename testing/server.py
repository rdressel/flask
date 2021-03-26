#!/usr/bin/env python3
from flask import Flask, render_template, url_for, request, redirect, make_response, Response, stream_with_context
import csv
from datetime import datetime
from io import StringIO
from werkzeug.datastructures import Headers
from werkzeug.wrappers import Response

import boto3

DATABASE = 'database.txt'
# ACCOUNTS=[(]'lafawsus_ro','lhamnonp_ro','lhamsbox_ro','lhamshare_ro','lhlaprod_ro','lhlanonp_ro','lhlasbox_ro']
ACCOUNTS = ['lhamsbox_ro', 'lhlasbox_ro']

global report_data
report_data = {}


app = Flask(__name__)


@app.route('/')
def my_home():
    '''
    Home page
    '''
    return render_template('index.html')


@app.route('/download')
def download():
    def generate():
        process_data = StringIO()
        print(type(process_data))
        print(type(csv))
        w = csv.writer(process_data)
        print(type(w))

        is_first_pass=True
        for item in report_data.keys():
            key_list=[]
            value_list=[]
            for key, value in report_data[item].items():
                key_list.append(key)
                value_list.append(value)
            # write header
            if is_first_pass:
                is_first_pass=False
                w.writerow(key_list)
                yield process_data.getvalue()
                process_data.seek(0)
                process_data.truncate(0)
            # write row
            w.writerow(value_list)
            yield process_data.getvalue()
            process_data.seek(0)
            process_data.truncate(0)
            print(value_list)

    # add a filename
    headers = Headers()
    headers.set('Content-Disposition', 'attachment', filename='save_report.csv')

    # stream the response as the data is generated
    return Response(
        stream_with_context(generate()),
        mimetype='text/csv', headers=headers
    )


#@app.route('/download')
#def download_log():
#    def generate():
#        data = StringIO()
#        w = csv.writer(data)
#
#        # write header
#        w.writerow(('action', 'timestamp'))
#        yield data.getvalue()
#        data.seek(0)
#        data.truncate(0)
#
#        # write each report_data item
#        for item in report_data:
#            w.writerow((
#                item[0],
#                item[1].isoformat()  # format datetime as string
#            ))
#            yield data.getvalue()
#            data.seek(0)
#            data.truncate(0)
#
#    # add a filename
#    headers = Headers()
#    headers.set('Content-Disposition', 'attachment', filename='save_report.csv')
#
#    # stream the response as the data is generated
#    return Response(
#        stream_with_context(generate()),
#        mimetype='text/csv', headers=headers
#    )

#@app.route('/download')
#def download():
#    print(report_data.keys())
#    for item in report_data.keys():
#        row=csvList=''
#        for key, value in report_data[item].items():
#            if value is None:  # Test for NoneType
#                value=''
#            row+=str(value)
#        csvList+=row
#    #print(csvList)
#    return render_template('index.html')


#@app.route('/download')
#def download():
#    '''
#    Download CSV file
#    '''
#    with open('outputs/report_data.csv', 'w') as csv_file:  
#        writer = csv.writer(csv_file)
#        for item in report_data.keys():
#            for key, value in report_data[item].items():
#                writer.writerow([key, value])
#
#    #print(send_csv(report_data))
#    
#    #    print(item)
#    #    for key, value in report_data[item].items():
#    #        print(key, value)
#    print('')
#    return send_file('outputs/report_data.csv',
#                     mimetype='text/csv',
#                     attachment_filename='report_data.csv',
#                     as_attachment=True)

    # return render_template('index.html')


# @app.route('/submit_form', methods=['POST', 'GET'])
# def submit_form():
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
        report_data, report_title = get_instances()
        # print(report_data)
        if len(report_data) > 0:
            first_item = list(report_data.keys())[0]
            columns = []
            for key, value in report_data[first_item].items():
                columns.append(key)
            return render_template('/run-reports.html', data=report_data, report_columns=report_columns, report_title=report_title)
        else:
            render_template(
                '/error.html', data='No data to be processed.', report_title=report_title)
    else:
        render_template(
            '/error.html', data='Something went wrong, try again.', report_title=report_title)


@app.route('/<string:page_name>')
def html_page(page_name):
    '''
    Dynamic html pages
    '''
    return render_template(page_name)





@app.route('/reports-<string:report_name>')
def report_page(report_name):
    '''
    Dynamic html reports
    '''
    print(report_name)
    if report_name == 'ec2instances':
        report_data, report_title = get_ec2instances()
    else:
        # Report not defined
        return render_template('error.html', data='Report not found...', report_title="Report not found")
    if len(report_data) > 0:
        first_item = list(report_data.keys())[0]
        report_columns = []
        for key, value in report_data[first_item].items():
            report_columns.append(key)
        return render_template('run-reports.html', report_data=report_data, report_columns=report_columns, report_title=report_title)
    else:
        return render_template('error.html', data='No data to be processed.', report_title=report_title)


def write_to_file(data):
    with open(DATABASE, "a", encoding='utf-8') as f:
        f.write('{}\n'.format(data))


def get_tag(tag_name, tags):
    '''
    Get tag key value.
    :param tag_name: Tag name to lookup.
    :param tags: Key, value list from resource.
    :return: Tag value.
    '''
    tagvalue = ''
    if tags is not None:  # Test for NoneType
        for tag in tags:
            if tag["Key"] == tag_name:
                tagvalue = tag["Value"]
    return tagvalue


def get_iam_profile(instance_id, session):
    '''
    Get IAM Profile for Ec2 instances.
    :param instance_id: Instance ID to lookup.
    :param session: AWS session to use.
    :return: IAM profile name.
    '''
    ec2 = session.client('ec2')
    try:
        association_id = 'None'
        response = ec2.describe_iam_instance_profile_associations(
            Filters=[
                {
                    'Name': 'instance-id',
                    'Values': [instance_id]
                }
            ]
        )
        if response['IamInstanceProfileAssociations']:
            profile = response['IamInstanceProfileAssociations'][0]['IamInstanceProfile']['Arn']
            profile = profile[profile.find('/')+1:]  # strip only name
            association_id = response['IamInstanceProfileAssociations'][0]['AssociationId']
        else:
            profile = "none assigned"
    except ec2.exceptions.ClientError as err:
        profile = "error during lookup"
    return(profile)


def get_ec2instances():
    '''
    Get Ec2 instances.
    :return report_data: Dict to generate report.
    :return report_title: HTML title to use.
    '''
    report_title = 'Ec2 Instances by Account'
    for account in ACCOUNTS:
        session = boto3.Session(profile_name=account)
        ec2 = session.resource('ec2')
        for instance in ec2.instances.all():
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
    return (report_data, report_title)
