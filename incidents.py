import json
import requests
import logging

class GetOpenIncidents():
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
                  nrql(query: "SELECT incidentId, mutingId, policyName, conditionName, evalType, target, entity, app_support_team FROM (SELECT uniqueCount(event) as 'total', latest(event) as 'state', latest(priority) as 'priority', latest(muted) as 'muted', latest(mutingRuleId) as 'mutingId', latest(evaluationType) as 'evalType', latest(targetName) as 'target', latest(entity.name) as 'entity', latest(tags.app_support_team) as 'app_support_team' FROM NrAiIncident where event in ('open','close') facet incidentId, policyName, conditionName limit max) where total=1 and state='open' and muted is true limit max since 1 day ago") {{
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

    def getOpenIncidents(self):
        try:
            resp = self.sendRequest()
            logging.debug('OpenIncidents')
            logging.debug(resp.json())
            if (resp.status_code == 200):
                parsed = resp.json()
                incidents = parsed['data']['actor']['account']['nrql']['results']
            else:
                logging.error('Failed to get open incidents. Response: ' + str(resp.status_code))
        except Exception as e:
            logging.exception('Exception occurred - Failed to get open incidents')
            raise

        return(incidents)
