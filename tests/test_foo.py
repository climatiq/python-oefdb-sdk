import csv
import datetime
import math
import pprint
import typing
from typing import List, Optional

import toml
from pydantic import BaseModel

from oefdb.new.configuration import load_schema_definition


def test_foo():
    schema = load_schema_definition("./tests/schema.toml")

    with open('./tests/input.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        # todo skip header

        headers = next(reader)

        schema.validate_columns(headers)

        for row in reader:
            print(row)
            schema.validate_row(row)
            break
            # print(row['first_name'], row['last_name'])

    raise Exception("sfd")
#     # csv = read_csv("./tests/input.csv")
#
#     for (column_name, column_data) in csv.iteritems():
#         print("Validating:", column_name)
#
#         configuration_for_column = next(x for x in configuration['columns'] if x["name"] == column_name)
#
#         validator_strings = configuration_for_column['validators']
#
#         validators = []
#
#         for validator_string in validator_strings:
#             # print(validator_string)
#             validator = validator_mapping[validator_string]
#
#             validators.append(validator)
#
#
#         print(validators)
#
#         for data_point in column_data:
#             for validator in validators:
#                 if validator(data_point):
#                     pass
#                 else:
#
#                     print(data_point, "did not pass test", type(data_point))
#                     raise Exception("Error validating")
#
#         # print(column_data)
#         # print(configuration_for_column)
#
#     raise Exception("sdfds")

