# Summary

This project is a working prototype for a scalable tracking system landing data into BigQuery with full control over the data model and no payload or hit count limitations.<br/><br/>

For further information see [slide deck](https://docs.google.com/presentation/d/1CNwJ5Xg8dDTsVH6_CyLoAly3bjMKO6iuATM2QhaOqxc/).<br/>


# Configuring and running

## High Level View of Tracking Solution

![High Level View of Tracking Solution](https://github.com/nkoronka/custom-web-tracking-with-apache-beam/blob/master/high-level-solution.png?raw=true)<br/>

## Setup Steps

### GCP Authentication
Create service account with following permissions:<br/>
<br/>
BigQuery Data Editor<br/>
Pub/Sub Publisher<br/>

Create private key for service account in json format. Include in same directory as apache beam code. Amend reference to point to file.<br/>

### Pub/Sub
Create a topic on GCP and amend references in request_handler and pipeline components<br/>

Further info: [https://cloud.google.com/pubsub/docs/](https://cloud.google.com/pubsub/docs/)

### Creating BigQuery Table

Create table named beamed_hits in US region with following schema:<br/>

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

Add dataset and table id references in pipeline code<br/>


### Hosting App Engine

Environment: AppEngine standard python3.7<br/>
<br/>
Debug: $ python3 main.py<br/>
Deploy: gcloud app deploy<br/>
Further info see: [https://cloud.google.com/appengine/docs/standard/python3/](https://cloud.google.com/appengine/docs/standard/python3/)<br/>

requirements.txt:<br/>
  Flask==1.0.2<br/>
  google-api-python-client==1.6.4<br/>


### Apache Beam

Install Instructions:<br/>
[https://beam.apache.org/get-started/quickstart-py/](https://beam.apache.org/get-started/quickstart-py/)<br/>
[https://stackoverflow.com/questions/49047778/airflow-installation-failure-beamgcp](https://stackoverflow.com/questions/49047778/airflow-installation-failure-beamgcp)<br/>

Environment: python 2.6 - use virtual environment exactly as stated in install instructions (see above)<br/>


### Adding Tracking

1. Host tracker.js code in S3 or similar and amend reference in tag<br/>
2. Must be publicly available<br/>
3. Congfigure GA using GTM<br/>
4. Add separate custom HTML tag in GTM for every separate event you want to track<br/>
5. Ensure tags are published to live GTM container<br/>
6. Test in browser console network tab to ensure connections are successfully made to App Engine<br/>


## Running The Pipeline

1. Host request handler on App Engine<br/>
2. Create pipeline either on DataFlow, local/VM environment<br/>
3. Add tracking code<br/>


### Different Deployment Types

1. Local<br/>
  Define runner in pipeline_args to be DirectRunner<br/>
  $ python streaming_pipeline.py<br/>

2. Virtual Machine<br/>
  Define runner in pipeline_args to be DirectRunner<br/>
  $ nohup python web-tracker.py &<br/>
  nohup ensures that process remains alive when terminal is closed down<br/>
  Alternatively create a daemon<br/>

3. Google Cloud Dataflow<br/>
  Define runner in pipeline_args to be DataflowRunner<br/>
  $ python streaming_pipeline.py<br/>
  Await setup of DataFlow job<br/>
  You can see your job progress here: [https://console.cloud.google.com/dataflow?project={job-id}](https://console.cloud.google.com/dataflow?project={job-id})<br/>
