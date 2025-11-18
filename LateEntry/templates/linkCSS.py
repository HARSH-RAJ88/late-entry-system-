import os
import re

for filename in os.listdir():

    if filename.endswith(".html"):
        print(filename)

        string = "{% load static %}\n"

        with open(filename, "r") as f:
            for line in f:
                match = re.search("assets/.*\.css", line)
                if match:
                    string += "<link rel=\"stylesheet\" href=\"{% static '" + match.group(0) + "' %}\">\n"
                else:
                    string += line

        with open(filename, "w") as f:
            f.write(string)

        string = ""

        with open(filename, "r") as f:
            for line in f:
                match = re.search(r"(assets/img/[^\"']*)", line)

                if match:
                    string += line.replace(match.group(0), "{% static '" + match.group(0) + "' %}")
                else:
                    string += line

        with open(filename, "w") as f:
            f.write(string)

        string = ""
        with open(filename, "r") as f:
            for line in f:
                if re.search("<form.*", line):
                    string += line + "{%csrf_token%}\n"
                else:
                    string += line

        with open(filename, "w") as f:
            f.write(string)

        string = ""
        with open(filename, "r") as f:
            for line in f:
                match = re.search("assets/.*\.js", line)
                if match:
                    string += "<script src=\"{% static '" + match.group(0) + "' %}\"></script>\n"
                else:
                    string += line

        with open(filename, "w") as f:
            f.write(string)
