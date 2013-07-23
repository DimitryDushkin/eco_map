# coding: utf-8
#
#import sys
#sys.path.append("./eco_map/lib/fusion-tables-client")
#
#from authorization.oauth import OAuth
#import ftclient
#
#consumer_key = '185198787335-9pm5sgrn5e56jgdd5jkssc2jko2ianmh.apps.googleusercontent.com' #client_id
#consumer_secret = '7IU6L9OVGjSriGt4bBk8BdhF'
#
#url, token, secret = OAuth().generateAuthorizationURL(consumer_key, consumer_secret, consumer_key)
#
##print "Visit this URL in a browser: "
##print url
##raw_input("Hit enter after authorization")
##token, secret = OAuth().authorize(consumer_key, consumer_secret, token, secret)
#
## Здесь используем токен, полученный от "ручного" предоставления доступа к клиентскому
## fusion tables, т.е. используется OAuth 2.0 через client account.
## Конечно, в будущем надо переписать на service account.
#
## Get once saved token and secret of auth. grant
#f = file('token_secret', 'r')
#token_secret = f.read()
#f.close()
#[token, secret] = token_secret.split(' ')
## Get access tokem
#oauth_client = ftclient.OAuthFTClient(consumer_key, consumer_secret, token, secret)
#
## Make quieries
#results = oauth_client.query('SELECT * FROM 1gvB3SedL89vG5r1128nUN5ICyyw7Wio5g1w1mbk')
#print results
#print(oauth_client.query('INSERT INTO 1gvB3SedL89vG5r1128nUN5ICyyw7Wio5g1w1mbk ' +
#                         '(Title, Location, Paper, Metall, Glass, Cloth, Danger, Plactic, Other) ' +
#                         'VALUES ' +
#                         '(\'test\', \'Москва, Петровка, 38\', 1, 1, 1, 1, 1, 1, 1)'))
#print(oauth_client.query('SELECT * FROM 1gvB3SedL89vG5r1128nUN5ICyyw7Wio5g1w1mbk'))


import sys
import os
import logging

sys.path.append(os.path.abspath("../eco_map/lib/google-api-python-client"))


import httplib2
from apiclient.discovery import build
from oauth2client.client import SignedJwtAssertionCredentials
from oauth2client.file import Storage

print sys.path

logging.getLogger().setLevel(logging.INFO)


f = file('d7509b5300823ddbc6a9d3a709a6804bf912d355-privatekey.p12', 'rb')
key = f.read()
f.close()

credentials = SignedJwtAssertionCredentials(
    '185198787335-vup5osvu3bgni0k20gdajlp3ofmb2dno@developer.gserviceaccount.com',
    key,
    scope='https://www.googleapis.com/auth/fusiontables')
storage = Storage('fusion.dat')
credentials.set_store(storage)

http = httplib2.Http()
http = credentials.authorize(http)


service = build("fusiontables", "v1", http=http)
response = service.query().sqlGet(sql='SELECT Location FROM 1gvB3SedL89vG5r1128nUN5ICyyw7Wio5g1w1mbk LIMIT 10').execute(http)
for row in response['rows']:
    print unicode(row[0]).encode('utf-8')
