# coding: utf8 -*-
import re
import codecs
import sys

input_file = sys.argv[1] if len(sys.argv) == 2 else 'list.env'
with codecs.open(input_file) as env:
    txt = env.read()

targets_list = {
    "list_lib": r'list_lib="(?P<target>.+)"',
    "list_so": r'list_so="(?P<target>.+)"',
    "list_common_so": r'list_common_so="(?P<target>.+)"',
    "list_bin": r'list_bin="(?P<target>.+)"',
}
result_list = dict()

for name, reg in targets_list.items():
    result = re.search(reg, txt, re.MULTILINE)
    if result is None:
        continue
    target = result.groupdict()['target'].rstrip().lstrip()

    target = target.replace('\t', ' ')
    print("============>", target)
    while '  ' in target:
        target = target.replace('  ', ' ')
    result_list[name] = target.split(' ')
    print(name, target)

body = ''
for name, components in result_list.items():
    body += f'  <!-- {name} -->\n'
    for com in components:
        body += f'  <project path="hqt401r03/{com}" name="new_energy/top/{com}"/>\n'

txt = f"""<?xml version="1.0" encoding="UTF-8"?>
<manifest>
  <remote  name="gitlab" fetch=".."  review="gitlab.hopechart.com"/>
  <remote  name="origin" fetch="ssh://git@gitlab.hopechart.com/RD1" review="gitlab.hopechart.com" revision="master"/>
  <default revision="master" remote="origin" sync-c="true" sync-j="4"/>
  
  <project path="hqt401r03/hqt401r03" name="projects/hqt401r03"/>
  <!-- Component -->

  {body}
</manifest>
"""

with codecs.open('hqt401r03.xml', 'w', encoding='utf8') as xml:
    xml.write(txt)
