# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class PeopleCounting(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, statistical_methods: str=None, time_range: TimeRange=None, enter: int=None, exit: int=None, _pass: int=None):  # noqa: E501
        """PeopleCounting - a model defined in Swagger

        :param statistical_methods: The statistical_methods of this PeopleCounting.  # noqa: E501
        :type statistical_methods: str
        :param time_range: The time_range of this PeopleCounting.  # noqa: E501
        :type time_range: TimeRange
        :param enter: The enter of this PeopleCounting.  # noqa: E501
        :type enter: int
        :param exit: The exit of this PeopleCounting.  # noqa: E501
        :type exit: int
        :param _pass: The _pass of this PeopleCounting.  # noqa: E501
        :type _pass: int
        """
        self.swagger_types = {
            'statistical_methods': str,
            'time_range': TimeRange,
            'enter': int,
            'exit': int,
            '_pass': int
        }

        self.attribute_map = {
            'statistical_methods': 'statisticalMethods',
            'time_range': 'TimeRange',
            'enter': 'enter',
            'exit': 'exit',
            '_pass': 'pass'
        }

        self._statistical_methods = statistical_methods
        self._time_range = time_range
        self._enter = enter
        self._exit = exit
        self.__pass = _pass

    @classmethod
    def from_dict(cls, dikt) -> 'PeopleCounting':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The PeopleCounting of this PeopleCounting.  # noqa: E501
        :rtype: PeopleCounting
        """
        return util.deserialize_model(dikt, cls)

    @property
    def statistical_methods(self) -> str:
        """Gets the statistical_methods of this PeopleCounting.


        :return: The statistical_methods of this PeopleCounting.
        :rtype: str
        """
        return self._statistical_methods

    @statistical_methods.setter
    def statistical_methods(self, statistical_methods: str):
        """Sets the statistical_methods of this PeopleCounting.


        :param statistical_methods: The statistical_methods of this PeopleCounting.
        :type statistical_methods: str
        """
        if statistical_methods is None:
            raise ValueError("Invalid value for `statistical_methods`, must not be `None`")  # noqa: E501

        self._statistical_methods = statistical_methods

    @property
    def time_range(self) -> TimeRange:
        """Gets the time_range of this PeopleCounting.


        :return: The time_range of this PeopleCounting.
        :rtype: TimeRange
        """
        return self._time_range

    @time_range.setter
    def time_range(self, time_range: TimeRange):
        """Sets the time_range of this PeopleCounting.


        :param time_range: The time_range of this PeopleCounting.
        :type time_range: TimeRange
        """

        self._time_range = time_range

    @property
    def enter(self) -> int:
        """Gets the enter of this PeopleCounting.


        :return: The enter of this PeopleCounting.
        :rtype: int
        """
        return self._enter

    @enter.setter
    def enter(self, enter: int):
        """Sets the enter of this PeopleCounting.


        :param enter: The enter of this PeopleCounting.
        :type enter: int
        """
        if enter is None:
            raise ValueError("Invalid value for `enter`, must not be `None`")  # noqa: E501

        self._enter = enter

    @property
    def exit(self) -> int:
        """Gets the exit of this PeopleCounting.


        :return: The exit of this PeopleCounting.
        :rtype: int
        """
        return self._exit

    @exit.setter
    def exit(self, exit: int):
        """Sets the exit of this PeopleCounting.


        :param exit: The exit of this PeopleCounting.
        :type exit: int
        """
        if exit is None:
            raise ValueError("Invalid value for `exit`, must not be `None`")  # noqa: E501

        self._exit = exit

    @property
    def _pass(self) -> int:
        """Gets the _pass of this PeopleCounting.


        :return: The _pass of this PeopleCounting.
        :rtype: int
        """
        return self.__pass

    @_pass.setter
    def _pass(self, _pass: int):
        """Sets the _pass of this PeopleCounting.


        :param _pass: The _pass of this PeopleCounting.
        :type _pass: int
        """
        if _pass is None:
            raise ValueError("Invalid value for `_pass`, must not be `None`")  # noqa: E501

        self.__pass = _pass