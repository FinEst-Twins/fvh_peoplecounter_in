from flask import jsonify, request, Blueprint, current_app
from flask_restful import Resource, Api, reqparse, abort
from datetime import datetime
import json
import os
from rq import Queue, Connection
import logging
import time
import logging
from confluent_kafka import Producer, avro
from confluent_kafka.avro import AvroProducer


observations_blueprint = Blueprint("observations", __name__)
api = Api(observations_blueprint)

def get_kafka_producer():
    return Producer(
        {
            "bootstrap.servers": current_app.config["KAFKA_BROKERS"],
            "security.protocol": current_app.config["SECURITY_PROTOCOL"],
            "sasl.mechanism": current_app.config["SASL_MECHANISM"],
            "sasl.username": current_app.config["SASL_UNAME"],
            "sasl.password": current_app.config["SASL_PASSWORD"],
            "ssl.ca.location": current_app.config["CA_CERT"],
        }
    )

class PeopleCounterObservation(Resource):
    def post(self):
        """
        Post new observation
        """
        data = request.get_json()
        logging.info(f"post observation: {data}")
        print(data)
        
        #kafka_producer = get_kafka_producer()

    #     try:

    #         #kafka_producer.produce(
    #         #    f"{topic_prefix}.{topic}", json.dumps(observations), callback=delivery_report
    #         #)
    #         #kafka_producer.poll(2)
    # except BufferError:
    #     logging.error("local buffer full", len(kafka_producer))
    #     elastic_apm.capture_exception()
    #     return False
    # except Exception as e:
    #     elastic_apm.capture_exception()
    #     logging.error(e)
    #     return False
    
    # return True
        response_object = {"status": "received"}
        return response_object, 200


api.add_resource(PeopleCounterObservation, "/peoplecounter/v1")


class TaskStatus(Resource):
    def get(self, task_id):
        with Connection(redis.from_url(current_app.config["REDIS_URL"])):
            q = Queue()
            task = q.fetch_job(task_id)
        if task:
            response_object = {
                "status": "success",
                "message": {
                    "task_id": task.get_id(),
                    "task_status": task.get_status(),
                    "task_result": task.result,
                },
            }
        else:
            response_object = {"status": "error"}
        return jsonify(response_object)


api.add_resource(TaskStatus, "/taskstatus/<task_id>")

