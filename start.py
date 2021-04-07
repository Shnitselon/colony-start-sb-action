import os
import sys
import argparse
from colony_client import ColonyClient

def parse_user_input():
    parser = argparse.ArgumentParser(prog='Colony Sandbox Start')

    parser.add_argument("blueprint_name", type=str, help="The name of source blueprint")
    parser.add_argument("sandbox_name", type=str, help="The name of sandbox")
    parser.add_argument("duration", type=int, default=120, help="The name of source blueprint")
    parser.add_argument("branch", type=str, help="Run the Blueprint version from a remote Git branch")
    parser.add_argument("inputs", type=str, help="The inputs can be provided as a comma-separated list of key=value pairs")
    parser.add_argument("artifacts", type=str, help="A comma-separated list of artifacts per application")

    return parser.parse_args()

def parse_comma_separated_string(params_string: str = None) -> dict:
    res = {}

    if not params_string:
        return res

    key_values = params_string.split(",")

    for item in key_values:
        parts = item.split("=")
        if len(parts) != 2:
            raise ValueError("Line must be comma-separated list of key=values: key1=val1, key2=val2...")

        key = parts[0].strip()
        val = parts[1].strip()

        res[key] = val

    return res

if __name__ == "__main__":
    args = parse_user_input()

    inputs_dict = parse_comma_separated_string(args.inputs)
    artifacts_dict = parse_comma_separated_string(args.artifacts)

    client = ColonyClient(
        space=os.environ.get("COLONY_SPACE", ""),
        token=os.environ.get("COLONY_TOKEN", "")
    )
    try: 
        sandbox_id = client.start_sandbox(
            args.blueprint_name,
            args.sandbox_name,
            args.duration,
            inputs_dict,
            artifacts_dict
        )
    except Exception as e:
        print(f"::error::Unable to start sandbox. Reason {e}")
        sys.exit(1)
        
    print(f"::set-output name=sandbox_id::{sandbox_id}")
