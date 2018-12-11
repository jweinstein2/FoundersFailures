Please direct any questions to jared.weinstein@yale.edu

# Setup
### Dependencies
1. `git clone https://github.com/jweinstein2/FoundersFailures.git`
2. `virtualenv venv`
3. `source venv/bin/activate`
4. `pip install -r requirements.txt`
5. `python app.py`

### Start Postfix Server (Mac)
1. [How to send emails from localhost (MAC OS X El Capitan) | Developer files](https://www.developerfiles.com/how-to-send-emails-from-localhost-mac-os-x-el-capitan/)
2. `sudo postfix start`
3. Edit the send email address in line 48 to be your own. If you’re using gmail make sure to allow insecure apps. 

### Connecting to Typeform
1. `ngrok http 5000`
Starts a tunnel giving your survey web hook access to localhost
2.  `curl --silent --show-error http://127.0.0.1:4040/api/tunnels | sed -nE 's/.*public_url":"https:..([^"]*).*/\1/p'`
Outputs the url to point to.
3.  `curl --request PUT --url https://api.typeform.com/forms/vQlUHl/webhooks/VC --header 'Authorization: bearer [AUTHORIZATION]' --header 'Content-Type: application/json' -d '{"url":"[URL]", "enabled":true}'`
Tells typeform where to send your results

# File Structure
1. `app.py` gets a flask server up and running. There is a single endpoint that processes the survey results, and sends an email with the compiled report. 
2. `analyze.py` does simple work to simplify the data before building the report
3. `send.py` sends email from 
4. `generate.py` uses the data from analyze to build and save a customized report. More work is required to clean up this class. 
