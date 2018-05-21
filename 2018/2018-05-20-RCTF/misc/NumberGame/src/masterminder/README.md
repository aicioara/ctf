masterminder
============

*I wrote this little script a few years ago. As the holiday season comes upon us once again, I decided to spruce it up with some nice colors—and a voice—for another year of family mischief.*

This is a program that plays [Mastermind](https://en.wikipedia.org/wiki/Mastermind_(board_game))... and always wins! To play in interactive mode
(i.e. for facing off against your friend), just run:

```
$ python masterminder.py
```

(Don't be alarmed—it talks!)

If you instead just want to see it play against itself by giving it a pattern
to start with, just run

```
$ python masterminder.py ABCD
```

where ABCD is any string of four colors that represent the secret configuration
(for example, WWOO for white-white-orange-orange).

E.g.
====
<img width="663" alt="A screenshot of the program." src="https://cloud.githubusercontent.com/assets/1410202/20872389/adca0270-ba63-11e6-93cc-a751ae487be8.png">

Behind the scenes
=================

This script essentially implements the minimax algorithm as demonstrated by Donald Knuth [in 1977](https://en.wikipedia.org/wiki/Mastermind_(board_game)#Five-guess_algorithm).

Feel free to adjust the variables at the top of the file to fit your version of the game.
