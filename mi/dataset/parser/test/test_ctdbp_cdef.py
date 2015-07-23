#!/usr/bin/env python

"""
@package mi.dataset.parser.test
@file mi-dataset/mi/dataset/parser/test/test_ctdbp_cdef.py
@author Jeff Roy
@brief Test code for ctdbp_cdef data parser

Files used for testing:

data1.log
  Contains Header + 100 Sensor records

invalid_data.log
  Contains 7 lines of invalid data

no_sensor_data.log
  Contains a header section and no sensor records

"""


import os
from nose.plugins.attrib import attr

from mi.idk.config import Config

from mi.core.log import get_logger
log = get_logger()

from mi.dataset.test.test_parser import ParserUnitTestCase
from mi.dataset.parser.ctdbp_cdef import CtdbpCdefParser

RESOURCE_PATH = os.path.join(Config().base_dir(), 'mi',
                             'dataset', 'driver', 'ctdbp_cdef', 'resource')

MODULE_NAME = 'mi.dataset.parser.ctdbp_cdef'


@attr('UNIT', group='mi')
class CtdbpCdefParserUnitTestCase(ParserUnitTestCase):
    """
    ctdbp_cdef Parser unit test suite
    """

    def test_simple(self):
        """
        Simple test to verify that records are successfully read and parsed from a data file
        """
        log.debug('===== START SIMPLE TEST =====')

        path = RESOURCE_PATH
        log.info(path)

        # test with Endurance data
        with open(os.path.join(RESOURCE_PATH, 'simple_test_endurance.log'), 'rU') as file_handle:

            parser = CtdbpCdefParser(file_handle,
                                     self.exception_callback)

            # In a single read, get all particles in this file.
            number_expected_results = 5
            result = parser.get_records(number_expected_results)
            self.assertEqual(len(result), number_expected_results)

            self.assertListEqual(self.exception_callback_value, [])

        # test with Pioneer data
        with open(os.path.join(RESOURCE_PATH, 'simple_test_pioneer.log'), 'rU') as file_handle:

            parser = CtdbpCdefParser(file_handle,
                                     self.exception_callback)

            # In a single read, get all particles in this file.
            number_expected_results = 5
            result = parser.get_records(number_expected_results)
            self.assertEqual(len(result), number_expected_results)

            self.assertListEqual(self.exception_callback_value, [])

        log.debug('===== END SIMPLE TEST =====')

    def test_verify_record_against_yaml(self):
        """
        Read data from a file and pull out data particles
        one at a time. Verify that the results are those we expected.
        """
        log.debug('===== START YAML TEST =====')

        # test with Endurance data
        with open(os.path.join(RESOURCE_PATH, 'data1_endurance.log'), 'rU') as file_handle:

            parser = CtdbpCdefParser(file_handle,
                                     self.exception_callback)

            # In a single read, get all particles in this file.
            number_expected_results = 143
            result = parser.get_records(number_expected_results)
            self.assert_particles(result, 'data1_endurance.yml', RESOURCE_PATH)

            self.assertListEqual(self.exception_callback_value, [])

        # test with Pioneer data
        with open(os.path.join(RESOURCE_PATH, 'data1_pioneer.log'), 'rU') as file_handle:

            parser = CtdbpCdefParser(file_handle,
                                     self.exception_callback)

            # In a single read, get all particles in this file.
            number_expected_results = 100
            result = parser.get_records(number_expected_results)
            self.assert_particles(result, 'data1_pioneer.yml', RESOURCE_PATH)

            self.assertListEqual(self.exception_callback_value, [])

        log.debug('===== END YAML TEST =====')

    def test_invalid_sensor_data_records(self):
        """
        Read data from a file containing invalid sensor data records.
        Verify that no instrument particles are produced
        and the correct number of exceptions are detected.
        """
        log.debug('===== START TEST INVALID SENSOR DATA =====')

        # test with Endurance data
        with open(os.path.join(RESOURCE_PATH, 'invalid_data_endurance.log'), 'rU') as file_handle:
            parser = CtdbpCdefParser(file_handle,
                                     self.exception_callback)

            # Try to get records and verify that none are returned.
            result = parser.get_records(1)
            self.assertEqual(result, [])
            self.assertEqual(len(self.exception_callback_value), 11)

        self.exception_callback_value = []  # reset exceptions

        # test with Pioneer data
        with open(os.path.join(RESOURCE_PATH, 'invalid_data_pioneer.log'), 'rU') as file_handle:
            parser = CtdbpCdefParser(file_handle,
                                     self.exception_callback)

            # Try to get records and verify that none are returned.
            result = parser.get_records(1)
            self.assertEqual(result, [])
            self.assertEqual(len(self.exception_callback_value), 11)

        log.debug('===== END TEST INVALID SENSOR DATA =====')

    def test_no_sensor_data(self):
        """
        Read a file containing no sensor data records
        and verify that no particles are produced.
        """
        log.debug('===== START TEST NO SENSOR DATA RECOVERED =====')

        # test with Endurance data
        with open(os.path.join(RESOURCE_PATH, 'no_sensor_data_endurance.log'), 'rU') as file_handle:
            parser = CtdbpCdefParser(file_handle,
                                     self.exception_callback)

            # Try to get a record and verify that none are produced.
            result = parser.get_records(1)
            self.assertEqual(result, [])

            self.assertListEqual(self.exception_callback_value, [])

        # test with Pioneer data
        with open(os.path.join(RESOURCE_PATH, 'no_sensor_data_pioneer.log'), 'rU') as file_handle:
            parser = CtdbpCdefParser(file_handle,
                                     self.exception_callback)

            # Try to get a record and verify that none are produced.
            result = parser.get_records(1)
            self.assertEqual(result, [])

            self.assertListEqual(self.exception_callback_value, [])

        log.debug('===== END TEST NO SENSOR DATA =====')
