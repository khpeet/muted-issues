import sys
import requests
import json
import logging
from muting_rules import GetMutingRules
from incidents import GetOpenIncidents
from issues import GetOpenIssues
from close_issue import CloseOpenIssue

#change level to DEBUG for troubleshooting
logging.basicConfig(filename='muting.log', format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

### CONFIG ###
API_KEY = '<user key>'
ACCOUNTID = 1
INGEST_KEY = '<license|insert key>'
### CONFIG ###

def main():
    getRules = GetMutingRules(API_KEY, ACCOUNTID)
    getIncidents = GetOpenIncidents(API_KEY, ACCOUNTID)
    getIssues = GetOpenIssues(API_KEY, ACCOUNTID)
    closeIssue = CloseOpenIssue(API_KEY)
    results = []

    try:
        rules = getRules.getMutingRules()
        incidents = getIncidents.getOpenIncidents()
        issues = getIssues.getOpenIssues()
        for rule in rules:
            if (rule['enabled'] is True):
                if (rule['status'] != 'ACTIVE'):
                    mutingId = int(rule['id'])
                    for incident in incidents:
                        inc_num = round(incident['mutingId'])
                        if (mutingId == inc_num):
                            incidentId = incident['incidentId']
                            for issue in issues:
                                if (incidentId in issue['incidentIds']):
                                    issueId = issue['issueId']
                                    closeResult = closeIssue.closeIssue(ACCOUNTID, issueId)
                                    results.append({'eventType': 'CloseMutedIssueResult', 'conditionName': incident['conditionName'], 'policyName': incident['policyName'], 'issueId': issueId, 'closeResult': closeResult})
        if (len(results) > 0):
            postResults(results)
        else:
            logging.info('No results to post.')
    except Exception as e:
        raise
        sys.exit(1)

def postResults(res):
    uri = 'https://insights-collector.newrelic.com/v1/accounts/' + str(ACCOUNTID) + '/events'
    h = {
      'X-Insert-Key': INGEST_KEY,
      'Content-Type': 'application/json'
    }

    data = json.dumps(res)

    resp = requests.post(uri, headers=h, data=data)
    if (resp.status_code == 200):
        logging.info('Posted to Results to NRDB successfully')
        pass
    else:
        logging.error('Failed to post results to NRDB: ' + str(resp.status_code))
        logging.debug(resp)


if __name__ == '__main__':
    main()
