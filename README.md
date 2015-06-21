### DarkenedAges &mdash; a twister-based game of intrigue and bad crypto

![Trust ██ like █████. Be ███████.](https://i.imgur.com/WfhHOX0.png)

### TL;DR We play with partial leaks that look like this

      ██████ Alice, ███ ███████ ███ ███████ ███████ ████ ███████ legal ███████████ ███ delays ███ ██ serious problem
    + ██████ ██████ ███ doesn't get ███████ ███████ ████ ███████ legal ███████████ ███ ██████ ███ ██ ███████ problem
    = ______________________________________________________________________________________________________________
      ██████ Alice, ███ doesn't get ███████ ███████ ████ ███████ legal ███████████ ███ delays ███ ██ serious problem
    + ...
    = ______________________________________________________________________________________________________________
      Unlike Alice, Bob doesn't get dropped packets when pinging legal department, and delays are no serious problem

#### Slightly longer examples [here](https://raw.githubusercontent.com/Knights-of-Redact/DarkenedAges/master/output.txt) and [here](https://pastee.org/v46af).

For public moves and gossip, see [#DarkenedAges](https://twisterio.com/search?kw=%23darkenedages) on [twister](http://twister.net.co)

### In AD 2101, peace was beginning.

The Unigalitarian Church has abolished the internet. A source of a century of war, misfortune, and mistrust.
Instead, people are only allowed to communicate via a church sanctioned telegram system.

How can they enforce this?
How can the church be sure people aren't communicating via other means? For example a face to face talk between husband and wife, mother and daughter?
They simply ask nicely.

Every citizen has to go to a daily confession where he/she is interviewed by a priest/priestes who are well equiped and well trained to detect lies and deviant behavior.
It's a bit like the [Voight Kampff empathy test](https://youtu.be/Umc9ezAyJv0) ;) 

It's not that you are not allowed to communicate by means other than official telegrams. It's just that you have to report all such communications.
Other parties to such a conversation also have such duties, and are also being scrutinized daily under lie-detection gear and practices.
You simply assume they know it all already, and try to be as percise as possible, because a contradiction might start a pretty nasty investigation and waste inquisitive resources.

#### Privacy (to a reasonable extent)
The church understands the value of privacy: there's no merit for the soul in coerced righteousness. If sin can't tempt you, how can you be a saint?
This is why no one can read your telegrams, unless you're a suspect. If the court so orders, a telegram of yours might have to be exposed.
In order to do that, 8 keys should combined in order to expose the message (although the game will probably start with 4 or even 3 keys until we have enough players).
Each message is encrypted with 8 different keys. These keys are distributed to 8 random citizens called trustees. You too can become a trustee to one or more telegrams.
If you're not rich or educated enough (or just lazy), the church can manage a key crypt in your behalf.
This way, checks and balances are kept, and those who have nothing to hide have nothing to fear.

In the beginning, most people chose the easy options, and only deranged otaku teenagers bothered to manage one (It was easier for them. The Japanese manuals are the best. The English translation deliberately sucks).

Then came the attack on the El-Hamdan (EH) encryption [unofficially attributed to the late Frau Tse Tung, but you didn't hear it from me ;) ]**[1]**

#### In AD 2102, peace was beginning to make sense.

As you already know, copies of all telegrams are kept on record at the Publicly Available International Archive (PAIA) [aka Leakvile :)]
Now that EH encryption has been broken, 
It has created a booming black market. The currency is telegram keys (aka unredactions).
Today, anyone who wants to make some pocket money (and who doesn't?) manages her own key crypt. They're no longer the bulky church-issued software. Systems today convert back and forth between El-Hamdan ciphers and keys and their more juicy conterparts: leakables and unredactions. The black market system where the more keys you own, the more of the actual telegram (or leakable) is exposed to you.
You know the metadata of your adversaries. You know who they have been talking to. You might even be lucky enough to be a trustee to some of their communications.

Perhaps you could trade this information with their adversaries? The possibilities are endless.

### How to play

**Note:** All code here should be run with python3. No telling what this code might do on python2 ;)

#### First you need to join

* Every player should have a [twister](http://twister.net.co) account
* <del>If you know how, add a line about yourself to [players.csv](https://github.com/Knights-of-Redact/DarkenedAges/blob/master/players.csv),
(as a pull-request or something).</del> Bugger it. Just twist `@darkenedages I want to play #DarkenedAges` ;)
* You **should** follow all other players (and `@darkenedages`) [so that we can all DM each other].
* It is *recommended* to have `#DarkenedAges` in your profile, but the formal definition of "player" is
"one who appears at [players.csv](https://github.com/Knights-of-Redact/DarkenedAges/blob/master/players.csv)" ;)

#### Sending a message
In this example we send from and to fictional characters (NPCs) [the trustees are always "real" players].

    $ ./dasend.py chuck flava -s "Can't truss it" < msg.txt 
    == Publicly twist:
    #Darkenedages #DA14342254974005 public: https://pastee.org/69f38#V4F8BjwgSfzkaentZlcBsacuLNM=
    [No need to DM NPC] flava:
    #Darkenedages #DA14342254974005 full https://pastee.org/4bsd6#QxCkPf7+G3qt4u+Ibj1pQVmxdvU=
    == DM @thedod:
    #Darkenedages #DA14342254974005 trustee broyo: https://pastee.org/hzrk2#DopLVbR1IWiROpQ00u9ncZH5+RA=
    == DM @sandyclaws:
    #Darkenedages #DA14342254974005 trustee sandyclaws: https://pastee.org/yt3dd#UWIbch+CM7+W7CMKYAHEIwsd93Y=
    == DM @forth:
    #Darkenedages #DA14342254974005 trustee forth: https://pastee.org/783rv#tbsqCly/fu4uKwzwAJ73gNbGC+I=
    
As we see, `dasend.py` tells us what to twist and DM (maybe one day this will be integrated, no rush).

#### Receiving a message

If this was really happening on twister, and I was @thedod, I'd only know the `public:` and `trustee broyo:` pastes.
What I'd do would be:

    $ ./daget.py https://pastee.org/69f38#V4F8BjwgSfzkaentZlcBsacuLNM=
    ### getting https://pastee.org/69f38#V4F8BjwgSfzkaentZlcBsacuLNM=
    # getting paste 69f38
    # Hash Matches
    # Wrote file: darkive/DA14342254974005/69f38.json
    $ ./daget.py https://pastee.org/hzrk2#DopLVbR1IWiROpQ00u9ncZH5+RA=
    ### getting https://pastee.org/hzrk2#DopLVbR1IWiROpQ00u9ncZH5+RA=
    # getting paste hzrk2
    # Hash Matches
    # Wrote file: darkive/DA14342254974005/hzrk2.json

The folder `darkive/` gets created if it doesn't exist.

#### Unredacting a message

**New:** Running `./unredact.py` without arguments shows summaries of all darkive's messages
(todo: search).

    $ ./unredact.py darkive/DA14342254974005/
    # Scanning folder darkive/DA14342254974005
    msgid: DA14342254974005
    sender: chuck
    recipients: ['flava']
    trustees: ['broyo', 'forth', 'sandyclaws']
    subject: Can't truss it
    
    ████ ███ ██████ ████████ ███ a ███ ████
    Because ██ that now █ ████ my █████
    So ██████ █ ████ to the strong
    █████ ███ █████ ██ the █████
    and the smile ████ █████ ████ ████

Note that I could also do `./unredact.py DA14342254974005` but you
can prefix it with `darkive` and append `/` if that's what autocomplete
tempts you to do ;)

If `flava` was a real player, he'd do:

    $ ./daget.py https://pastee.org/4bsd6#QxCkPf7+G3qt4u+Ibj1pQVmxdvU=
    ### getting https://pastee.org/4bsd6#QxCkPf7+G3qt4u+Ibj1pQVmxdvU=
    # getting paste 4bsd6
    # Hash Matches
    # Wrote file: darkive/DA14342254974005/4bsd6.json

He could then simulate what `forth` and `sandyclaws` could do if
they shared the keys between them

    $ ./unredact.py darkive/DA14342254974005/ forth sandyclaws
    # Scanning folder darkive/DA14342254974005
    msgid: DA14342254974005
    sender: chuck
    recipients: ['flava']
    trustees: ['broyo', 'forth', 'sandyclaws']
    subject: Can't truss it
    
    King and chief, probably had █ big beef
    ███████ of ████ ███ I grit ██ teeth
    ██ here's a song ██ ███ ██████
    'Bout the shake of ███ snake
    ███ ███ █████ went along With that

#### Todo:

A utility to search the darkive by from/to/subject.

#### The `darkened.py` library [under the hood]

The file [output.txt](https://raw.githubusercontent.com/Knights-of-Redact/DarkenedAges/master/output.txt)
was produced with `python darkened.py > output.txt`. You should get a similar output if everything works well.

The motivation behind this "full retard crypto suite" is to create an environment where everyone can have a go at code breaking.

_______________________________________

**[1]** "It was never truly attributed to FTT, but it is believe that she has found the transformation between a 1/K El-Hamdan key and 1/K of the One Time Pad (OTP) equivalent of the session key when expanded (although she has failed to see that the data was chunked on a word boundary, as discovered by ████ 2 years earlier)." -- "Faster Than Thought", a biography of FTT by Jon Reinhardt


