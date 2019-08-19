from flask import Flask
from jenkinsapi.jenkins import Jenkins
from jenkinsapi.utils.crumb_requester import CrumbRequester
from flask import request
import logging
import configparser
from threading import Thread

logging.basicConfig(level=logging.DEBUG)
jenkins_username = ""
jenkins_token = ""
jenkins_url = ""
app = Flask(__name__)
datastore = {}
jenkinsconfig = configparser.ConfigParser()

def loadjenkins():
    try:
        global jenkins_token, jenkins_username, jenkins_url
        jenkinsconfig.read("config.ini")
        jenkins_url = jenkinsconfig.get("JENKINS_PARAMETER", "jenkins_url")
        jenkins_username = jenkinsconfig.get("JENKINS_PARAMETER", "user")
        jenkins_token = jenkinsconfig.get("JENKINS_PARAMETER", "token")
    except FileNotFoundError:
        logging.error("Unable to read config file or file does not exist")

loadjenkins()

def postUrl(jobname, parameter):
    loadjenkins()
    crumb = CrumbRequester(username=jenkins_username, password=jenkins_token, baseurl=jenkins_url)
    logging.debug("Jobname " + jobname)
    logging.debug("Parameter List " + json.dumps(parameter))
    jenkins = Jenkins(jenkins_url, username=jenkins_username,
                                         password=jenkins_token, requester=crumb, timeout=30)
    jenkins.build_job(jobname, parameter)

@app.route('/build', methods=['POST'])
def trigger_build():
    '''
        This is api is used to execute jenkins job.
        Data format example:
        {"data":{"parameter":{"param1":"value1","param2": "value2"},"jobname":"FireBuild"}}
    '''
    final = request.get_json()
    datastore = final['data']
    try:
        t1 = Thread(target=postUrl, args=(datastore['jobname'], datastore['parameter']))
        t1.start()
    except:
        print('Unable to execute job')
    return 'Job Executed'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8098, debug=True)
