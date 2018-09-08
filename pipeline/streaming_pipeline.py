#! /usr/bin/env python2.6
# -*- coding: utf-8 -*-

"""Request handler for custom web tracker
Setup services on GCP and configure all {variables below}

See git for further details [https://github.com/nkoronka/custom-web-tracking-with-apache-beam](https://github.com/nkoronka/custom-web-tracking-with-apache-beam)

"""


from __future__ import absolute_import
from datetime import datetime
import json
import logging
import os
import urllib

import apache_beam as beam
from apache_beam.io import ReadFromText
from apache_beam.io import WriteToText
from apache_beam.io import WriteToBigQuery
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions


# obtain reference to pwd
project_dir = os.path.dirname(os.path.realpath(__file__))
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = project_dir+'/{service-account-credentials}.json'


class SplitUrl(beam.DoFn):
    """Define transformation subclass"""
    def process(self, element):
        element = urllib.unquote(element)
        print element
        splits = element.split('?')
        blank_string = ""

        request_url = blank_string.join(splits[0:1])
        request_querystring = blank_string.join(splits[1:])
        query_params = request_querystring.split('&')

        params = {}

        for param in query_params:
            key = param.split('=')[0]
            value = param.split('=')[1]
            params[key] = value

        params['t'] = datetime.utcfromtimestamp(float(params['t']) / 1000).strftime('%Y-%m-%d %H:%M:%S.%f UTC')

        return [{
            'request_url': request_url,
            'request_querystring': request_querystring,
            'id': params['id'],
            'cid': params['cid'],
            'eventType': params['eventType'],
            'timestamp': params['t'],
            'hostname': params['hostname'],
            'url': params['url'],
            'path': params['path'],
            'firstVisitStartTime': params['fvst'],
            'visitId': params['vst']
        }]



if __name__ == '__main__':

    logging.getLogger().setLevel(logging.INFO)

    topic = 'projects/{project-id}/topics/{topic-ref}'

    # if running on vm you use nohup e.g "nohup python web-tracker.py &" - keeps process alive when you close terminal


    pipeline_args = [
        '--runner=DirectRunner', #'--runner=DirectRunner', '--runner=DataflowRunner' - change to dataflow runner to use GCP autoscaling solution - make sure you shut down after testing to avoid costs
        '--project={project-id}',
        '--staging_location=gs://{staging-cloud-storage-bucket}/staging',
        '--temp_location=gs://{staging-cloud-storage-bucket}/temp_storage',
        '--job_name=web-tracker',
        '--streaming'
    ]

    pipeline_options = PipelineOptions(pipeline_args)

    with beam.Pipeline(options=pipeline_options) as p:
        lines = p | beam.io.ReadStringsFromPubSub(topic=topic) #ReadFromText(input)

        output = (
            lines | 'Split' >> beam.ParDo(SplitUrl()))  # apply transformations
            output | beam.io.WriteToBigQuery(table='{bigquery-table-id}',dataset='{bigquery-dataset-id}',project='{project-id}') # send to BigQuery
