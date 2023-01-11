from model.pif import PIF
from model.symboltable import SymbolTable
import re


class Scanner:
    def __init__(self, tokens, program):
        self.symbol_table = SymbolTable()
        self.pif_tbl = PIF()
        self.filename = program
        self.tokens = tokens
        self.pif = open("PIF.out", "w")
        self.st_file = open("ST.out", "w")
        self.separators = []
        self.operators = []
        self.keywords = []

    def get_sym_tbl(self):
        return self.symbol_table.get_table()

    def split_tokens(self, file):
        f = open(file, "r")
        for line in f:
            if line == "space":
                self.separators.append(" ")
            elif line.rstrip() in ["+", "=", "-", "*", "/", "cmp", "like", "[", "]", "=+=", "=-="]:
                self.operators.append(line.rstrip())
            elif line.rstrip() in [".", ",", ";", "\""]:
                self.separators.append(line.rstrip())
            elif line.rstrip() in ["int", "type", "str", "ans", "say", "arr", "loop", "stoploop"]:
                self.keywords.append(line.rstrip())

    def scan(self):
        cnt = 1
        self.split_tokens(self.tokens)
        file = open(self.filename, "r")
        for line in file:

            for word in line.split():

                if word in self.operators or word in self.separators or word in self.keywords:

                    self.pif_tbl.add(word, -1)
                    self.pif.write(word + " -1" + "\n")


                elif re.match('^\w+$', word) and word not in self.symbol_table.get_keys():
                    pos = self.symbol_table.put(word, cnt)
                    cnt += 1
                    if pos == -1:
                        continue
                    self.st_file.write("identifier/constant " + str(pos) + "\n")

                    self.pif_tbl.add(word, pos)
                    self.pif.write(word + " " + str(pos) + "\n")




