from parsing.model.config import Config


class Parser:
    def __init__(self, grammar):
        self.grammar = grammar
        self.output_file = "files\out1.txt"
        file = open(self.output_file, 'w')
        file.write("")
        file.close()

    def write_all_data(self, config):
        with open(self.output_file, 'a') as file:
            file.write(
                f'state: {str(config.state)} index: {str(config.pos)}\n'
                f'WS: {str(config.working_stack)}\n'
                f'IS: {str(config.input_stack)}\n')

    def write_message(self, message):
        with open(self.output_file, 'a') as file:
            file.write(message + "\n")

    def print_working(self, config):
        print("Working stack:", config.working_stack)
        self.write_message("Working stack: " + str(config.working_stack))

    def print_production_string(self, config):
        prod_str = []
        for i in config.working_stack:
            if type(i) == tuple:
                prod_str.append(i)
        print("Production String: ", prod_str)

    def expand(self, config):
        """
        WHEN: head of input stack is a non terminal
        (q, i, alpha, A beta) ⊢ (q, i, alpha A1, gamma1 beta)
        """
        if config.input_stack:
            self.write_message("///EXPAND///")
            nonterminal = config.input_stack.pop(0)
            config.working_stack.append((nonterminal, 0))
            new_production = self.grammar.get_productions_for_nonterminal(nonterminal)
            config.input_stack = new_production[0] + config.input_stack

    def advance(self, config):
        """
        WHEN: head of input stack is a terminal = current symbol from input
        (q, i, alpha, a_i beta) ⊢ (q, i+1, alpha a_i, beta)
        """
        if config.input_stack:
            self.write_message("///ADVANCE///")
            terminal = config.input_stack.pop(0)
            config.working_stack.append(terminal)
            config.pos += 1

    def momentary_insuccess(self, config):
        """
        WHEN: head of input stack is a terminal ≠ current symbol from input
        (q,i, alpha, ai beta) ⊢ (b,i, alpha, ai beta)
        """
        self.write_message("///MOMENTARY INSUCCESS///")
        config.state = 'b'

    def back(self, config):
        """
        When: head of working stack is a terminal
        (b, i, alpha a, beta) ⊢ (b, i-1, alpha, a beta)
        """
        if config.working_stack:
            self.write_message("///BACK///")
            new_elem = config.working_stack.pop()
            config.input_stack = [new_elem] + config.input_stack
            config.pos -= 1

    def success(self, config):
        """
        (q, n+1, alpha, eps) ⊢ (f,n+1, alpha, eps)
        """
        self.write_message("///SUCCESS///")
        config.state = 'f'

    def another_try(self, config):
        self.write_message("///ANOTHER TRY///")
        last = config.working_stack.pop()  # (nonterminal, index)
        nonterminal = last[0]
        index = last[1]
        if index + 1 < len(self.grammar.get_productions_for_nonterminal(nonterminal)):
            config.state = "q"
            new_tuple = (nonterminal, index + 1)
            config.working_stack.append(new_tuple)
            # change production on top input
            length_last_production = len(
                self.grammar.get_productions_for_nonterminal(nonterminal)[index])  # how many to delete
            # delete last production from input
            config.input_stack = config.input_stack[length_last_production:]
            # put new production in input
            next_production = self.grammar.get_productions_for_nonterminal(nonterminal)[index + 1]
            config.input_stack = next_production + config.input_stack
        elif config.pos == 0 and nonterminal == self.grammar.start:
            config.state = "e"
        else:  # go back
            # change production on top input
            length_last_production = len(self.grammar.get_productions_for_nonterminal(nonterminal)[index])
            # delete last production from input
            config.input_stack = config.input_stack[length_last_production:]
            config.input_stack = [nonterminal] + config.input_stack

    def recursive_descent(self, sequence):
        config = Config(self.grammar.start)
        while (config.state != 'f') and (config.state != 'e'):
            self.write_all_data(config)
            if config.state == 'q':
                if len(config.input_stack) == 0 and config.pos == len(sequence):
                    self.success(config)
                elif len(config.input_stack) == 0:
                    self.momentary_insuccess(config)
                elif config.input_stack[0] in self.grammar.get_nonterminals():
                    self.expand(config)
                elif config.pos < len(sequence) and config.input_stack[0] == sequence[config.pos]:
                    self.advance(config)
                else:
                    self.momentary_insuccess(config)
            elif config.state == 'b':
                if config.working_stack[-1] in self.grammar.get_terminals():
                    self.back(config)
                else:
                    self.another_try(config)
        message = "message"
        if config.state == 'e':
            message = "Invalid sequence"
        elif config.state == 'f':
            message = "Sequence is accepted!"

        else:
            print("What?")
        print(message)
        self.write_message(message)
        self.print_working(config)
        self.print_production_string(config)

    # def another_try(self, config):
    #     """
    #     WHEN: head of working stack is a nonterminal
    #     (b,i, alpha Aj, yj beta) ⊢
    #         (q,i, alpha Aj+1, yj+1 beta) , if ∃ A → yj+1
    #         (b,i, alpha, A beta), otherwise with the exception
    #         (e,i, alpha,beta), if i=1, A =S, ERROR
    #     """
    #     nonterminal = config.working_stack[0][0]
    #     last_production_index = config.working_stack[0][1]
    #     config.working_stack.pop()
    #     last_production = self.grammar.productions[nonterminal][last_production_index]
    #     len_last_production = len(last_production)
    #     next_production = self.get_next_production(last_production, self.grammar.productions[nonterminal])
    #     if next_production:
    #         config.state = State.NORMAL
    #         config.working_stack.append((nonterminal, last_production_index + 1))
    #         next_production = next_production[0]
    #         config.input_stack = next_production + config.input_stack[len_last_production:]
    #     elif config.pos == 0 and nonterminal == self.grammar.start:
    #         config.state = State.ERROR
    #     else:
    #         config.input_stack = [nonterminal] + config.input_stack[len_last_production:]

    # def recursive_descent(self, sequence):
    #     config = Config(self.grammar.start)
    #     print(self.grammar.start)
    #     while (config.state != State.FINAL) and (config.state != State.ERROR):
    #         if config.state == State.NORMAL:
    #             if len(config.input_stack) == 0 and config.pos == len(sequence):
    #                 self.success(config)
    #             elif isinstance(config.input_stack[0], str) and config.input_stack[0] in self.grammar.get_nonterminals():
    #                 self.expand(config)
    #             elif config.input_stack[0] == sequence[0]:
    #                 self.advance(config)
    #             else:
    #                 self.momentary_insuccess(config)
    #         elif config.state == State.BACK:
    #             if len(config.working_stack) > 0:
    #                 # if isinstance(config.working_stack[0], str) and config.working_stack[0] in self.grammar.get_terminals():
    #                 for x in self.grammar.get_terminals():
    #                     if x == config.working_stack[0]:
    #                         self.back(config)
    #                     else:
    #                         self.another_try(config)
    #             config.working_stack.pop()
    #             # else:
    #             #     config.state = 'f'
    #
    #     if config.state == State.ERROR:
    #         print("Error")
    #     else:
    #         print("Sequence accepted")

    # def get_next_production(self, prod, productions):
    #     for i in range(len(productions)):
    #         if prod == productions[i] and i + 1 < len(productions):
    #             return productions[i + 1]
    #     return None
