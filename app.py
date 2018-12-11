from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import json
import analyze, generate, send

app = Flask(__name__)
CORS(app)

"9fy29EsGXLZL3bZ1uhzn8qqxYQsvw7PePtajFSGFFEb3"

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/', methods = ['POST'])
def handle_response(testing=False):
    print("RESPONSE RECEIVED")

    if not testing:
        json_data = request.get_json()
        with open('example', 'w') as f:
            json.dump(json_data, f)
    else:
        with open('example', 'r') as f:
            json_data = json.load(f)

    answers = json_data['form_response']['answers']

    # Administrative Information
    email = answers[-1]['email']
    name = answers[0]['text']

    answers = answers[1:16]
    fields = json_data['form_response']['definition']['fields'][1:16]

    # Analysis
    data = analyze.wealth_control(answers, fields)

    # Generate Report
    generate.generate(name, data)

    # Send the completed pdf report
    subject = "Your Report is Ready"
    msg = """
Dear {},

Thank you for taking the time to fill out our survey. Below you will find attached the pdf document that summarizes your results. Please take 5 minutes to evaluate the report at https://jaredweinstein.typeform.com/to/NMb5sE".
    """.format(name)
    files = ['generated/wealth_vs_control.pdf']
    send.sendMail([email], 'Founders Feedback <soccerstar199@gmail.com>', subject, msg, files)

    return 'success'

if __name__ == '__main__':
    testing = False

    if not testing:
        app.run(debug=True)
    handle_response(True)
