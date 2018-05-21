# Number Game - misc

## Problem

Guess Guess Guess

nc 149.28.139.172 10002

Then

```
sha256(****+yHn1M1ZBTLVP2zQh) == 1fdfcd161d85b245030e4dd1e5e0fae9b11afc45a4b048667503009a77ccfa19
Give me XXXX:
```

## Tools used

- Python
- GitHub

## Solution

Seems like it wants me to find 4 characters, which are then concatenated to a salt to give me the hash.

```python
def crack(salt, hash):
    alphabet = string.letters + string.digits

    for prefix in itertools.product(alphabet, repeat=4):
        candidate = "".join(prefix) + salt
        h = hashlib.sha256(candidate).hexdigest()
        if h == hash:
            return "".join(prefix)
            break

print crack('yHn1M1ZBTLVP2zQh', '1fdfcd161d85b245030e4dd1e5e0fae9b11afc45a4b048667503009a77ccfa19')
```

But it is not over. This is just a Proof of Work for the real challenge.

## Problem 2

```

  o__ __o             o__ __o    ____o__ __o____   o__ __o__/_
 <|     v\           /v     v\    /   \   /   \   <|    v
 / \     <\         />       <\        \o/        < >
 \o/     o/       o/                    |          |
  |__  _<|       <|                    < >         o__/_
  |       \       \                    |          |
 <o>       \o       \         /         o         <o>
  |         v\       o       o         <|          |
 / \         <\      <\__ __/>         / \        / \



In every round of the game, I'll choose some different numbers from the figure interval. You are required to guess those numbers,ofc so does the order of them.
On each surmise of yours, 2 numbers will be told as a hint for you, but you need to speculate the fuctions of these 2 figures. (XD
GLHF

================== round 1 ==================
Give me 4 numbers, in[0, 10), You can only try 6 times
0 0 0 0
Nope. 0, 0
1 1 1 1
Nope. 0, 0
2 2 2 2
Nope. 1, 0
2 1 1 1
Nope. 1, 0
1 2 1 1
Nope. 0, 1
1 1 2 1
Nope. 0, 1
You lose, Correct answer is 2 5 6 7 .Bye.
```

If you get it right, it continues for 8 rounds

## Solution 2

This is a variation of the [Mastermind](https://en.wikipedia.org/wiki/Mastermind_(board_game))

The two numbers the server returns are the number of red pegs and the number of white pegs.

You get a red peg for every number you found and got at the right position and a white peg for every number you got right but not in the right position.

This is a variation of the game, because the original game uses 6 colors (in our case would be digits 0-5 rather than 0-9) and and the colors can be repeated, while for us it appears that the numbers are all distinct.

Now I can write my own min-max algorithm, but github is my friend. Quick search for mastermind, selecting the top three repositories and looking through the code should do.

I settled on https://github.com/theopolisme/masterminder because it was clean, single-file, easy to follow and it looked like it was coded in a very extensible way (which I needed since I had a variation of mastermind).

Changes made:

- Separated the recursive architecture of the `guess()` function into stateful `validate()` and `guess()` for better interaction.
- Changed colors from the 6 letters to the 10 digits I have
- Changed the initial `self.all_possibilities` from an `itertools.product` to a `itertools.permutations` to avoid repeated digits

And that was about it, the architecture of `guess()` being the most work. Also, since this was python, the program was to slow and the server was timing out after 30 seconds of inactivity, so I had to change the solution to only consider up to 700 branches in the (I hope) minmax.

After this, just some python plumbing and interaction with the server through the `socket` package. And let it run.

The issue was that the library did not guarantee to solve mastermind in less than 6 moves, so usually in round 5-7 it was failing to find the solution. However, running it in parallel on 8 CPU cores did the trick.

**Flag: RCTF{0lD_GaM3_nAmed_Bu11s_4nd_C0ws}**
