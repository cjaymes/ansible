#!/usr/bin/python

import sys
import json

from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['xml'])
)
if len(sys.argv) < 2:
    print('No template specified')
    sys.exit(1)

template = env.get_template(sys.argv[1])
if len(sys.argv) < 3:
    print(template.render())
else:
    print(template.render(**json.loads(sys.argv[2])))
