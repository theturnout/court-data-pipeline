import glob
import json
import os
from pyshacl import validate


def validator():
    """
    validate scraped json files
    if valid, move to valid_json folder
    if not, append error msg to errors
    """

    # scraped JSON-LD files
    scraped_json_files = glob.glob("data/raw_json/*.json")

    if len(scraped_json_files) == 0:
        print("No files provided to validator script. Exiting script.")
        return

    # SHACL file to validate data against
    shacl_file = 'data/defs/court-data-standard-shacl.ttl'

    # collect errors to display on exit
    errors = []

    print("Starting file validation.")

    for file in scraped_json_files:
        try:
            r = validate(file,
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
                print(f"{file} failed validation.")
            # otherwise, move file to valid_json folder
            else:
                renamed_file = str(file.split(".")[-2] + ".json")
                file.replace(".data/raw_json/", "")
                os.rename(f"{file}", f"data/valid_json/{renamed_file}")
                print(f"{file} successfully validated.")

        except json.JSONDecodeError:
            errors.append(f"{file}\nBad JSON format. Validation aborted.")

    print(*errors, sep="\n") if errors else print("All files successfully validated.")
