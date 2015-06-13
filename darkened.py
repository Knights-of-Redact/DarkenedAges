#!/usr/bin/env python3
import random
import time
import codecs
import json
import csv
import textwrap

CHAR_REDACTED = '\u2588'  # Full block.
CHAR_CONFLICT = '\u2573'  # Box drawings light diagonal cross.
NTRUSTEES = 3  # for now(?)

#------ begin prefab input
cipher1 = [
    ['lgPNUJU8', 'qLvBBQ==', '5GfdMat4', 'z8hPe4BlxxdUMXzi4w==', '2IheMA==',
     'uZyB', 'wVCtnQ==', 'VnU=', '/pTNipiB55M=', 'XcT1gQ==', 'gxU8', '9MYX',
     'io0='],
    ['0fOyC2/y', 'bg8=', 'bu2T', 'rJH6dWUzpg==', 'B4BTkvtl', '+Ug=', '6wky',
     'H78=', 'nx8=', 'TO3/fbE=', 'tqw=', 'S4k8', '+mXOsQ==', 'E3rblIM=',
     'bIu6qbrh1g=='],
    ['sfjl', 'JBxnLbfe0k0n', 'BShgq+QrmdquMA==', 'VYD1hx8=', 'MLk=', 'ig==',
     'oasqOoWF', 'Asw=', 'Rof1s/gpQQONcnk=', 'ZW3zOSnTvyg=', 'QlA=',
     '6Q0qOw=='],
    ['9fPa', '2mFZdDltLL4=', '13vdBg==', '+eWH', 'koB24LLGnxs=', 'CedkJ3k=',
     'b41+QUU=', 'fRkV', '4/Yc', 'anY6cA==', 'muk=', '9LrH', '5t1uXU0=',
     'M1eqTaWs'],
    ['8Ah2Pq4=', 'ouQ=', 'miJQVgwle6yOcg==', 'PPc=', '6jes', 'kYsY2ynZdg==']]
pad1 = [
    ['xWusIv5F', '29q4dg==', 'zAa7Rc4K', 'pqY7HvIXqHA1RRWMhA==', None, None,
     'lSXD+g==', None, None, None, None, None, None],
    ['sJDRbhyB', None, None, None, None, 'uDs=', 'jWhA', None, '6Ho=',
     'J4OQCp0=', '39g=', 'JuhF', 'kgS41A==', 'fR+t8fE=', None],
    ['5ZCA', None, None, None, 'Wco=', None, None, None, 'L+mR1ohML2foHA0=',
     None, None, None],
    ['sbuL', 'qhM8EFAOWM0=', 'oxO8cg==', None, '/eYQidGv/nc=', 'epMLVQA=',
     None, None, 'i5dv', 'Dh9fFA==', None, 'gNKi', 'lrEPMyg=', None],
    [None, None, '+UoxOmBAFcvrFg==', 'Xo4=', None, '4f56t0C6WA==']]
pad2 = [
    [None, None, None, None, 'nvo/RQ==', '7ebk', None, 'Pxs=',
     'jvG/+ffvzr8=', 'KayU9Q==', '8H1Z', 'nKdz', '5OI='],
    [None, 'GmA=', 'GoX2', '/OSQHAtXxw==', 'd+Ej94lL', None, None, 'fsw=',
     None, None, None, None, None, None, 'AO7bwt+F+A=='],
    [None, 'YXBKZdaztixJ', 'YEYD2Z1b7bPBXg==', 'NvKU5HQ=', None, '6w==',
     '085ZT+nx', 'bao=', None, 'FwiAXEih3EA=', 'ICk=', 'r1l+FQ=='],
    [None, None, None, 'jY3i', None, None, 'R/kWIDE=', 'O01B', None, None,
     '84c=', None, 'kq8PNCM=', 'UCXLPs2F'],
    ['h2cYGdo=', 'wIE=', None, None, 'nl/J', None]]
#------ end prefab input

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
>>> mapmsgs(lambda word1,word2:'({}/{})'.format(word1,word2),str2msg("a b\nc d"),str2msg("x y\nz w"))
[['(a/x)', '(b/y)'], ['(c/z)', '(d/w)']]"""
    return list(map(lambda s:list(map(lambda v:func(*v), zip(*s))), zip(*msgs)))

def msgget(msg,key,default=None):
    return mapmsgs(lambda d:d.get(key,default),msg)

## conversion helpers
def str2bytes(s):
    return bytes(s,'utf8')

def bytes2str(b):
    return str(b,'utf8','replace')

def bytes2base64(b):
    return str(codecs.encode(b,'base64').strip(),'ascii')

def base642bytes(b64):
    if b64 is None: return None  # Might be missing
    return codecs.decode(bytes(b64,'ascii'),'base64')

## "crypto" functions
def makepad(b):
    """Returns a random pad with the same length as b,
encoded to base64.
You think this random function is weak? *Celebrate* that ;)"""
    return random._urandom(len(b))

def makeid():
    "Looks fancy enough and would probably never collide"
    return 'DA{:.4f}'.format(time.time()).replace('.','')

def xor2(c1,c2):
    return c1^c2

def integrate2(a,b): 
    if a is None or a==b: return b
    if b is None: return a
    return ""  # Invoke a conflict [0 is always wrong length ;)]

def integrate(*args):
    if not args: return None
    if len(args)==1: return args[0]
    return integrate2(args[0],integrate(*args[1:]))
    
def _redact(s):
    plaintext = str2bytes(s)
    pad = makepad(plaintext)
    return {"cipher":bytes2base64(bytes(map(xor2,plaintext,pad))), "pad":bytes2base64(pad)}

def _unredact(cipher,pad):
    if pad is None:  # pad is missing
        return(CHAR_REDACTED*len(cipher))
    if len(cipher)!=len(pad):  # Failed the only integrity test ;)
        return(CHAR_CONFLICT*len(cipher))
    return str(bytes(map(xor2,cipher,pad)),'utf8','replace')

def _disintegrate(value,k=NTRUSTEES):
    lucky = random.randint(0,k-1) 
    return [i==lucky and value or None for i in range(k)]

def disintegrate(msg,k=NTRUSTEES):
    zipped = mapmsgs(lambda p:_disintegrate(p,k),msg)
    return [mapmsgs(lambda v:v[i],zipped) for i in range(k)]

def redact(s,k=NTRUSTEES):
    redaction = mapmsgs(_redact,str2msg(s))
    return {
        'cipher': msgget(redaction,'cipher'),
        'pads': disintegrate(msgget(redaction,'pad'),k)}

def unredact(cipher64,*pads64):
    return msg2str(mapmsgs(
        _unredact,
            mapmsgs(base642bytes,cipher64),
            mapmsgs(base642bytes,
                mapmsgs(integrate,*pads64))))

## Game functions
def getplayers():
    "returns players.csv as a dict"
    c=csv.reader(open('players.csv'))
    names = next(c)
    d = {}
    for r in c:
        p = dict(zip(names,r))
        d[p['player']] = p
    return d

def choosetrustees(n=NTRUSTEES, exclude=[], players=None):
    if players is None:
        players = getplayers()
    candidates = list(set(players.keys())-set(exclude))
    return random.sample(candidates,n)

def testit():
    "Todo: turn this into proper unit tests, anyone?"
    print('<!DOCTYPE html><html lang="en"><head><title>Testing DarkenedAges library</title><meta http-equiv="Content-Type" content="text/html; charset=UTF-8" /></head><body><pre>')
    print('### Players')
    for p in getplayers().values():
        print('\n# {name} ({player},@{twister}):'.format(**p))
        print('\n'.join('  '+l for l in textwrap.wrap(p['bio'])))
    print('\n\n### Simulating a random selection of {} trustees for msgid #{}'.format(NTRUSTEES,makeid()))
    print(choosetrustees(exclude=['GCHQ']))  # Wishful thinking ;)
    print('\n\n### Redacting prefab plaintext (2 trustees)')
    plaintext = "Here's the first line,\nfollowed by a second one"
    redaction = redact(plaintext,2)
    for pad in redaction['pads']:
        print('\n# pOTP >>>')
        print(pad)
        print('# >>> Unredaction')
        print(unredact(redaction['cipher'],pad))
    print('\n### >>> integration >>>')
    print(unredact(redaction['cipher'],*redaction['pads']))
    print('\n\n### Simulating incoming [prefab] ciphertext and conflicting pads')
    for pad in [pad1,pad2]:
        print('\n# pOTP >>>')
        #print(json.dumps(pad,indent=4))
        print(pad)
        print('# >>> Unredaction')
        print(unredact(cipher1,pad))
    print('\n### >>> integration >>>')
    print(unredact(cipher1,pad1,pad2))

    print('</pre></body></html>')

if __name__=='__main__':
    testit()
