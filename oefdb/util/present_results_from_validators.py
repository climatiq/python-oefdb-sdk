from __future__ import annotations

from oefdb.validate import results_from_validators_type


def present_results_from_validators(
    validation_result: bool, results_from_validators: results_from_validators_type
) -> None:
    for validator_name, validator_results in results_from_validators.items():
        validation_result, validation_messages = validator_results
        for validation_message in validation_messages:
            print(f"{validator_name}: {validation_message}")  # noqa: T001,T201
