import sys
import json

json_file = sys.argv[1]

with open(json_file) as input_json:
	input_json_string = input_json.read()
# with open(sys.argv[2], 'w') as output_file:
# 	output_file.write(input_json_string)
data = json.loads(input_json_string)

events = data["events"]
output = []
for event in events:
	# if event["_id"] in [x[0] for x in output]:

	# else:
	# 	output += [[event["_id"], event]]

	# TODO: build dataframe from json
