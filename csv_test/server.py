import csv
from datetime import datetime
from io import StringIO
from flask import Flask, stream_with_context
from werkzeug.datastructures import Headers
from werkzeug.wrappers import Response

app = Flask(__name__)

# example data, this could come from wherever you are storing logs
report_data={'i-08c5bc5763cebdac5': {'AWS Account': 'lhamsbox_ro', 'Instance ID': 'i-08c5bc5763cebdac5', 'Project Tag': 'ng-infra-na', 'Name Tag': 'cloudendure replication server con17', 'Type': 't3.small', 'State': 'running', 'Private IP': '10.44.56.132', 'Public IP': None, 'IAM Profile': 'DefaultInstanceProfile'},
'i-036bd2d2b3e756890': {'AWS Account': 'lhamsbox_ro', 'Instance ID': 'i-036bd2d2b3e756890', 'Project Tag': 'ng-infra-na', 'Name Tag': 'CloudEndure Replication Server con17', 'Type': 't3.small', 'State': 'running', 'Private IP': '10.44.56.230', 'Public IP': None, 'IAM Profile': 'DefaultInstanceProfile'},
'i-03fa271b45679d6b8': {'AWS Account': 'lhamsbox_ro', 'Instance ID': 'i-03fa271b45679d6b8', 'Project Tag': 'ng-infra-na', 'Name Tag': 'amanpocinqa02.na.holcim.net', 'Type': 't3.medium', 'State': 'stopped', 'Private IP': '10.44.56.77', 'Public IP': None, 'IAM Profile': 'DefaultInstanceProfile'},
'i-0366735c10d5b998a': {'AWS Account': 'lhamsbox_ro', 'Instance ID': 'i-0366735c10d5b998a', 'Project Tag': 'ng-infra-na', 'Name Tag': 'Win2012R2NEW', 'Type': 't3a.medium', 'State': 'running', 'Private IP': '10.44.56.127', 'Public IP': None, 'IAM Profile': 'DefaultInstanceProfile'},
}

log = [
    ('login', datetime(2015, 1, 10, 5, 30)),
    ('deposit', datetime(2015, 1, 10, 5, 35)),
    ('order', datetime(2015, 1, 10, 5, 50)),
    ('withdraw', datetime(2015, 1, 10, 6, 10)),
    ('logout', datetime(2015, 1, 10, 6, 15))
]

@app.route('/')
def download_log():
    def generate():
        data = StringIO()
        w = csv.writer(data)

        # write header
        w.writerow(('AWS Account', 'Instance ID'))
        yield data.getvalue()
        data.seek(0)
        data.truncate(0)

        # write each log item
        for item in log:
            w.writerow((
                item[0],
                item[1].isoformat()  # format datetime as string
            ))
            yield data.getvalue()
            data.seek(0)
            data.truncate(0)

    # add a filename
    headers = Headers()
    headers.set('Content-Disposition', 'attachment', filename='log.csv')

    # stream the response as the data is generated
    return Response(
        stream_with_context(generate()),
        mimetype='text/csv', headers=headers
    )

app.run()