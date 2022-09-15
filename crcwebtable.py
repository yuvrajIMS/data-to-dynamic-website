# CSV to Table
import csv 
from flask import Flask 
from flask import render_template_string

# Creating web app's instance 
app = Flask('__name__')
# read data from CSV 
@app.route('/')
def read():
    # varibable to hold CSV data
    data = []
    # read data from CSV file
    with open('crc1.csv','r') as f:
        # create csv dictionary render instance
        reader = csv.DictReader(f)
        # initialize CSV dataset
        for row in reader:
           data.append(dict(row)) # [data.append(dict(row)) for row in reader]
    # render HTML page dynamically 
    return render_template_string('''
    <html>
        <head>
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/css/bootstrap.min.css" />
        </head>
        <body>
            <h1> CRC 1456 DATASETS </h1>
            <h2> Research data </h2>
            <div class = "crc">
                <!-- CSV data -->
                <table class="table table-striped mt-5">
                    <thead>
                        <tr>
                            {% for header in data[0].keys() %}
                            <th scope="col">{{header}}</th>
                            {% endfor %}                         
                        </tr>
                    </thead>
                    <tbody>
                       {% for row in data %}   
                            <tr>
                              {% for col in range(0,len(list(row.values()))) %}
                                <td>{{ list(row.values())[col] }}</td>
                              {% endfor %}
                            </tr>
                        {% endfor %} 
                    </tbody>
                </table>
            </div>
        </body>
    </html>
    ''',data = data, list=list, len=len)

# run HHTP server
if __name__ == '__main__':
    app.run(debug=True, threaded = True)

  