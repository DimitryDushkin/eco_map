#!/usr/bin/python2.4
# -*- coding: utf-8 -*-
#
# Copyright (C) 2010 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Simple command-line example for Moderator.

Command-line application that exercises the Google Moderator API.

Usage:
  $ python moderator.py

You can also get help on all the command-line flags the program understands
by running:

  $ python moderator.py --help

To get detailed log output run:

  $ python moderator.py --logging_level=DEBUG
"""

__author__ = 'jcgregorio@google.com (Joe Gregorio)'

import gflags
import httplib2
import logging
import pprint
import sys

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run

FLAGS = gflags.FLAGS

# Set up a Flow object to be used if we need to authenticate. This
# sample uses OAuth 2.0, and we set up the OAuth2WebServerFlow with
# the information it needs to authenticate. Note that it is called
# the Web Server Flow, but it can also handle the flow for native
# applications <http://code.google.com/apis/accounts/docs/OAuth2.html#IA>
# The client_id client_secret are copied from the API Access tab on
# the Google APIs Console <http://code.google.com/apis/console>. When
# creating credentials for this application be sure to choose an Application
# type of "Installed application".
FLOW = OAuth2WebServerFlow(
    client_id='433807057907.apps.googleusercontent.com',
    client_secret='jigtZpMApkRxncxikFpR+SFg',
    scope='https://www.googleapis.com/auth/moderator',
    user_agent='moderator-cmdline-sample/1.0')

# The gflags module makes defining command-line options easy for
# applications. Run this program with the '--help' argument to see
# all the flags that it understands.
gflags.DEFINE_enum('logging_level', 'ERROR',
    ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
    'Set the level of logging detail.')


def main(argv):
  # Let the gflags module process the command-line arguments
  try:
    argv = FLAGS(argv)
  except gflags.FlagsError, e:
    print '%s\\nUsage: %s ARGS\\n%s' % (e, argv[0], FLAGS)
    sys.exit(1)

  # Set the logging according to the command-line flag
  logging.getLogger().setLevel(getattr(logging, FLAGS.logging_level))

  # If the Credentials don't exist or are invalid run through the native client
  # flow. The Storage object will ensure that if successful the good
  # Credentials will get written back to a file.
  storage = Storage('moderator.dat')
  credentials = storage.get()
  if credentials is None or credentials.invalid:
    credentials = run(FLOW, storage)

  # Create an httplib2.Http object to handle our HTTP requests and authorize it
  # with our good Credentials.
  http = httplib2.Http()
  http = credentials.authorize(http)

  service = build("moderator", "v1", http=http)

  try:

    # Create a new Moderator series.
    series_body = {
          "description": "Share and rank tips for eating healthy and cheap!",
          "name": "Eating Healthy & Cheap",
          "videoSubmissionAllowed": False
          }
    series = service.series().insert(body=series_body).execute()
    print "Created a new series"

    # Create a new Moderator topic in that series.
    topic_body = {
          "description": "Share your ideas on eating healthy!",
          "name": "Ideas",
          "presenter": "liz"
          }
    topic = service.topics().insert(seriesId=series['id']['seriesId'],
                              body=topic_body).execute()
    print "Created a new topic"

    # Create a new Submission in that topic.
    submission_body = {
          "attachmentUrl": "http://www.youtube.com/watch?v=1a1wyc5Xxpg",
          "attribution": {
            "displayName": "Bashan",
            "location": "Bainbridge Island, WA"
            },
          "text": "Charlie Ayers @ Google"
          }
    submission = service.submissions().insert(seriesId=topic['id']['seriesId'],
        topicId=topic['id']['topicId'], body=submission_body).execute()
    print "Inserted a new submisson on the topic"

    # Vote on that newly added Submission.
    vote_body = {
          "vote": "PLUS"
          }
    service.votes().insert(seriesId=topic['id']['seriesId'],
                     submissionId=submission['id']['submissionId'],
                     body=vote_body)
    print "Voted on the submission"

  except AccessTokenRefreshError:
    print ("The credentials have been revoked or expired, please re-run"
      "the application to re-authorize")

if __name__ == '__main__':
  main(sys.argv)
