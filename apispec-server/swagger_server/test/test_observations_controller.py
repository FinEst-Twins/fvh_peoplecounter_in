# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.event_notification_alert import EventNotificationAlert  # noqa: E501
from swagger_server.test import BaseTestCase


class TestObservationsController(BaseTestCase):
    """ObservationsController integration test stubs"""

    def test_peoplecounter_v1_post(self):
        """Test case for peoplecounter_v1_post

        adds count observations to UoP
        """
        EventNotificationAlert = EventNotificationAlert()
        response = self.client.open(
            '/FinEst-Twins/peoplecounter/1.0.0/peoplecounter/v1',
            method='POST',
            data=json.dumps(EventNotificationAlert),
            content_type='application/xml')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
