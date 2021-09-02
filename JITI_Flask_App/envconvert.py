import os, sys
import string

# if your project is in the parent directory, you may need this:
os.chdir("JITI_Flask_App")

with open('environment.yml') as f:
    read_file = f.readlines()

with open('env-min.yaml', "w") as f:
    substring_list = [
        "name:",
        "channels:",
        "- defaults",
        "dependencies:",
        "pip:"
    ]

    for line in read_file:
        # https://stackoverflow.com/a/8122096/3255525
        if any(substring in line for substring in substring_list):
            f.write(line)
        else:
            newline = line.split("=")[0]
            f.write(newline + "\n")
