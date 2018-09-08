# Configuring and running

## High Level View of Tracking Solution

![High Level View of Tracking Solution](https://github.com/nkoronka/custom-web-tracking-with-apache-beam/blob/master/high-level-solution.png?raw=true)

## Setup Steps

### GCP Authentication
Create service account with following permissions:

BigQuery Data Editor
Pub/Sub Publisher

Create private key for service account in json format. Include in same directory as apache beam code. Amend reference to point to file.

### Pub/Sub
Create a topic on GCP and amend references in request_handler and pipeline components

Further info: [https://cloud.google.com/pubsub/docs/](https://cloud.google.com/pubsub/docs/)

### Creating BigQuery Table

Create table named beamed_hits in US region with following schema:

  id - STRING<br/>
  cid - STRING<br/>
  eventType - STRING<br/>
  timestamp - TIMESTAMP<br/>
  visitId - STRING<br/>
  hostname - STRING<br/>
  url - STRING<br/>
  path - STRING<br/>
  request_url - STRING<br/>
  request_querystring - STRING<br/>
  firstVisitStartTime - STRING<br/>

Add dataset and table id references in pipeline code


### Hosting App Engine

Environment: AppEngine standard python3.7
Debug: $ python3 main.py
Deploy: gcloud app deploy
Further info see: [https://cloud.google.com/appengine/docs/standard/python3/](https://cloud.google.com/appengine/docs/standard/python3/)

requirements.txt:
  Flask==1.0.2
  google-api-python-client==1.6.4


### Apache Beam

Install Instructions:
[https://beam.apache.org/get-started/quickstart-py/](https://beam.apache.org/get-started/quickstart-py/)
[https://stackoverflow.com/questions/49047778/airflow-installation-failure-beamgcp](https://stackoverflow.com/questions/49047778/airflow-installation-failure-beamgcp)

Environment: python 2.6 - use virtual environment exacrtly as stated in install instructions (see above)


### Adding Tracking

Host tracker.js code in S3 or similar and amend reference in tag
Must be publicly available
Congfigure GA using GTM
Add separate custom HTML tag in GTM for every separate event you want to track
Ensure tags are published to live GTM container
Test in browser console network tab to ensure connections are successfully made to App Engine


## Running The Pipeline

1. Host request handler on App Engine
2. Create pipeline either on DataFlow, local/VM environment
3. Add tracking code


### Different Deployment Types

1. Local
  Define runner in pipeline_args to be DirectRunner
  $ python streaming_pipeline.py

2. Virtual Machine
  Define runner in pipeline_args to be DirectRunner
  $ nohup python web-tracker.py &
  nohup ensures that process remains alive when terminal is closed down
  Alternatively create a daemon

3. Google Cloud Dataflow
  Define runner in pipeline_args to be DataflowRunner
  $ python streaming_pipeline.py
  Await setup of DataFlow job
  You can see your job progress here: [https://console.cloud.google.com/dataflow?project={job-id}](https://console.cloud.google.com/dataflow?project={job-id})
