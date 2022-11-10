import os
import glob
from pyshacl import validate

# VALIDATE SCRAPED DATA #

### dev ### 
# clear destination dir
files = glob.glob("data/valid_json/*")
for file in files:
    os.remove(file)    
### /dev ###


# scraped JSON-LD files 
scraped_json_files = glob.glob("data/raw_json/*")

# SHACL file to validate data against
shacl_file = 'data/defs/court-data-standard-shacl.ttl'

errors = []

def validate_json(scraped_json_files, shacl_file):
    """
    validate scraped json files
    if valid, move to valid_json folder
    if not, append error msg to errors
    """

    for file in scraped_json_files:
        if len(scraped_json_files) < 1:
            print("No files provided. Validation aborted.")
            break
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
                file.replace(".data/raw_json/","")
                os.rename(f"{file}", f"./data/valid_json/{renamed_file}")
                print(f"{file} successfully validated.")
                
        except json.JSONDecodeError:
            errors.append(f"{file}\nBad JSON format. Validation aborted.")
            pass
    
    print(*errors, sep="\n") if errors else print("All files successfully validated.")

validate_json(scraped_json_files, shacl_file)