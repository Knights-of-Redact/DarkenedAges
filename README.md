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

#### Slightly longer examples [here](http://bl.ocks.org/thedod/raw/7a4a81224b5bed676b00/) and [here](https://pastee.org/v46af).

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

More info soon, meanwhile here's how to become a player:

* Every player should have a [twister](http://twister.net.co) account
* <del>Fork this, add a line about yourself to `players.csv`, and mention `@darkenedages` on twister with a link to your forked gist.</del> Bugger it. Just twist `@darkenedages I want to play #DarkenedAges` ;)
* It is recommended to follow `@darkenedages` and have `#DarkenedAges` in your profile, but the formal definition of "player" is "one who appears at `players.csv`" ;)

Essentially [index.html](http://bl.ocks.org/thedod/raw/7a4a81224b5bed676b00/) was produced with `python darkened.py > index.html`.
The motivation behind this "full retard crypto suite" is to create an environment where everyone can have a go at code breaking.

_______________________________________

**[1]** "It was never truly attributed to FTT, but it is believe that she has found the transformation between a 1/K El-Hamdan key and 1/K of the One Time Pad (OTP) equivalent of the session key when expanded (although she has failed to see that the data was chunked on a word boundary, as discovered by ████ 2 years earlier)." -- "Faster Than Thought", a biography of FTT by Jon Reinhardt


