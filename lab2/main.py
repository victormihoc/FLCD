# pif-operators, separators, keywords etc have value -1 meaning they dont appear in symtbl
# in symtbl nu se mai dauga identifieru in pif da
from model.finite_automata import FA
from model.grammar import Grammar
from model.parser import Parser
from model.pif import PIF
from model.scanner import Scanner
from model.symboltable import SymbolTable

if __name__ == '__main__':
    # sym_tbl = SymbolTable()
    # # sym_tbl.put("a", 1)
    # # sym_tbl.put('b', 3)
    # # sym_tbl.put('a', 3)
    # # print(sym_tbl.size)
    # # print(sym_tbl['a'])
    # pif = PIF()
    #
    # scanner = Scanner("files/token.in", "files/p3.txt")
    # scanner.scan()

    # fa = FA()
    # fa.start()
    # print(fa.is_sequence_accepted("p q r s"))

    gramm = Grammar()
#    gramm.run()
    parser = Parser(gramm)
    parser.recursive_descent('ac')
