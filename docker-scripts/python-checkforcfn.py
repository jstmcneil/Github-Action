import sys
import json
import yaml
import os

# Checking Specific File: only YAML & JSON inputs.
with open(sys.argv[1], "r") as file:
	print(file)
	filename, file_extension = os.path.splitext(sys.argv[1])
	if file_extension.lower() == ".yaml" or file_extension == ".yml":
		data = yaml.load(file, Loader=yaml.FullLoader)
	else:
		data = json.load(file)
	if ("AWSTemplateFormatVersion" in data or "Resources" in data):
		# If we have CFM template fields, sucessfully exit.
		sys.exit(0)
	else:
		# If we don't have CFM template fields, generic error exit. 
		sys.exit(1)
