import json
from pyshacl import validate
import glob

"""
validate scraped json files
if invalid, append error msg to errors
"""


class Validator:

    def __init__(self):
        self.json_list = glob.glob("data/json/scraped/*.json")
        self.valid_json = []

    def validate_json(self):

        # SHACL file to validate data against
        # Will be replaced with remote resource in future versions
        shacl_file = 'data/defs/court-data-standard-shacl.ttl'

        # collect errors to display on exit
        errors = []

        if len(self.json_list) < 1:
            print("Validator found no JSON-LD data. Exiting.")
            raise SystemExit

        print(f"Starting file validation with {len(self.json_list)} files.")

        for file in self.json_list:
            try:
                r = validate(
                    file,
                    data_graph_format='json-ld',
                    shacl_graph=shacl_file,
                    inference='none',
                    abort_on_first=True,
                    allow_infos=False,
                    allow_warnings=False,
                    meta_shacl=False,
                    advanced=True,
                    js=False,
                    debug=False)

                # if error, append msg to errors list
                if r[0] != True:
                    msg = r[2]
                    errors.append(f"{file}\n{msg}\n")
                    print(
                        f"{file} failed validation. Removing from file list.")
                    self.json_list.remove(file)

                else:
                    self.valid_json.append(json.load(open(file)))
                    print(f"{file} validated.")

            except json.JSONDecodeError:
                errors.append(f"{file}\nBad JSON format. Validation aborted.")

        print(*errors, sep="\n") if errors else print("All files successfully validated.")

        return self.valid_json
