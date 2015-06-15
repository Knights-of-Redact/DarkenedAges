#!/usr/bin/env python3
import sys
import os
import json
import darkened
import pastee3

__version__ = (0, 1, 0)

pasteclient = pastee3.PasteClient()

def fromdarkive(msgid):
    """Retrieve all files in a "darkive" folder, and returns cipher and consolidated pads"""
    folder = os.path.join('darkive',msgid)
    if not os.path.isdir(folder):
        sys.stderr.write('# Folder does not exist! {}\n'.format(folder))
        return None, None
    sys.stderr.write('# Scanning folder {}\n'.format(folder))
    cipher = None
    pads = None
    for f in os.listdir(folder):
        # sys.stderr.write('Reading {}\n'.format(f))
        try:
            d=json.load(open(os.path.join(folder,f)))
        except Exception as e:
            sys.stderr.write('Error reading {}! {}\n'.format(os.path.join(folder,f),e))
            continue
        if 'cipher' in d:
            cipher = d
        else:
            if pads:
                pads['pads'].update(d['pads'])  # Todo: check conflicts?
            else:
                pads = d
    return cipher, pads

def showmsg(msgid,trustees=[],detailed=True):
    # Trick to allow e.g. 'darkive/DA14342254974005/' (like autocomplete does)
    msgid = list(filter(None,msgid.split('/')))[-1]
    cipher,pads = fromdarkive(msgid)
    if cipher or pads:
        d = cipher or pads
        for k in ['msgid', 'sender', 'recipients', 'trustees', 'subject']:
            if k in d:
                print('{}: {}'.format(k,d[k]))
    if detailed and cipher:
        print()
        # Todo: unmessify redact() so that we don't need this kludge :s
        print(darkened.unredact(cipher,pads or {'pads':[]},trustees=trustees))

if __name__=='__main__':
    if len(sys.argv)<2:
        is_detailed = False
        if not os.path.isdir('darkive'):
            print('No "darkive" folder. You should run daget.py first')
            sys.exit(1)
        msgs = [m for m in os.listdir('darkive')
            if m!='corrupt' and os.path.isdir(os.path.join('darkive',m))]
        if not msgs:
            print('No messages in "darkive" folder. You should run daget.py first')
            sys.exit(0)
        for msgid in msgs:
            if msgid!='corrupt' and os.path.isdir(os.path.join('darkive',msgid)):
                print('# {} {}'.format(sys.argv[0],msgid))
                showmsg(msgid,detailed=False)
                print()
    else:
        showmsg(sys.argv[1],trustees=sys.argv[2:])
