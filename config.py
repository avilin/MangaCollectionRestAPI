import json


with open("instance/config.json") as config_file:
  file_contents = config_file.read()
  
config_json = json.loads(file_contents)