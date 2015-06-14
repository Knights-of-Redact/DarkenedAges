#!/usr/bin/env python3
import sys
import optparse
import json
import darkened
import pastee3

__version__ = (0, 1, 0)

pasteclient = pastee3.PasteClient()

def paste(value, indent=None):
    b = bytes(json.dumps(value, indent=indent).strip(), 'ascii')
    h = darkened.hash64(b)
    return '#'.join((pasteclient.paste(b, ttl=365), h))

def main():
    parser = optparse.OptionParser(
        usage='%prog [options] From To [To ...]',
        epilog='This will create some pastee.org pastes, '
            'and write stuff you need to copy/paste and tweet/DM')
    parser.add_option("-s", "--subject", default="(untitled)",
                      help=("Subject"))
    parser.add_option("-d", "--debug", action="store_true",
                      help=("Debug: don't crate pastes, dump as json to stdout instead"))
    (options, args) = parser.parse_args()
    if len(args)<2:
        parser.print_help()
        exit(1)
    redaction = darkened.redact(sys.stdin.read(), sender=args.pop(0), recipients=args, subject=options.subject)
    if options.debug:
        json.dump(redaction, sys.stdout, indent=4)
    else:
        players = darkened.getplayers()
        payload = redaction.pop('__public__')
        pasteurl = paste(payload, indent=4)
        print('== Publicly twist:\n#Darkenedages #{} public: {}'.format(payload.get('msgid', 'bug!!!'), pasteurl))
        payload = redaction.pop('__to__')
        pasteurl = paste(payload, indent=4)
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
