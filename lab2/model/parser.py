# from model.config import State, Config
#
#
# class Parser:
#     def __init__(self, grammar):
#         self.grammar = grammar
#
#     def expand(self, config):
#         nonterminal = config.input_stack[0]
#         config.pos += 1
#
#     def advance(self, config):
#         terminal = config.input_stack[0]
#         config.working_stack.append(terminal)
#
#     def momentary_insuccess(self, config):
#         config.type = State.BACK
#
#     def back(self, config):
#         terminal = config.working_stack[0]
#         config.pos -= 1
#         config.type = State.BACK
#
#     def another_try(self, config):
#         nonterminal = config.working_stack[0]
#
#     def success(self, config):
#         config.type = State.FINAL
#
#
#     def rd_algo(self, grammar, seq):
#         config = Config(self.grammar.start)
#         while config.type != State.FINAL and config.type != State.ERROR:
#             pass
#
from model import config
from model.config import Config, State


class Parser:
    def __init__(self, grammar):
        self.grammar = grammar

    def expand(self, config):
        """
        WHEN: head of input stack is a non terminal
        (q, i, alpha, A beta) ⊢ (q, i, alpha A1, gamma1 beta)
        """
        if config.input_stack:
            nonterminal = config.input_stack.pop(0)
            config.working_stack.append((nonterminal, 0))
            new_production = self.grammar.get_productions_for_nonterminal(nonterminal)
            config.input_stack.append(new_production[0])

    def advance(self, config):
        """
        WHEN: head of input stack is a terminal = current symbol from input
        (q, i, alpha, a_i beta) ⊢ (q, i+1, alpha a_i, beta)
        """
        if config.input_stack:
            terminal = config.input_stack.pop(0)
            config.working_stack.append(terminal)
            config.pos += 1

    def momentary_insuccess(self, config):
        """
        WHEN: head of input stack is a terminal ≠ current symbol from input
        (q,i, alpha, ai beta) ⊢ (b,i, alpha, ai beta)
        """
        config.type = State.BACK

    def back(self, config):
        """
        When: head of working stack is a terminal
        (b, i, alpha a, beta) ⊢ (b, i-1, alpha, a beta)
        """
        if config.working_stack:
            new_elem = config.working_stack.pop(0)
            config.input_stack = [new_elem] + config.input_stack
            config.pos -= 1

    def success(self, config):
        """
        (q, n+1, alpha, eps) ⊢ (f,n+1, alpha, eps)
        """
        config.type = State.FINAL

    def another_try(self, config):
        """
        WHEN: head of working stack is a nonterminal
        (b,i, alpha Aj, yj beta) ⊢
            (q,i, alpha Aj+1, yj+1 beta) , if ∃ A → yj+1
            (b,i, alpha, A beta), otherwise with the exception
            (e,i, alpha,beta), if i=1, A =S, ERROR
        """
        # if config.working_stack:
        #     nonterminal = config.working_stack.pop(0)

        # print(config)
        nonterminal = config.working_stack[0][0]
        last_production_index = config.working_stack[0][1]
        config.working_stack.pop()
        last_production = self.grammar.productions[nonterminal][last_production_index]
        len_last_production = len(last_production)
        next_production = self.get_next_production(last_production, self.grammar.productions[nonterminal])
        if next_production:
            config.type = State.NORMAL
            config.working_stack.append((nonterminal, last_production_index + 1))
            next_production = next_production[0]
            print(next_production)
            config.input_stack = next_production + config.input_stack[len_last_production:]
        elif config.pos == 0 and nonterminal == self.grammar.start:
            config.type = State.ERROR
        else:
            config.input_stack = [nonterminal] + config.input_stack[len_last_production:]
        # print(config)


    def recursive_descent(self, sequence):
        config = Config(self.grammar.start)

        # print(config.input_stack[0], sequence[0])

        while config.type != State.FINAL and config.type != State.ERROR:
            if config.type == State.NORMAL:
                # print(config.pos)
                # print(config.input_stack)
                if config.pos == len(sequence) and len(config.input_stack) == 0:
                    self.success(config)
                elif isinstance(config.input_stack[0], str) and config.input_stack[0] in self.grammar.get_nonterminals():
                    self.expand(config)
                elif config.input_stack[0] == sequence[0]:
                    # print("AAA")
                    self.advance(config)
                else:
                    self.momentary_insuccess(config)
            elif config.type == State.BACK:
                # print(config.working_stack, type(self.grammar.get_terminals()))
                if len(config.working_stack) > 0:
                    # if config.working_stack[0] in self.grammar.get_terminals():
                    for x in self.grammar.get_terminals():
                        if x == config.working_stack[0]:
                            self.back(config)
                        else:
                            self.another_try(config)
                # else:
                #     config.type = 'f'

        if config.type == State.ERROR:
            print("Error")
        else:
            print("Sequence accepted")
        # self.parse_tree(config.working_stack)

    def get_next_production(self, prod, productions):
        for i in range(len(productions)):
            if prod == productions[i] and i + 1 < len(productions):
                return productions[i + 1]
        return None
