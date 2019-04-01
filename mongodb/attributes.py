import sys
import json
import numpy as np

json_file = sys.argv[1]

with open(json_file) as input_json:
	input_json_string = input_json.read()
data = json.loads(input_json_string)

events = data["events"]
id_list = []
fields = []

for event in events:
	if event["_id"] not in id_list:
		id_list.append(event["_id"])
	if event["event"] not in fields:
		fields.append(event["event"])

output = {}

id_list = sorted(id_list)

for this_id in id_list:
	this_tuple = []
	for f in fields:
		this_tuple.append(0)
	output.update({this_id: this_tuple})

for event in events:
	this_tuple = output[event["_id"]]
	this_tuple[fields.index(event["event"])] = event["count"]
	output.update({this_id: this_tuple})

# dtype = dict(names = fields, formats=formats)
output_array = np.array([[x[0]] + x[1] for x in list(output.items())])

np.savetxt(sys.argv[2], output_array, delimiter=",")
