import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.axes as axes

class Contestant():
    """ Creates a contestant in the matchmaking game """

    def __init__(self, name = "Nameless"):
        """ creates a blank contestant """

        self.name = name
        self.not_matches = set()
        self.potential_matches = set()

    def not_match(self, bad_match):
        """ removes the bad_match from potential matches """

        self.not_matches.add(bad_match)
        self.potential_matches.discard(bad_match)

    def add_potential(self, potential):
        """ adds a potential new match """

        if potential not in self.not_matches:
            self.potential_matches.add(potential)

    def __repr__(self):
        """ returns the name of the contestant """

        return self.name


class Game():
    """ Creates a matchmaking game """

    def __init__(self, names):
        """ sets up the game """

        self.contestants = []
        self.set_contestants(names)
        self.unmatched = self.contestants[:] # list of contestants that have yet to be matched
        self.perfect_pairs = self.set_pairs(8)
        self.correct_guesses = set() # set of pairs that have already been correctly guessed
        self.correct_pairs = set() # set of this week's pairs that are perfect pairs
        

    def set_contestants(self, names):
        """ creates contestants for each name in the list """

        for name in names:
            self.contestants.append(Contestant(name))

    def set_pairs(self, num_pairs, unmatched = None):
        """ randomly divides remaining contestants into pairs """

        if unmatched == None:
            unmatched = self.unmatched

        contestant_copy = unmatched[:]
        pairs = []

        for index in range(num_pairs):
            first_max = 2 * (num_pairs - index) - 1
            second_max = 2 * (num_pairs - index - 1)
            pairs.append((contestant_copy.pop(random.randint(0, first_max)), contestant_copy.pop(random.randint(0, second_max))))

        return pairs

    def correct_pairs_this_week(self, week_pairs):
        """ checks which pairs are correctly matched from a set of pairs """

        # resets the correct pairs for this week
        self.correct_pairs = set()

        # checks each pair to see if they are a perfect match
        for pair in week_pairs:
            if self.is_pair_perfect(pair):
                self.correct_pairs.add(pair)

        # adjusts potential and bad matches
        for pair in week_pairs:
            if len(self.correct_pairs) == 0:

                pair[0].not_match(pair[1])
                pair[1].not_match(pair[0])

            else: 

                pair[0].add_potential(pair[1])
                pair[1].add_potential(pair[0])

    def is_pair_perfect(self, pair):
        """ returns True if pair is a perfect pair """

        if pair in self.perfect_pairs or (pair[1],pair[0]) in self.perfect_pairs:
            return True
        else:
            return False

    def check_pair(self, pair):
        """ chekcs if pair is a perfect pair and adjust additional information"""

        if self.is_pair_perfect(pair):
            
            self.unmatched.remove(pair[0])
            self.unmatched.remove(pair[1])

            for contestant in self.unmatched:
                for member in pair:
                    contestant.not_match(member)

            self.correct_guesses.add(pair)
            return True
        else:
            pair[0].not_match(pair[1])
            pair[1].not_match(pair[0])

            return False

    def random_solve(self, week = 0):
        """ Pairs are randomly set and the first one is selected """

        # base case
        if len(self.correct_guesses) == 8:
            return week

        # increments week number
        week += 1
        
        week_pairs = self.set_pairs(8 - len(self.correct_guesses))
        self.correct_pairs_this_week(week_pairs)

        # just guesses the first pair
        self.check_pair(week_pairs[0])

        # keep guessing until all pairs are found
        return self.random_solve(week)

    def comp_solve(self, week = 0, solve = None):
        """ Strategically picks guesses and sometimes pairs as well """

        if solve is None:
            solve = self.set_pairs

        # base case
        if len(self.correct_guesses) == 8:
            return week

        # increment week number
        week += 1

        week_pairs = solve(8 - len(self.correct_guesses))
        self.correct_pairs_this_week(week_pairs)

        guess = week_pairs[0]
        potential_num = float("inf")
        
        # figuring out the best guess assuming that this week has perfect matches
        if(len(self.correct_pairs) > 0):
            # checks each pair
            for pair in week_pairs:
                # if the pair is a potential match
                if pair[0] in pair[1].potential_matches:

                    # checks that there are not many other potential pairs for the contestants to be in
                    if len(pair[1].potential_matches) < potential_num and len(pair[1].potential_matches) > 0:
                        guess = pair
                        potential_num = len(pair[1].potential_matches)
                    # if this is the only potential match for the contestants then potential_num can't get lower
                    if potential_num == 1:
                        break

        self.check_pair(guess)
        return self.comp_solve(week, solve)  

    def set_smart_pairs(self, num_pairs):
        """ creates pairs so that they are more likely to be potential matches """

        contestant_copy = self.unmatched[:]
        pairs = []

        pairs_made = 0

        for index in range(num_pairs):

            if len(contestant_copy[0].potential_matches) > 0:
                for match in contestant_copy[0].potential_matches:

                    # pair has been made
                    if match in contestant_copy:
                        pairs.append((contestant_copy[0], match))
                        contestant_copy.remove(match)
                        contestant_copy.pop(0)
                        pairs_made += 1
                        break
        
        # randomizes remaining pairs
        pairs.extend(self.set_pairs(num_pairs - pairs_made, contestant_copy))

        return pairs

    def smart_solve(self, week = 0):
        """ Pairs are randomly set, but guesses are selected based on potential matches """
        return self.comp_solve(week, self.set_smart_pairs)

    def auto_solve(self, week = 0):
        """ Pairs are randomly set, but guesses are selected based on potential matches """
        return self.comp_solve(week)

class Histogram:
    """ Displays data as a histogram """

    def create(datasets):
        """ creates a histogram that compares the different datasets in one graph """
        
        # color for a given method
        current_color = 0

        # cycles through the data for each method
        for data in datasets:

            # creates histogram
            plt.hist(data[0], label = data[1], alpha = .60, bins = [5*x for x in range(30)])
            # creates median line
            plt.axvline(np.median(data[0]), linestyle = "dashed", alpha = .75, color = "C" + str(current_color))
            current_color += 1 # changes color for next set of data
            
        # labels the medians
        plt.text(np.median(datasets[0][0]) + 2, 290, np.median(datasets[0][0]), alpha = .75, color = "k")
        plt.text(np.median(datasets[1][0]) + 2, 290, np.median(datasets[1][0]), alpha = .75, color = "k")
        plt.text(np.median(datasets[2][0]) - 13, 290, np.median(datasets[2][0]), alpha = .75, color = "k")

        # labels the graph and its axes
        plt.title("Comparison of Various Algorithms To Solve the Game")
        plt.xlabel("Number of Weeks To Solve the Game")
        plt.ylabel("Frequency Out of 1000 Trials")

        # creates a legend
        plt.legend(loc="upper right")

        plt.show()

if __name__ == "__main__":
    # checks that random_solve takes a lot longer than auto_solve

    solving_methods = [Game.auto_solve, Game.random_solve, Game.smart_solve]

    data_dict = {Game.auto_solve: [], Game.random_solve: [], Game.smart_solve: []}

    # cycles through each method
    for method in solving_methods:

        for i in range(1000):

            names = ["Bob", "John", "Mary", "Rick", "Emma", "Ana", "Harry", "Meredith",
                         "Perry", "Rita", "Derek", "Paula", "Arthur", "Peter", "Lina", "Samantha"]
            game = Game(names)

            weeks = method(game)

            data_dict[method].append(weeks)
        
    # displays results as a histogram
    auto_data = (data_dict[Game.auto_solve], "Auto Solve")
    random_data = (data_dict[Game.random_solve], "Random Solve")
    smart_data = (data_dict[Game.smart_solve], "Smart Solve")

    Histogram.create([auto_data, random_data, smart_data])