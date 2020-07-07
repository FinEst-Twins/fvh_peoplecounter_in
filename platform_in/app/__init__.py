from flask import Flask
import os
import sys
from flask import jsonify
from elasticapm.contrib.flask import ElasticAPM
import logging
from flask import jsonify, request
import json
from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer
import xmltodict
import certifi

logging.basicConfig(level=logging.DEBUG)
elastic_apm = ElasticAPM()
# print(app.config, file=sys.stderr)

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

def delivery_report(err, msg):
    if err is not None:
        logging.error(f"Message delivery failed: {err}")
    else:
        logging.debug(f"Message delivered to {msg.topic()} [{msg.partition()}]")



def kafka_avro_produce(avroProducer, topic, data):

    try:
        avroProducer.produce(topic=topic, value=data)
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

def create_app(script_info=None):

    # instantiate the app
    app = Flask(__name__)

    # set config
    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    # set up extensions
    #elastic_apm.init_app(app)

    #from app.resources.observations import observations_blueprint
    #app.register_blueprint(observations_blueprint)
    value_schema = avro.loads(counter_data_schema)
    #value = {"name": "Value"}

    avroProducer = AvroProducer(
        {
            "bootstrap.servers": app.config["KAFKA_BROKERS"],
            "security.protocol": app.config["SECURITY_PROTOCOL"],
            "sasl.mechanism": app.config["SASL_MECHANISM"],
            "sasl.username": app.config["SASL_UNAME"],
            "sasl.password": app.config["SASL_PASSWORD"],
            "ssl.ca.location": certifi.where(),
            "debug": "security,cgrp,fetch,topic,broker,protocol",
            #"on_delivery": delivery_report,
            "schema.registry.url": "https://kafka01.fvh.fi:8081",
        },
        default_value_schema=value_schema,
    )

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {"app": app}
    
    @app.route("/")
    def hello_world():
        return jsonify(hello="world")

    @app.route('/peoplecounter/v1/', methods=['POST'])
    def post_peoplecounter_data():
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
            kafka_avro_produce(avroProducer, topic, data_dict)
            #kafka_produce_peoplecounter_data(topic, json.dumps(data_dict))
            return success_response_object,success_code

        except Exception as e:
            print("error", e)
            elastic_apm.capture_exception()

    return app

