import json
import requests
import logging

class GetOpenIssues():
    def __init__(self, key, accountId):
        self.url = 'https://api.newrelic.com/graphql'
        self.headers = {
            'Content-Type': 'application/json',
            'API-Key': key
        }
        self.query = f'''
            {{
              actor {{
                account(id: {accountId}) {{
                  nrql(timeout: 90, query: "SELECT incidentIds, issueId FROM (FROM NrAiIssue SELECT uniqueCount(event) as 'total', latest(event) as 'state', latest(muted) as 'muted' where event in ('activate', 'create', 'close') facet issueId, incidentIds limit max) where total = 2 and state = 'activate' and muted = 'fullyMuted' limit max since 1 day ago") {{
                    results
                  }}
                }}
              }}
            }}
        '''
        self.vars = {}


    def sendRequest(self):
        res = requests.request("POST", self.url, headers=self.headers, json={'query': self.query, 'variables': self.vars})
        return res

    def getOpenIssues(self):
        try:
            resp = self.sendRequest()
            logging.debug('OpenIssues')
            logging.debug(resp.json())
            if (resp.status_code == 200):
                parsed = resp.json()
                incidents = parsed['data']['actor']['account']['nrql']['results']
            else:
                logging.error('Failed to get open issues. Response: ' + str(resp.status_code))
        except Exception as e:
            logging.exception('Exception occurred - Failed to get open issues')
            raise

        return(incidents)
