 # CSV to LIST 
import csv
from flask import Flask 
from flask import render_template_string

# Creating web app's instance 
app = Flask('__name__')
# Reading CSV 
@app.route('/')
def read():
    # To hold CSV data
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
            <script type="text/javascript">
            function toggleShowHide(elementId) {
                var element = document.getElementById(elementId);
                element.style.height = element.offsetHeight == "500" ? height+"px" : "500px";
                if (element) {
                    if (element.style.display == "none")
                        element.style.display = "inline";
                    else
                        element.style.display = "none";
                }
            }
            </script>
        </head>
        <body>
            <h1> CRC 1456 DATASETS </h1><br>
            <u><h2> Research Data </h2></u>        
            <div class = "crclist">
                <ul style = "">
                    {% for row in data %}
                    <li><h3>{{(row.get("TITLE")[:])}}</h3></li>
                    <b>{{(row.get("AUTHOR")[:])}}</b>
                    ,&ensp;
                    {{(row.get("SUBJECT")[:])}}
                    ,&ensp;
                    {{(row.get("DATE_DEPOSITED")[:])}}
                    ,&ensp;
                    <em>{{(row.get("PID")[:])}}</em>
                    <p onClick="toggleShowHide('{{(row.get("TITLE")[:])}}')"><u><font color='blue'>Description</font></u></p>
                    <div id="{{(row.get("TITLE")[:])}}" style="display:none">{{row.get("DESCRIPTION")[:]}}</div>
                    </em>
                    <br><br>
                    {% endfor %}
                </ul>
            </div>
        </body>
    </html>
    ''',data = data, list=list, len=len, str = str)
# run HTTP server
if __name__ == '__main__':
    app.run(debug=True, threaded = True)
    