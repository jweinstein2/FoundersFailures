from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import analyze, generate, send

app = Flask(__name__)
CORS(app)

"9fy29EsGXLZL3bZ1uhzn8qqxYQsvw7PePtajFSGFFEb3"

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/response/', methods = ['POST'])
def handle_response():
    print("RESPONSE RECEIVED")
    json = request.get_json()
    answers = json['form_response']['answers']

    # Administrative Information
    email = answers[-1]['email']
    name = answers[0]['text']

    # Question Breakdown
    wealthcontrol_q = {'jDsxSXt5EgLL', 'qQW47QEs9oEd', 'MILiZULYdV27', 's3mkuuO14uUs',
                     'iLPSvUbF6Oyy', 'SsQi6eslA3XU', 'yDR7uSnMsrBo', 'NXANdgpyVf7o',
                     'ZdxfyWUwCAaI', 'VkhUMMXGkNeM', 'g9oxdkvrVC9w', 'vnNMV7zDDjIh',
                     'IAQgXtCOxTpV', 'ZtaPKhAYvD1q', 'IRdum1N08oev'}
    wealthcontrol_a = answers[1:15]
    for ans in answers:
        pass

    # Send the completed pdf report
    subject = "Your Report is Ready"
    msg = """
Dear {},

Thank you for taking the time to fill out our survey. Below you will find attached the pdf document that summarizes your results. Please provide feedback at the link below.
    """.format(name)
    files = ['generated/name(wealth_vs_control).pdf']
    send.sendMail([email], 'Founders Feedback <soccerstar199@gmail.com>', subject, msg, files)

    return 'success'

if __name__ == '__main__':
    app.run(debug=True)
