#!/usr/bin/python
import io
import json
import re
import sys
from pprint import pprint
from timeit import Timer


def _json_import():
    parsed_dict = {}
    URL = "https://raw.githubusercontent.com/jaredrummler/AndroidDeviceNames" \
          "/master/json/devices.json"

    try:
        import requests
        requests.packages.urllib3.disable_warnings()  # No sensitive data.
    except ImportError:
        sys.exit("'requests' library required")

    r = requests.get(URL, stream=True)
    r.raise_for_status()

    data = r.json()

    pprint("Parsing %s total items" % len(data))

    for item in data:
        manu = item['manufacturer'].strip()
        model = item['model'].strip()
        name = item['market_name'].strip()
        if manu is None or manu == "" or \
                model is None or model == "" \
                or name is None or name == "":
            continue

        if re.match(manu.lower(), name.lower()):
            parsed_line = name[0].upper() + name[1:]
        else:
            parsed_line = "%s %s".strip() % (manu, name)

        parsed_dict[model] = parsed_line

    with io.open('parsed.devices', encoding="utf-8") as cached_file:
        read_data = cached_file.readlines()

    for line in read_data:
        lines = re.split("\s*=\s*", line)
        model = lines[0]
        name = lines[1].strip()

        parsed_dict[model] = name

    f = open("new.devices", mode="w")
    for k in sorted(parsed_dict.iterkeys()):
        if re.search('"', k): continue
        f.write("%s = %s\n" % (k, parsed_dict[k]))

    pprint("[%s] total entries parsed" % len(parsed_dict))


if __name__ == '__main__':
    t = Timer("print _json_import()",
              "from __main__ import _json_import")
    print "Total time: %s seconds\n" % str(t.timeit(1))[:4]
