import tkinter as tk
from game_backend import *

class Graphics:
    """ Handles all of the graphics for the game """

    def __init__(self):
        """ starts the game """

        self.restart()
        
    def restart(self):
        """ starts the game from scratch """

        # names of the contestants
        names = ["Bob", "John", "Mary", "Rick", "Emma", "Ana", "Harry", "Meredith",
                 "Perry", "Rita", "Derek", "Paula", "Arthur", "Peter", "Lina", "Samantha"]
        self.game = Game(names)

        self.game_info = {}
        self.game_info["week"] = 0

        self.week = 0

        self.display_title()

    def check(self, pair):
        """ Checks the chosen pair to see if they are a perfect match """

        if self.game.check_pair(pair):
        
            self.clear_screen()

            if len(self.game.correct_guesses) == 8:
                # Player won the game
                self.end_game()
                return
            else:
                # Lets the player know their guess was right
                announcement = tk.Label(frame, font = "Arial", text="That was a perfect match!")
        else:

            self.clear_screen()
        
            # Lets the player know that their guess was wrong
            announcement = tk.Label(frame, font = "Arial", text= "Sorry, that was not a match.")
        announcement.grid(column = 0, sticky = "n")
        self.next_week()

    def clear_screen(self):
        """ wipes the screen clear, deleting all of widgets """

        for widgets in frame.winfo_children():
                widgets.destroy()

    def make_button(self, pair):
        """ creates a button for each pair """

        button = tk.Button(
                frame,
                text = str(pair),
                font = "Arial",
                width = 25,
                height = 2,
                bg = "#609ef0",
                activebackground = "#3c6396",
                highlightcolor = "#3c6396",
                relief = "flat",
                command =lambda : self.check(pair)
                )

        button.grid(column = 0, sticky = "n", pady = 2)

    def next_week(self):
        """ reset the situation for the next week """

        # increments the week number
        self.week += 1

        week_pairs = self.game.set_pairs(8 - len(self.game.correct_guesses))
        self.game.correct_pairs_this_week(week_pairs)

        matches_this_week = len(self.game.correct_pairs)
        correct_pairs = tk.Label(frame, font = "Arial", text="During Week " + str(self.week) + ", there were " + str(matches_this_week) + " correct matches")
        correct_pairs.grid(column = 0, sticky = "n")

        # creates a button for each pair
        for pair in week_pairs:
            self.make_button(pair)

        # type in a contestestant name and hit search to see their bad and potential matches
        info_direction = tk.Label(frame, font = "Arial", text= "Type a name to get more information about them")
        info_direction.grid(row = 3, column = 1, sticky = "n")

        info_seeker = tk.Entry(frame, font = "Arial", bg = "#d4e4ff")
        search_btn = tk.Button(frame, font = "Arial", text = "Search", bg = "#609ef0", relief = "flat", width = 25,
                               height = 2, command = lambda : self.display_contestant_info(info_seeker.get()))

        search_btn.grid(row = 4, column = 1, sticky = "n")
        info_seeker.grid(row = 5, column = 1, sticky = "n")

        # button that reveals all of the perfect pairs
        show_perfect = tk.Button(frame, font = "Arial", text = "Show Perfect Pairs", bg = "#609ef0",
                                 width = 25, height = 2, relief = "flat", command = self.show_perfect_pairs)
        show_perfect.grid(row = 6, column = 1, sticky = "n")

    def display_contestant_info(self, contestant):
        """ displays the list of bad matches and potential matches for a given contestant """

        for person in self.game.unmatched:
            if person.name == contestant:

                contestant = person

                contestant_info = tk.Label(frame, font = "Arial", wraplength = 300, justify = "center",
                                          text=contestant.name + "\nBad Matches: " + str(contestant.not_matches) +
                                          "\nPotential Matches: " + str(contestant.potential_matches))
                contestant_info.grid(column = 1, sticky = "n")

                break

    def start_game(self):
        """ starts the game for the player """

        self.clear_screen()
        self.next_week()

    def end_game(self):
        """ ends the game and gives the option to start over """

        self.clear_screen()

        final = tk.Label(frame, font = "Arial", text = "Congratulations! After " + str(self.week) + " weeks, you got all of the perfect matches!")
        final.grid(column = 0, sticky = "n")

        title_btn = tk.Button(frame, font = "Arial", text = "Return to Title Screen", bg = "#609ef0",
                              width = 25, height = 2, relief = "flat", command = lambda : self.restart())
        title_btn.grid(column = 0, sticky = "n")

    def display_title(self):
        """ creates the title screen """

        self.clear_screen()

        intro = tk.Label(frame, font = "Arial", text= "Welcome to Are You the One!")
        intro.grid(column = 0, sticky = "n")

        # button for the player to manually play
        start_btn = tk.Button(frame, font = "Arial", text = "Start Game", bg = "#609ef0",
                              width = 25, height = 2, relief = "flat", command = lambda : self.start_game())
        start_btn.grid(column = 0, sticky = "n", pady = 2)

        # the computer tries to pick strategic guesses each week
        auto_btn = tk.Button(frame, font = "Arial", text = "Auto Match", bg = "#609ef0",
                             width = 25, height = 2, relief = "flat", command = lambda : self.auto_solve())
        auto_btn.grid(column = 0, sticky = "n", pady = 2)

        # the computer just picks the first pair each week
        random_btn = tk.Button(frame, font = "Arial", text = "Random Match", bg = "#609ef0",
                               width = 25, height = 2, relief = "flat", command = lambda : self.random_solve())
        random_btn.grid(column = 0, sticky = "n", pady = 2)

        # the computer tries to pick strategic pairs and guesses each week
        smart_btn = tk.Button(frame, font = "Arial", text = "Smart Match", bg = "#609ef0",
                             width = 25, height = 2, relief = "flat", command = lambda : self.smart_solve())
        smart_btn.grid(column = 0, sticky = "n", pady = 2)

    def auto_solve(self):
        """ computer uses the auto solve algorithm to find the matches """

        self.comp_solve(self.game.auto_solve)

    def random_solve(self):
        """ computer uses the random solve algorithm to find the matches """

        self.comp_solve(self.game.random_solve)

    def smart_solve(self):
        """ computer uses the smart solve algorithm to find the matches """

        self.comp_solve(self.game.smart_solve)

    def comp_solve(self, method):
        """ computer uses different algorithms to find the matches """

        self.clear_screen()

        solved = tk.Label(frame, font = "Arial", text= "Computer got all matches during Week " + str(method()))
        solved.grid(column = 0, sticky = "n")

        title_btn = tk.Button(frame, font = "Arial", text = "Return to Title Screen", bg = "#609ef0",
                              width = 25, height = 2, relief = "flat", command = lambda : self.restart())
        title_btn.grid(column = 0, sticky = "n")


    def show_perfect_pairs(self):
        """ reveals the perfect pairs """

        perfect = tk.Label(frame, font = "Arial", wraplength = 300, text = str(self.game.perfect_pairs))
        perfect.grid(column = 1, sticky = "n")
 
        
if __name__ == "__main__":

    window = tk.Tk()
    window.geometry("5000x1000")

    info = tk.Frame(window)
    info.pack()

    frame = tk.Frame(window)
    frame.pack()

    graphics = Graphics()

    window.mainloop()
