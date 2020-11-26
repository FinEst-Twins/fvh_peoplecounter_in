import connexion
import six

from swagger_server.models.event_notification_alert import EventNotificationAlert  # noqa: E501
from swagger_server import util


def add_inventory(EventNotificationAlert=None):  # noqa: E501
    """adds noise observations to UoP

    Adds an item to the system # noqa: E501

    :param EventNotificationAlert: Observations from Sensors
    :type EventNotificationAlert: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        EventNotificationAlert = EventNotificationAlert.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
