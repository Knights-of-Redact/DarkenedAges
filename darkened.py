#!/usr/bin/env python3
import random
import time
import codecs
import hashlib
import json
import csv
import textwrap

CHAR_REDACTED = '\u2588'  # Full block.
CHAR_CONFLICT = '\u2573'  # Box drawings light diagonal cross.
NTRUSTEES = 3  # for now(?)

## [['an', 'msg', 'is', 'a', 'list', 'of', 'lines,'],
##  ['where', 'each', 'line', 'is', 'a', 'list', 'of', 'words.']]
def str2msg(s):
    "explode a string into an msg"
    return list(map(lambda l:l.split(), s.splitlines()))

def msg2str(ws):
    "implode an msg into a string"
    return '\n'.join(map(lambda l:' '.join(l), ws))

def mapmsgs(func, *msgs):
    """map func word-per-word on all corresponding words inside [a sequence of] msgs of the same structure. E.g.
>>> mapmsgs(lambda word1, word2:'({}/{})'.format(word1, word2), str2msg("a b\nc d"), str2msg("x y\nz w"))
[['(a/x)', '(b/y)'], ['(c/z)', '(d/w)']]"""
    return list(map(lambda s:list(map(lambda v:func(*v), zip(*s))), zip(*msgs)))

def msgget(msg, key, default=None):
    return mapmsgs(lambda d:d.get(key, default), msg)

## conversion helpers
def str2bytes(s):
    return bytes(s, 'utf8')

def bytes2str(b):
    return str(b, 'utf8', 'replace')

def bytes2base64(b):
    return str(codecs.encode(b, 'base64').strip(), 'ascii').replace('\n','')

def base642bytes(b64):
    if b64 is None: return None  # Might be missing
    return codecs.decode(bytes(b64, 'ascii'), 'base64')

## "crypto" functions
def makepad(b):
    """Returns a random pad with the same length as b,
encoded to base64.
You think this random function is weak? *Celebrate* that ;)"""
    return random._urandom(len(b))

def xor2(c1, c2):
    return c1^c2

def integrate2(a, b): 
    if a is None or a==b: return b
    if b is None: return a
    return ""  # Invoke a conflict [0 is always wrong length ;)]

def integrate(*args):
    if not args: return None
    if len(args)==1: return args[0]
    return integrate2(args[0], integrate(*args[1:]))
    
def _redact(s):
    plaintext = str2bytes(s)
    pad = makepad(plaintext)
    return {"cipher":bytes2base64(bytes(map(xor2, plaintext, pad))), "pad":bytes2base64(pad)}

def _unredact(cipher, pad):
    if pad is None:  # pad is missing
        return(CHAR_REDACTED*len(cipher))
    if len(cipher)!=len(pad):  # Failed the only integrity test ;)
        return(CHAR_CONFLICT*len(cipher))
    return str(bytes(map(xor2, cipher, pad)), 'utf8', 'replace')

def _disintegrate(value, k=NTRUSTEES):
    lucky = random.randint(0, k-1) 
    return [i==lucky and value or None for i in range(k)]

def disintegrate(msg, k=NTRUSTEES):
    zipped = mapmsgs(lambda p:_disintegrate(p, k), msg)
    return [mapmsgs(lambda v:v[i], zipped) for i in range(k)]

def redact(s, sender, recipients=[], subject="(untitled)", k=NTRUSTEES):
    msgid = makeid()
    trustees = choosetrustees(k,exclude=[sender]+recipients)
    header = {
        "msgid": msgid, "sender": sender, "recipients": recipients,
        "subject": subject, "trustees": trustees}

    redaction = mapmsgs(_redact, str2msg(s))
    pads = dict(zip(trustees,disintegrate(msgget(redaction, 'pad'), len(trustees))))
    result = {}
    result['__public__'] = header.copy()
    result['__public__']['cipher'] = msgget(redaction, 'cipher')
    result['__to__'] = header.copy()
    result['__to__']['pads'] = pads  # the whole shebang
    for t in trustees:
        result[t] = header.copy()
        result[t]['pads'] = {t: pads[t]}
    return result;

def unredact(cipher, pads, trustees=[]):
    cipher64 = cipher['cipher']
    pads64 = [pads['pads'][t] for t in pads['pads']
                 if not trustees or t in trustees]
    return msg2str(mapmsgs(
        _unredact,
            mapmsgs(base642bytes, cipher64),
            mapmsgs(base642bytes,
                mapmsgs(integrate, *pads64))))

def hash64(b):
    "Returns base64 of sha1 (appended as hash to paste urls against evil eye)"
    return str(codecs.encode(hashlib.sha1(b).digest(),'base64').strip(),'ascii')

## Game functions

def makeid():
    """msgid (e.g. can be used as hashtags in move twists).
Sorting by it is like sorting by time,
it looks fancy enough, and would probably never collide"""
    return 'DA{:.4f}'.format(time.time()).replace('.', '')

def getplayers():
    "returns players.csv as a dict"
    c=csv.reader(open('players.csv'))
    names = next(c)
    d = {}
    for r in c:
        p = dict(zip(names, r))
        d[p['player']] = p
    return d

def choosetrustees(k=NTRUSTEES, exclude=[], players=None):
    if players is None:
        players = getplayers()
    candidates = list(set(players.keys())-set(exclude))
    return random.sample(candidates, k)

#------ begin prefab redaction
prefab = {
    "__public__": {"trustees": ["ted", "dan"], "sender": "alice",
    "msgid": "DA14341968415407", "recipients": ["bob", "carol"],
    "subject": "Hey, sport. YOU connect the dots.", "cipher":
    [["lgPNUJU8", "qLvBBQ==", "5GfdMat4", "z8hPe4BlxxdUMXzi4w==",
    "2IheMA==", "uZyB", "wVCtnQ==", "VnU=", "/pTNipiB55M=", "XcT1gQ==",
    "gxU8", "9MYX", "io0="], ["0fOyC2/y", "bg8=", "bu2T", "rJH6dWUzpg==",
    "B4BTkvtl", "+Ug=", "6wky", "H78=", "nx8=", "TO3/fbE=", "tqw=",
    "S4k8", "+mXOsQ==", "E3rblIM=", "bIu6qbrh1g=="], ["sfjl",
    "JBxnLbfe0k0n", "BShgq+QrmdquMA==", "VYD1hx8=", "MLk=", "ig==",
    "oasqOoWF", "Asw=", "Rof1s/gpQQONcnk=", "ZW3zOSnTvyg=", "QlA=",
    "6Q0qOw=="], ["9fPa", "2mFZdDltLL4=", "13vdBg==", "+eWH",
    "koB24LLGnxs=", "CedkJ3k=", "b41+QUU=", "fRkV", "4/Yc", "anY6cA==",
    "muk=", "9LrH", "5t1uXU0=", "M1eqTaWs"], ["8Ah2Pq4=", "ouQ=",
    "miJQVgwle6yOcg==", "PPc=", "6jes", "kYsY2ynZdg=="]]}, "dan":
    {"trustees": ["ted", "dan"], "sender": "alice", "msgid":
    "DA14341968415407", "pads": {"dan": [[None, None, None, None,
    "nvo/RQ==", "7ebk", None, "Pxs=", "jvG/+ffvzr8=", "KayU9Q==", "8H1Z",
    "nKdz", "5OI="], [None, "GmA=", "GoX2", "/OSQHAtXxw==", "d+Ej94lL",
    None, None, "fsw=", None, None, None, None, None, None,
    "AO7bwt+F+A=="], [None, "YXBKZdaztixJ", "YEYD2Z1b7bPBXg==",
    "NvKU5HQ=", None, "6w==", "085ZT+nx", "bao=", None, "FwiAXEih3EA=",
    "ICk=", "r1l+FQ=="], [None, None, None, "jY3i", None, None,
    "R/kWIDE=", "O01B", None, None, "84c=", None, "kq8PNCM=", "UCXLPs2F"],
    ["h2cYGdo=", "wIE=", None, None, "nl/J", None]]}, "recipients":
    ["bob", "carol"], "subject": "Hey, sport. YOU connect the dots."},
    "__to__": {"trustees": ["ted", "dan"], "sender": "alice", "msgid":
    "DA14341968415407", "pads": {"dan": [[None, None, None, None,
    "nvo/RQ==", "7ebk", None, "Pxs=", "jvG/+ffvzr8=", "KayU9Q==", "8H1Z",
    "nKdz", "5OI="], [None, "GmA=", "GoX2", "/OSQHAtXxw==", "d+Ej94lL",
    None, None, "fsw=", None, None, None, None, None, None,
    "AO7bwt+F+A=="], [None, "YXBKZdaztixJ", "YEYD2Z1b7bPBXg==",
    "NvKU5HQ=", None, "6w==", "085ZT+nx", "bao=", None, "FwiAXEih3EA=",
    "ICk=", "r1l+FQ=="], [None, None, None, "jY3i", None, None,
    "R/kWIDE=", "O01B", None, None, "84c=", None, "kq8PNCM=", "UCXLPs2F"],
    ["h2cYGdo=", "wIE=", None, None, "nl/J", None]], "ted": [["xWusIv5F",
    "29q4dg==", "zAa7Rc4K", "pqY7HvIXqHA1RRWMhA==", None, None,
    "lSXD+g==", None, None, None, None, None, None], ["sJDRbhyB", None,
    None, None, None, "uDs=", "jWhA", None, "6Ho=", "J4OQCp0=", "39g=",
    "JuhF", "kgS41A==", "fR+t8fE=", None], ["5ZCA", None, None, None,
    "Wco=", None, None, None, "L+mR1ohML2foHA0=", None, None, None],
    ["sbuL", "qhM8EFAOWM0=", "oxO8cg==", None, "/eYQidGv/nc=", "epMLVQA=",
    None, None, "i5dv", "Dh9fFA==", None, "gNKi", "lrEPMyg=", None],
    [None, None, "+UoxOmBAFcvrFg==", "Xo4=", None, "4f56t0C6WA=="]]},
    "recipients": ["bob", "carol"], "subject": "Hey, sport. YOU connect "
    "the dots."}, "ted": {"trustees": ["ted", "dan"], "sender": "alice",
    "msgid": "DA14341968415407", "pads": {"ted": [["xWusIv5F", "29q4dg==",
    "zAa7Rc4K", "pqY7HvIXqHA1RRWMhA==", None, None, "lSXD+g==", None,
    None, None, None, None, None], ["sJDRbhyB", None, None, None, None,
    "uDs=", "jWhA", None, "6Ho=", "J4OQCp0=", "39g=", "JuhF", "kgS41A==",
    "fR+t8fE=", None], ["5ZCA", None, None, None, "Wco=", None, None,
    None, "L+mR1ohML2foHA0=", None, None, None], ["sbuL", "qhM8EFAOWM0=",
    "oxO8cg==", None, "/eYQidGv/nc=", "epMLVQA=", None, None, "i5dv",
    "Dh9fFA==", None, "gNKi", "lrEPMyg=", None], [None, None,
    "+UoxOmBAFcvrFg==", "Xo4=", None, "4f56t0C6WA=="]]}, "recipients":
    ["bob", "carol"], "subject": "Hey, sport. YOU connect the dots."}}
#------ end prefab redaction

def testit():
    "Todo: turn this into proper unit tests, anyone?"
    print('### Players')
    for p in getplayers().values():
        print('\n# {name} ({player}, @{twister}):'.format(**p))
        print('\n'.join('  '+l for l in textwrap.wrap(p['bio'])))
    print('\n\n### Redacting prefab plaintext (2 trustees)')
    plaintext = "Here's the first line, \nfollowed by a second one"
    redaction = redact(plaintext, 'alice', recipients=['bob','carol'], subject='Is this thing on?', k=2)
    for line in textwrap.wrap(json.dumps(redaction)): print(line)
    for t in redaction['__public__']['trustees']:
        print('\n# >>> Unredaction for trustee: {}'.format(t))
        print(unredact(redaction['__public__'], redaction[t]))
    print('\n### >>> integration >>>')
    print(unredact(redaction['__public__'], redaction['__to__']))
    print('\n\n### Unredaction of prefab message (with conflicting pads)')
    for t in prefab['__public__']['trustees']:
        print('\n# >>> Unredaction for trustee: {}'.format(t))
        print(unredact(prefab['__public__'], prefab['__to__'],trustees=[t]))
    print('\n### >>> integration >>>')
    print(unredact(prefab['__public__'], prefab['__to__']))

if __name__=='__main__':
    testit()
