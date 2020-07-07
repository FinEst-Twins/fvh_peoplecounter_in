from flask import jsonify, request, Blueprint, current_app
from flask_restful import Resource, Api, reqparse, abort
from datetime import datetime
import json
import os
import logging
import time
import logging
from confluent_kafka import Producer, avro
from confluent_kafka.avro import AvroProducer
from app import elastic_apm
import xmltodict

observations_blueprint = Blueprint("observations", __name__)
api = Api(observations_blueprint)

success_response_object = {"status":"success"}
success_code = 202
failure_response_object = {"status":"failure"}
failure_code = 400

counter_data_schema = """{
  "name": "MyClass",
  "type": "record",
  "namespace": "fvh.peoplecounter.avro",
  "fields": [
    {
      "name": "EventNotificationAlert",
      "type": {
        "name": "EventNotificationAlert",
        "type": "record",
        "fields": [
          {
            "name": "@version",
            "type": "string"
          },
          {
            "name": "@xmlns",
            "type": "string"
          },
          {
            "name": "ipAddress",
            "type": "string"
          },
          {
            "name": "protocolType",
            "type": "string"
          },
          {
            "name": "macAddress",
            "type": "string"
          },
          {
            "name": "channelID",
            "type": "string"
          },
          {
            "name": "dateTime",
            "type": "int",
            "logicalType": "date"
          },
          {
            "name": "activePostCount",
            "type": "string"
          },
          {
            "name": "eventType",
            "type": "string"
          },
          {
            "name": "eventState",
            "type": "string"
          },
          {
            "name": "eventDescription",
            "type": "string"
          },
          {
            "name": "channelName",
            "type": "string"
          },
          {
            "name": "peopleCounting",
            "type": {
              "name": "peopleCounting",
              "type": "record",
              "fields": [
                {
                  "name": "statisticalMethods",
                  "type": "string"
                },
                {
                  "name": "TimeRange",
                  "type": {
                    "name": "TimeRange",
                    "type": "record",
                    "fields": [
                      {
                        "name": "startTime",
                        "type": "int",
                        "logicalType": "date"
                      },
                      {
                        "name": "endTime",
                        "type": "int",
                        "logicalType": "date"
                      }
                    ]
                  }
                },
                {
                  "name": "enter",
                  "type": "string"
                },
                {
                  "name": "exit",
                  "type": "string"
                },
                {
                  "name": "pass",
                  "type": "string"
                }
              ]
            }
          }
        ]
      }
    }
  ]
}"""

kafka_producer = Producer(
        {
            "bootstrap.servers": current_app.config["KAFKA_BROKERS"],
            "security.protocol": current_app.config["SECURITY_PROTOCOL"],
            "sasl.mechanism": current_app.config["SASL_MECHANISM"],
            "sasl.username": current_app.config["SASL_UNAME"],
            "sasl.password": current_app.config["SASL_PASSWORD"],
            "ssl.ca.location": current_app.config["CA_CERT"],
        }
    )

def delivery_report(err, msg):
    if err is not None:
        logging.error(f"Message delivery failed: {err}")
    else:
        logging.debug(f"Message delivered to {msg.topic()} [{msg.partition()}]")

def kafka_produce_peoplecounter_data(topic, jsonstring):

    try:
        kafka_producer.produce(
                topic, jsonstring, callback=delivery_report
            )
        kafka_producer.poll(2)
    except BufferError:
        logging.error("local buffer full", len(kafka_producer))
        elastic_apm.capture_exception()
        return False
    except Exception as e:
        elastic_apm.capture_exception()
        logging.error(e)
        return False

def kafka_avro_produce(topic, data):

#     value_schema_str = """
#     {
#    "namespace": "my.test",
#    "name": "value",
#    "type": "record",
#    "fields" : [
#      {
#        "name" : "name",
#        "type" : "string"
#      }
#     ]
#     }
#    """

    value_schema = avro.loads(counter_data_schema)
    #value = {"name": "Value"}

    avroProducer = AvroProducer(
        {
            "bootstrap.servers": current_app.config["KAFKA_BROKERS"],
            "security.protocol": current_app.config["SECURITY_PROTOCOL"],
            "sasl.mechanism": current_app.config["SASL_MECHANISM"],
            "sasl.username": current_app.config["SASL_UNAME"],
            "sasl.password": current_app.config["SASL_PASSWORD"],
            "ssl.ca.location": current_app.config["CA_CERT"],
            "on_delivery": delivery_report,
            "schema.registry.url": "https://kafka01.fvh.fi:8081",
        },
        default_value_schema=counter_data_schema,
    )

    try:
        avroProducer.produce(topic="test.sputhan.finest.testnoise", value=data)
        logging.debug("avro produce")
        avroProducer.poll(2)
        if len(avroProducer) != 0:
            return False
    except BufferError:
        logging.error("local buffer full", len(avroProducer))
        return False
    except Exception as e:
        logging.error(e)
        return False

    return True

class PeopleCounterObservation(Resource):
    def post(self):
        """
        Post new observation
        """
        try:
            data = request.get_data() #get_json()
            logging.info(f"post observation: {data}")
            data_dict = xmltodict.parse(data)
            print(json.dumps(data_dict))

            ip = data_dict["EventNotificationAlert"]["ipAddress"]
            channel = data_dict["EventNotificationAlert"]["channelName"].replace(" ", "_")
            topic_prefix = "test.sputhan.finest.peoplecounter"
            topic = f"{topic_prefix}.{ip}.{channel}"
            #print(topic)
            kafka_avro_produce(topic, data_dict)
            #kafka_produce_peoplecounter_data(topic, json.dumps(data_dict))
            return success_response_object,success_code

        except Exception as e:
            print("error", e)
            elastic_apm.capture_exception()
            return failure_response_object,failure_code

api.add_resource(PeopleCounterObservation, "/peoplecounter/v1/")
