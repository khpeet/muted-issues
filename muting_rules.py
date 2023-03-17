import json
import requests
import logging

class GetMutingRules():
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
                  alerts {{
                    mutingRules {{
                      name
                      id
                      enabled
                      status
                    }}
                  }}
                }}
              }}
            }}
        '''
        self.vars = {}


    def sendRequest(self):
        res = requests.request("POST", self.url, headers=self.headers, json={'query': self.query, 'variables': self.vars})
        return res

    def getMutingRules(self):
        try:
            resp = self.sendRequest()
            logging.debug('GetMutingRules')
            logging.debug(resp.json())
            if (resp.status_code == 200):
                parsed = resp.json()
                rules = parsed['data']['actor']['account']['alerts']['mutingRules']
            else:
                logging.error('Failed to get muting rules. Response: ' + str(resp.status_code))
        except Exception as e:
            logging.exception('Exception occurred - Failed to get muting rules')
            raise

        return(rules)
