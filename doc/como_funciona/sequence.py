#!/usr/bin/python
#
# made: http://www.websequencediagrams.com/embedding.html
#
# minor changes by Hugo Ruscitti
import urllib
import os
import re
import sys


def getSequenceDiagram( text, outputFile, style = 'default' ):
    request = {}
    request["message"] = text
    request["style"] = style

    url = urllib.urlencode(request)

    f = urllib.urlopen("http://www.websequencediagrams.com/", url)
    line = f.readline()
    f.close()

    expr = re.compile("(\?img=[a-zA-Z0-9]+)")
    m = expr.search(line)

    if m == None:
        print "Invalid response from server."
        return False

    urllib.urlretrieve("http://www.websequencediagrams.com/" + m.group(0),
            outputFile )
    return True

style = "qsd"
text = "alice->bob: authentication request\nbob-->alice: response"
pngFile = "out.png"


if len(sys.argv) < 2:
    print "usage %s INPUT_FILENAME [OUTPUT_PNGNAME]" %(sys.argv[0])
    sys.exit(1)

filename = sys.argv[1]

if not os.path.exists(filename):
    print "File not found: %s" %(filename)
    sys.exit(1)

if len(sys.argv) == 3:
    output = sys.argv[2]
else:
    only_name = os.path.splitext(filename)[0]
    output = only_name + ".png"

input_file = open(filename)
input_text = input_file.read()
input_file.close()

print "Creating: %s" %(output)
getSequenceDiagram(input_text, output, style) 
