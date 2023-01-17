import json
from pyshacl import validate

"""
validate scraped json files
if invalid, append error msg to errors
"""


class Validator:

    def __init__(self, json_list):
        self.json_list = [json.dumps(file) for file in json_list]

    def validate_json(self):

        # SHACL file to validate data against
        shacl_file = 'data/defs/court-data-standard-shacl.ttl'

        # collect errors to display on exit
        errors = []

        print("Starting file validation.")

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
                        f"File{self.json_list.index[file]} failed validation.")

                else:
                    print("JSON file validated.")

            except json.JSONDecodeError:
                errors.append(f"{file}\nBad JSON format. Validation aborted.")

        print(*errors, sep="\n") if errors else print("All files successfully validated.")

        return self.json_list
