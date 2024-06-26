import unittest
from src.module_1.module_1_meteo_api import process_data, validate_response_schema


class TestValidateResponseSchema(unittest.TestCase):
    def test_validate_response_schema_success(self):
        data = {
            "daily": {
                "time": ["2021-01-01", "2021-01-02"],
                "temperature_2m_mean": [10, 20],
                "precipitation_sum": [5, 10],
                "soil_moisture_0_to_10cm_mean": [0.5, 0.6],
            }
        }
        validate_response_schema(data)

    def test_validate_response_schema_failure(self):
        data = {"daily": {}}
        with self.assertRaises(Exception):
            validate_response_schema(data)

    def test_validate_response_schema_missing_daily(self):
        data = {}
        with self.assertRaises(Exception):
            validate_response_schema(data)

    def test_validate_response_schema_missing_time(self):
        data = {"daily": {"temperature_2m_mean": [10, 20]}}
        with self.assertRaises(Exception):
            validate_response_schema(data)

    def test_validate_response_schema_missing_variable(self):
        data = {"daily": {"time": ["2021-01-01", "2021-01-02"]}}
        with self.assertRaises(Exception):
            validate_response_schema(data)


class TestProcessData(unittest.TestCase):
    def test_process_data(self):
        data = {
            "time": ["2021-01-01", "2021-01-02"],
            "temperature_2m_mean": [10, 20],
            "precipitation_sum": [5, 10],
            "soil_moisture_0_to_10cm_mean": [0.5, 0.6],
        }
        processed_data = process_data(data)

        self.assertIsInstance(processed_data, dict)
        self.assertIn("temperature_2m_mean", processed_data)
        self.assertIn("precipitation_sum", processed_data)
        self.assertIn("soil_moisture_0_to_10cm_mean", processed_data)

        temperature_df = processed_data["temperature_2m_mean"]
        self.assertTrue(not temperature_df.empty)
        self.assertEqual(list(temperature_df["mean"]), [10, 20])
        self.assertEqual(list(temperature_df["std_deviation"]), [0, 0])

        precipitation_df = processed_data["precipitation_sum"]
        self.assertTrue(not precipitation_df.empty)
        self.assertEqual(list(precipitation_df["mean"]), [5, 10])
        self.assertEqual(list(precipitation_df["std_deviation"]), [0, 0])

        soil_moisture_df = processed_data["soil_moisture_0_to_10cm_mean"]
        self.assertTrue(not soil_moisture_df.empty)
        self.assertEqual(list(soil_moisture_df["mean"]), [0.5, 0.6])
        self.assertEqual(list(soil_moisture_df["std_deviation"]), [0, 0])


class TestValidateResponseSchemaEdgeCases(unittest.TestCase):
    def test_incorrect_data_types(self):
        data = {
            "daily": {
                "time": [20210101, 20210102],
                "temperature_2m_mean": ["10", "20"],
                "precipitation_sum": [None, 10],
            }
        }
        with self.assertRaises(Exception):
            validate_response_schema(data)


class TestProcessDataEdgeCases(unittest.TestCase):
    def test_missing_data(self):
        data = {}
        processed_data = process_data(data)
        self.assertIsNone(processed_data)

    def test_empty_lists(self):
        data = {
            "time": [],
            "temperature_2m_mean": [],
            "precipitation_sum": [],
        }
        processed_data = process_data(data)
        self.assertTrue(all(df.empty for df in processed_data.values()))
