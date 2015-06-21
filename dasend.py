#!/usr/bin/env python3
import sys
import argparse
import json
import darkened
import pastee3
import daget

__version__ = (0, 1, 0)

pasteclient = pastee3.PasteClient()

def paste(value, indent=None):
    b = bytes(json.dumps(value, indent=indent).strip(), 'ascii')
    h = darkened.hash64(b)
    print('# Pasting...')
    return '#'.join((pasteclient.paste(b, ttl=365), h))

def main():
    parser = argparse.ArgumentParser(
        epilog='This will create some pastee.org pastes, '
            'and write stuff you need to copy/paste and tweet/DM')
    parser.add_argument('sender', metavar='from', help='sender of the message. That would you yourself')
    parser.add_argument('to', nargs='+', help='receipient(s) of the message. Character name, not twister handle!')

    parser.add_argument("-s", "--subject", default="(untitled)",
                      help=("Subject"))
    parser.add_argument('-i', '--input', type=str, help='Message file. If not provided, message will be read from stdin')
    parser.add_argument("-d", "--debug", action="store_true",
                      help=("Debug: don't crate pastes, dump as json to stdout instead"))

    options = parser.parse_args()

    if options.input is None:
        input_lines = sys.stdin.read()
    else:
        with open(options.input, 'r') as f:
            input_lines = f.read()
    redaction = darkened.redact(input_lines, sender=options.sender, recipients=options.to, subject=options.subject)
    if options.debug:
        json.dump(redaction, sys.stdout, indent=4)
    else:
        players = darkened.getplayers()
        payload = redaction.pop('__public__')
        pasteurl = paste(payload, indent=4)
        daget.daget(pasteurl)  # Save local copy.
        print('== Publicly twist:\n#Darkenedages #{} public: {}'.format(payload.get('msgid', 'bug!!!'), pasteurl))
        payload = redaction.pop('__to__')
        pasteurl = paste(payload, indent=4)
        daget.daget(pasteurl)  # Save local copy.
        for r in payload['recipients']:
            if r in players:
                print('== DM @{}:\n#Darkenedages #{} full: {}'.format(players[r]['twister'], payload.get('msgid', 'bug!!!'), pasteurl))
            else:
                print('[No need to DM NPC] {}:\n#Darkenedages #{} full: {}'.format(r, payload.get('msgid', 'bug!!!'), pasteurl))
        for t in redaction:  # Only trustees left after popping those two
            payload = redaction[t]
            pasteurl = paste(payload, indent=4)
            print('== DM @{}:\n#Darkenedages #{} trustee {}: {}'.format(players[t]['twister'], payload.get('msgid', 'bug!!!'), t, pasteurl))

if __name__ == "__main__":
  main()
