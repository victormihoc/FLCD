# recursive descendant algo
#    2 stacks, 6 actions

def display_menu():
    print("\n1 - Display the set of nonterminals")
    print("2 - Display the set of terminals")
    print("3 - Display the set of productions")
    print("4 - Display the set of productions for a nonterminal")
    print("5 - CFG check")
    print("6 - Check sequence\n")

class Grammar:
    def __init__(self):
        self.nonterminals = []
        self.terminals = []
        self.start = 'S'
        self.productions = {}
        #self.productions_for_nonterminal = []
        self.fileG = open("files/g1.txt", "r")
        self.read_grammar_from_file()
        self.cmds = {"1": self.print_nonterminals, '2': self.print_terminals, '3': self.print_productions}

    def read_grammar_from_file(self):
        self.nonterminals = self.fileG.readline().strip().split(" ")
        self.terminals = self.fileG.readline().strip().split(" ")

        for line in self.fileG:

            line = line.strip()
            left, right = line.split('->')
            left = left.strip()
            right = [part.strip() for part in right.split("|")]

            if left in self.productions.keys():
                print("error")

            self.productions[left] = right

    def print_nonterminals(self):
        for nonterminal in self.nonterminals:
            print(nonterminal)

    def print_terminals(self):
        for terminal in self.terminals:
            print(terminal)

    def print_productions(self, nonterminal):
        if not nonterminal:
            for production in self.productions:
                print(production)

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

