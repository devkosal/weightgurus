#!/usr/bin/env python3
from cmath import nan
from datetime import datetime, timedelta
import json
import os

from dotenv import load_dotenv
import requests

load_dotenv()


def transform_weight(weight):
    """
    Transforms normal weight in pounds to Weight Gurus format

    :param weight: Weight in pounds
    :return: Weight Guru format
    """
    try:
        weight = str(weight).replace('.', '')
        transformed_weight = int(weight)
        return transformed_weight
    except ValueError:
        try:
            transformed_weight = int(float(weight))
            return transformed_weight
        except ValueError:
            print(f"Caught ValueError! '{weight}' is not a number.")


LOGIN_TIMEOUT_S = 3600  # 1 hour


class WeightGurus:

    def __init__(self, username, password):
        self.username = username
        self.login_data = {
            'email': self.username,
            'password': password,
            'web': True
        }
        self.start_date = 'start=1970-01-01T01:00:00.504Z'
        self.weight_history = None
        self.add_weight = {}
        self._headers = None
        self.last_login_at = datetime.now()

    @property
    def headers(self):
        if self._headers is None or (datetime.now() - self.last_login_at).seconds > LOGIN_TIMEOUT_S:
            self.__do_login()
        return self._headers

    def __do_login(self):
        req = requests.post('https://api.weightgurus.com/v3/account/login', data=self.login_data)
        try:
            json_data = req.json()
            self._headers = {'authorization': f"Bearer {json_data['accessToken']}"}
        except Exception as e:
            print(f"Caught Exception reading JSON while logging in: {e}")
            raise e

    def __get_weight_history(self, start_date=None):
        if start_date:
            self.start_date = f"start={start_date}"
        req = requests.get(f'https://api.weightgurus.com/v3/operation/?{self.start_date}', headers=self.headers)
        try:
            json_data = req.json()
        except Exception as e:
            print(f"Caught Exception reading JSON: {e}")
            json_data = None
        return json_data

    def get_all(self):
        return self.__get_weight_history()

    def get_since_date(self, start_date):
        return self.__get_weight_history(start_date)

    def get_latest(self, start_date: str | None = None, daily_lookback_days: int | None = None):
        if daily_lookback_days:
            if start_date:
                print("Warning: start_date will be ignored when `daily_lookback_days` is provided.")
            today = datetime.now().date()
            lookback_day = 0
            while lookback_day < daily_lookback_days:
                weight_data = self.__get_weight_history(start_date=(today - timedelta(days=lookback_day)).isoformat())
                if weight_data['operations']:
                    return weight_data['operations'][-1]
                lookback_day += 1
            print(f"No weight data found in the last {daily_lookback_days} days for {self.username}!")
        weight_data = self.__get_weight_history(start_date=start_date)
        return weight_data['operations'][-1]

    def get_unremoved_entries(self):
        operations = self.__get_weight_history()["operations"]
        operations = self._clean_operations(operations)
        return operations

    @staticmethod
    def _clean_operations(operations: list):
        operations = WeightGurus._remove_deleted_operations(operations)
        return operations

    @staticmethod
    def _remove_deleted_operations(operations):
        for index, operation in enumerate(operations):
            if operation["operationType"] == "delete":
                deleted_operation = operations.pop(index)
                operations = WeightGurus._remove_operation_deleted(
                    operations, deleted_operation
                )

        return operations

    @staticmethod
    def _remove_operation_deleted(operations, deleted_operation):
        for index, current_operation in enumerate(operations):
            if WeightGurus._is_deleted_operation(current_operation, deleted_operation):
                operations.pop(index)

        return operations

    @staticmethod
    def _is_deleted_operation(current_operation, deleted_operation):
        if (
            WeightGurus._is_operation_earlier(current_operation, deleted_operation)
            and current_operation["weight"] == deleted_operation["weight"]
        ):
            return True

        return False

    @staticmethod
    def _is_operation_earlier(current_operation, deleted_operation):
        current_date = datetime.fromisoformat(
            current_operation["serverTimestamp"].replace("Z", "+00:00")
        )
        deleted_date = datetime.fromisoformat(
            deleted_operation["serverTimestamp"].replace("Z", "+00:00")
        )
        return current_date < deleted_date

    @staticmethod
    def _wg_num_to_float(number):
        number = str(number)
        if len(number) <= 1:
            raise Exception("Unsure of how weight guru handles numbers this small")

        try:
            whole_number = int(number[:-1])
        except ValueError:
            return nan

        try:
            decimal_point = int(number[-1]) / 10
        except ValueError:
            return nan

        return whole_number + decimal_point

    def manual_entry(self, weight, bmi=None, body_fat=None, muscle_mass=None, water=None):
        """
        Weight Gurus has a weird way of adding weight, they want integer values (numbers) without decimals.
        This requires you to take you weight and remove the decimal. So, 100.0 pounds would be 1000 when you add it.
        """
        self.__do_login()
        self._headers['user-agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, ' \
                                     'like Gecko) Chrome/89.0.4389.128 Safari/537.36'
        self._headers['content-type'] = 'application/json'
        if bmi:
            self.add_weight['bmi'] = int(bmi)
        if body_fat:
            self.add_weight['bodyFat'] = int(body_fat)
        self.add_weight['entryTimestamp'] = str(datetime.now())
        if muscle_mass:
            self.add_weight['muscleMass'] = int(muscle_mass)
        self.add_weight['operationType'] = 'create'
        self.add_weight['source'] = 'manual'
        if water:
            self.add_weight['water'] = int(water)
        if weight is None:
            print("You need to provide your weight")
            exit(1)
            return False
        weight = transform_weight(weight)
        self.add_weight['weight'] = weight
        req = requests.post('https://api.weightgurus.com/v3/operation',
                            data=json.dumps(self.add_weight),
                            headers=self.headers)
        status_code = req.status_code
        if status_code == 201:
            print("Successfully added weight!")
            return req.json()


if __name__ == "__main__":
    weight_gurus = WeightGurus(os.environ['USERNAME'], os.environ['PASSWORD'])
    print(weight_gurus.get_all())
