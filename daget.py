#!/usr/bin/env python3
import sys
import os
import json
import darkened
import pastee3

__version__ = (0, 1, 0)

pasteclient = pastee3.PasteClient()

def todarkive(s,folder,filename):
    """Store a string as a file in the "darkive", and notify the user"""
    folder = os.path.join('darkive',folder)
    os.makedirs(folder,0o700,True)
    filename = os.path.join(folder,filename)
    if os.path.exists(filename):
        sys.stderr.write('# Skipping existing file! {}\n'.format(filename))
    else:
        open(filename,'w').write(s)
        sys.stderr.write('# Wrote file: {}\n'.format(filename))

def daget(pasteid):
    pasteid = pasteid.split('/')[-1] # in case it's a full url
    if '#' in pasteid:
        p,needhash = pasteid.split('#')
    else:
        p,needhash = pasteid,None
    sys.stderr.write('# getting paste {}\n'.format(p))
    payload = pasteclient.sloppy_get(p)
    if not payload:
        sys.stderr.write('# bad or missing pastee!\n')
        return False
    if needhash:
        gothash = darkened.hash64(bytes(payload.strip(),'ascii','replace'))
        if gothash == needhash:
            sys.stderr.write('# Hash Matches\n')
            d = json.loads(payload)
            todarkive(payload,d['msgid'],'{}.json'.format(p))
            return True
        else:
            sys.stderr.write('# Hash mismatch! need {}, got {}. Corrupt paste?\n'.format(repr(needhash),repr(gothash)))
            todarkive(payload,'corrupt','{}.corrupt.json'.format(p))
            return False
    else:
        sys.stderr.write('# Not checking hash(!)\n')
        d = json.loads(payload)
        todarkive(payload,d['msgid'],'{}.unverified.json'.format(p))
        return True

if __name__=='__main__':
    if len(sys.argv)<2:
        sys.stderr.write("""Usage: {} pasteeurl[#hash] ...
E.g. {} https://pastee.org/69f38#V4F8BjwgSfzkaentZlcBsacuLNM= hzrk2
(second argument is in the shortest form: only id, no hash)
""")
        sys.exit(1)
    for pasteid in sys.argv[1:]:
        sys.stderr.write('### getting {}\n'.format(pasteid))
        daget(pasteid)
