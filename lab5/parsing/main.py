from model.grammar import Grammar
from model.parser import Parser

if __name__ == '__main__':
    gramm = Grammar()
    # gramm.run()
    parser = Parser(gramm)
    parser.recursive_descent('acbc')
