import json
import requests
import logging

class CloseOpenIssue():
    def __init__(self, key):
        self.url = 'https://api.newrelic.com/graphql'
        self.headers = {
            'Content-Type': 'application/json',
            'API-Key': key
        }
        self.vars = {}


    def sendRequest(self, q):
        res = requests.request("POST", self.url, headers=self.headers, json={'query': q, 'variables': self.vars})
        return res


          #       {
          # "data": {
          #   "aiIssuesResolveIssue": {
          #     "error": "internal error while processing the request - routingKey is null",
          #     "result": null
          #   }
          # }


    def closeIssue(self, accountId, issueToClose):
        mutation = f'''
            mutation {{
              aiIssuesResolveIssue(accountId: {accountId}, issueId: "{issueToClose}") {{
                error
                result {{
                  action
                  issueId
                  accountId
                }}
              }}
            }}
        '''
        res = ''

        try:
            resp = self.sendRequest(mutation)
            logging.debug('CloseIssue')
            logging.debug(resp.json())
            parsed = resp.json()
            if (parsed['data']['aiIssuesResolveIssue']['error'] is None):
                res = 'success'
            else:
                res = 'failed'
                logging.error('Failed to close issue. Response: ' + resp['data']['aiIssuesResolveIssue']['error'])
        except Exception as e:
            logging.exception('Exception occurred - Failed to close issue: ' + issueToClose)
            raise

        return(res)
