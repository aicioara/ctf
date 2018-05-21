# Adapted from https://github.com/theopolisme/masterminder
# THIS IS NOT MY CODE!

# -*- coding: utf-8 -*-

import itertools
import operator
import random
import sys
import time

NUMBER_OF_SLOTS = 4
COLORS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
COLOR_NAMES = {
    '0': '0',
    '1': '1',
    '2': '2',
    '3': '3',
    '4': '4',
    '5': '5',
    '6': '6',
    '7': '7',
    '8': '8',
    '9': '9',
    # 'W': 'white',
    # 'O': 'orange',
    # 'Y': 'yellow',
    # 'M': 'magenta',
    # 'P': 'purple',
    # 'T': 'teal'
}

RED_WHITE_COMBOS = sum([[[i, j] for j in range(NUMBER_OF_SLOTS + 1 - i)]
                      for i in range(NUMBER_OF_SLOTS + 1)], [])
RED_WHITE_COMBOS.remove([NUMBER_OF_SLOTS - 1, 1])  # Impossible configuration

class termcolors:
    """So we can show pretty colors in our console output!"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class MastermindGame(object):
    """This represents a Mastermind game."""

    def __init__(self):
        self.all_possibilities = [''.join(possibility)
                                  for possibility in itertools.permutations(
                                  COLORS, NUMBER_OF_SLOTS)]
        self.possibilities = self.all_possibilities
        self.past_guesses = []
        self.autoplay_solution = None
        self.last_guess = ()

    def start_game(self, with_autoplay_solution=None):
        """Alwyas start by guessing two different colors, in pairs (aabb).
        If "with_autoplay_solution" is specified (a string in the form abcd),
        the masterminder will play itself to the solution instead of requiring
        human intervention.
        """

        print termcolors.HEADER + termcolors.UNDERLINE + 'Welcome to Masterminder!' + termcolors.ENDC

        if with_autoplay_solution:
            self.autoplay_solution = with_autoplay_solution

        colors = random.sample(COLORS, 4)
        return (colors[0], colors[1], colors[2], colors[3])
        # self.guess(colors[0] + colors[1] + colors[2] + colors[3])

    def _compute_red_white(self, guess, solution):
        """Compute the red/whites returned given a guess for particular
        possibile final solution. Red indicates a correct color in a correct
        position; white indicates a correct color in the wrong position.
        """

        red = 0
        white = 0
        guess = list(guess)
        solution = list(solution)

        for index, color in enumerate(solution):
            if guess[index] == color:
                red += 1
                guess[index] = None
                solution[index] = None

        for color in guess:
            if color is not None and color in solution:
                white += 1
                solution[solution.index(color)] = None

        return {
            'red': red,
            'white': white
        }

    def _check_red_white(self, guess, solution, red, white):
        """Checks if a given guess would return the given red & white for
        a given solution.
        """
        result = self._compute_red_white(guess=guess,
                                         solution=solution)

        return result['red'] == red and result['white'] == white

    def filter_possibilities(self, guess, red, white):
        """Remove all possibilities that would not give the given score of
        of red and white pegs if they were the answer.
        """

        new_possibilities = []

        for possibility in self.possibilities:
            if self._check_red_white(guess, possibility, red, white):
                new_possibilities.append(possibility)

        self.possibilities = new_possibilities

    def _prompt_for_integer(self, message):
        """Prompt the user to enter an integer."""
        result = None
        while result is None:
            try:
                result = int(
                    raw_input(termcolors.OKBLUE + message + termcolors.ENDC)
                )
            except ValueError:
                print termcolors.FAIL + "Integer only, please." + \
                    termcolors.ENDC
        return result

    def validate(self, guess):
        self.last_guess = guess

        i_am_guessing_statement = "Okay, I'm guessing {}."
        long_names = self._pretty_print_pattern(guess)
        print termcolors.OKGREEN + i_am_guessing_statement.format(guess) + \
            termcolors.ENDC
        self.say(i_am_guessing_statement.format(long_names))

        self.past_guesses.append(guess)

    def guess(self, red, white):
        """Perform a guess routine - state the guess, prompt for red/white,
        filter appropriately, then continue to the next guess.
        """

        # red = self._prompt_for_integer("How many are the correct color in " +
        #                           "the correct position (red): ")
        # white = self._prompt_for_integer("How many are the correct color but " +
        #                             "in the wrong position (white): ")

        if red == 4:
            self.say('Yay, I am a winner!')
            print termcolors.HEADER + \
                "Yay, I won in {0} guesses!".format(len(self.past_guesses))
            print self.serialize() + ' ✔' + termcolors.ENDC
            sys.exit()

        self.filter_possibilities(self.last_guess, red, white)
        return self.select_next_guess()

    def select_next_guess(self):
        """For each possible guess (even if it has been eliminated as a
        possible final solution), calculate how many possibilities from the
        remaining possibilities would be eliminated for each possible
        red/white score. The score of the guess is the least of such
        values. Play the guess with the highest score (minimax).
        """

        print("{0} possible solutions remain...".format(len(self.possibilities)))
        start_time = time.time()

        self.say("Now I'm thinking")

        if len(self.possibilities) == 0:
            print termcolors.FAIL + 'Oh no! No solutions found. Did ' + \
                'you perhaps make an error in inputting the red/white ' + \
                'counts?\n' + self.serialize() + ' ❌' + termcolors.ENDC
            sys.exit()
        elif len(self.possibilities) == 1:
            print "Only one possibility left, so..."
            return self.possibilities[0]
        elif len(self.possibilities) == 2:
            print "There are only two possibilities left, so I'll just guess."
            return random.choice(self.possibilities)

        final_scores = {}

        def score_guess(guess):
            if guess in self.past_guesses:
                return

            guess_eliminates = None

            for red, white in RED_WHITE_COMBOS:
                combo_eliminates = 0
                for possibility in self.possibilities:
                    if not self._check_red_white(guess, possibility, red, white):
                        combo_eliminates += 1

                if guess_eliminates is None:
                    guess_eliminates = combo_eliminates
                elif combo_eliminates < guess_eliminates:
                    guess_eliminates = combo_eliminates

            final_scores[guess] = guess_eliminates

        for guess in self.all_possibilities[:700]:
            score_guess(guess)

        final_guess, eliminates = max(final_scores.iteritems(),
                                key=operator.itemgetter(1))

        seconds_elapsed = round(time.time() - start_time, 2)

        print(("My best option is guessing {}, to eliminate at worst {}/{} " +
            "possibilties ({}s elapsed).").format(final_guess, eliminates,
                                    len(self.possibilities), seconds_elapsed))

        # self.guess(final_guess)
        return final_guess

    def serialize(self):
        """Serialize the guessing history for fun & profit."""
        return '->'.join(self.past_guesses) + ''

    def say(self, statement):
        """Say something out loud. If we're autoplaying, we don't say
        anything, since that would be taking to ourselves which is odd.
        """
        if not self.autoplay_solution:
            print (statement)

    def _pretty_print_pattern(self, pattern):
        """Formats a pattern to use color names if available."""
        return '-'.join([COLOR_NAMES.get(c, c) for c in pattern])

def main():
    game = MastermindGame()
    if len(sys.argv) == 2:
        game.start_game(with_autoplay_solution=sys.argv[1])
    else:
        game.start_game()

if __name__ == '__main__':
    main()
