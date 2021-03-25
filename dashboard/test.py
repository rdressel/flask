#!/usr/bin/env python3

import boto3
SESSION=boto3.Session(profile_name='lhamsbox_ro')

def get_tag(tag_name,tags): 
    tagvalue = '' 
    if tags is not None: # Test for NoneType
        for tag in tags:
            if tag["Key"] == tag_name: 
                tagvalue = tag["Value"]
    return tagvalue

def get_instances():

ec2 = SESSION.resource('ec2')
report_data={}
for instance in ec2.instances.all():
    report_data[instance.id] = {'Instance ID': instance.id, 
        'Project Tag': get_tag('Project', instance.tags),
        'Name Tag': get_tag('Name', instance.tags)
        }
    # for id in report_data.keys():
    #     for key, value in report_data[id].items():
    #         print(key, value)

if len(report_data)>0:
    first_item=list(report_data.keys())[0]
    header=[]
    for key, value in report_data[first_item].items():
        header.append(key)


    print(report_data)


        return report_data


  {% block body %}
  <table class="table">
    <thead class="thead-dark">
      <div class="col">
        <div class="col-15-xs">
          <tr>
            {% for column_name in header%}
              <th>{{ column_name }}</th>
            {% endfor %}
            <th></th>
          </tr>
        </div>
      </div>
    </thead>
      {% for id in data.keys()%}
        <tr>
        {% for key, value in data[id].items() %}
          <td>{{ value }}</td>
          {% if key == 'Name Tag' %}
            <td>{{ value[:20] }}</td>
          {% else %}
            <td>{{ value }}</td>
          {% endif %}
        {% endfor %}
        <th></th>
      </tr>
      {% endfor %}
  </table>
{% endblock %}




  {% block body %}
  <table class="table">
    <thead class="thead-dark">
      <div class="col">
        <div class="col-15-xs">
          <tr>
            {% for column_name in header%}
              <th>{{ column_name }}</th>
            {% endfor %}
            <th></th>
          </tr>
        </div>
      </div>
    </thead>
      {% for id in data.keys()%}
        <tr>
        {% for key, value in data[id].items() %}
          <td>{{ value }}</td>
        {% endfor %}
        <th></th>
      </tr>
      {% endfor %}
  </table>
{% endblock %}