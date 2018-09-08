#! /usr/bin/env python3.7
# -*- coding: utf-8 -*-

"""Request handler for custom web tracker

Runs on AppEngine. Receives messages from javascript client,
authenticates with pub/sub to pass messages on.

Setup services on GCP and configure all {variables below}

See git for further details

author: Nick Koronka
email: nick.koronka@gmail.com
"""


# [START gae_python37_app]
import os

from flask import Flask
from flask import request
from google.cloud import pubsub_v1



project_dir = os.path.dirname(os.path.realpath(__file__))
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = project_dir+'/{service-account-private-key}.json'
PROJECT_ID = "{gcp-project-id}"
TOPIC_NAME = "{pub-sub-topic-name}"


def publish_messages(project, topic_name, message):
    """Publishes multiple messages to a Pub/Sub topic."""
    # [START pubsub_quickstart_publisher]
    # [START pubsub_publish]

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project, topic_name)
    message = message.encode('utf-8')

    def callback(message_future):
        if message_future.exception():
            print('Publishing message on {} threw an Exception {}.'.format(
                topic_name, message_future.exception()))
        else:
            print(message_future.result())

    message_future = publisher.publish(topic_path, data=message)
    message_future.add_done_callback(callback)
    # [END pubsub_quickstart_publisher]
    # [END pubsub_publish]

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)


@app.route('/')
def track():
    url = request.url
    publish_messages(PROJECT_ID, TOPIC_NAME, url)
    return "process-complete"


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=5000, debug=True)
# [END gae_python37_app]