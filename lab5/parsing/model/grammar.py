# recursive descendant algo
#    2 stacks, 6 actions

def display_menu():
    print("\n1 - Display the set of nonterminals")
    print("2 - Display the set of terminals")
    print("3 - Display the set of productions")
    print("4 - Display the set of productions for a nonterminal")


class Grammar:
    def __init__(self):
        self.nonterminals = []
        self.terminals = []
        self.start = 'x'
        self.raw_prod = []
        self.productions = {}
        self.fileG = open("files/g1.txt", "r")
        self.read_grammar_from_file()
        self.cmds = {"1": self.print_nonterminals,
                     '2': self.print_terminals,
                     '3': self.print_productions,
                     '4': self.print_productions_for_nonterminal}

    def read_grammar_from_file(self):
        lines = self.fileG.read().splitlines()

        self.nonterminals = lines[0].split(" ")
        self.terminals = lines[1].split(" ")
        self.start = lines[2]
        self.raw_prod = lines[3:]

        for raw_prod in self.raw_prod:
            st, dr = raw_prod.strip().split("->")
            self.productions[st] = []
            for p in dr.split("|"):
                self.productions[st].append(p.split(" "))

    def print_nonterminals(self):
        for nonterminal in self.nonterminals:
            print(nonterminal)

    def get_nonterminals(self):
        return self.nonterminals

    def print_terminals(self):
        for terminal in self.terminals:
            print(terminal)

    def get_terminals(self):
        return self.terminals

    def print_productions(self):
        for production in self.prod:
            print(production)

    def print_productions_for_nonterminal(self):
        nonterminal = input("nonterminal:")
        print(self.productions[nonterminal])

    def get_productions_for_nonterminal(self, nonterminal):
        return self.productions[nonterminal]

    def run(self):

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
