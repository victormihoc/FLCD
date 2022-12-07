def display_menu():
    print("\n1 - Display the set of states")
    print("2 - Display the alphabet")
    print("3 - Display the transitions")
    print("4 - Display the initial state")
    print("5 - Display the final state")
    print("6 - Check sequence\n")


class FA:
    def __init__(self):
        self.states = []
        self.alphabet = []
        self.transitions = []
        self.initial_state = 'p'
        self.final_states = 's'
        self.fileFA = open("files/FA.in", "r")
        self.read_file()
        self.cmds = {"1": self.display_states, '2': self.display_alphabet, '3': self.display_transitions,
                     '4': self.display_initial, '5': self.display_final, '6': self.check}

    def display_states(self):
        print("Set of states: \n")
        for state in self.states:
            print(state)

    def display_alphabet(self):
        print("The alphabet: \n")
        for letter in self.alphabet:
            print(letter)

    def display_transitions(self):
        print("The transitions: \n")
        for tran in self.transitions:
            print(tran)

    def display_initial(self):
        print("Initial state: \n")
        for state in self.initial_state:
            print(state)

    def display_final(self):
        print("Final states: \n")
        for state in self.final_states:
            print(state)

    def check(self):
        sequence = input("Check for a sequence: ")
        print(self.is_sequence_accepted(sequence))

    def read_file(self):
        self.states = self.fileFA.readline().rstrip().split(" ")
        self.alphabet = self.fileFA.readline().rstrip().split(" ")
        self.transitions = self.fileFA.readline().rstrip().split(";")
        # self.initial_state = self.fileFA.readline().rstrip().split(" ")
        # self.final_states.append(self.fileFA.readline().rstrip().split(" "))

    def is_deterministic(self):
        visited = []
        for el in self.transitions:
            if [el[0], el[1]] not in visited:
                visited.append([el[0], el[1]])
            return True
        return False

    def is_sequence_accepted(self, sequence):
        curr = self.initial_state
        i = 0
        if not self.is_deterministic():
            return False
        for char in sequence[1:]:
            if curr == self.transitions[i][0] and char == self.transitions[i][2]:
                curr = self.transitions[i][2]
                i += 1
            else:
                return False
        return curr in self.final_states

    def start(self):

        display_menu()

        while True:
            cmd = input().strip().lower()
            if cmd == 'exit':
                return
            if cmd not in self.cmds:
                print("\nBad command")
            try:
                self.cmds[cmd]()
            except ValueError as ve:
                print("error - " + str(ve))
