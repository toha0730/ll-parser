import sys
import grammar

class LL:
    def __init__(self, parse_input, rec_mode, grammar):
        # Add '$' add the end of the parse input to be able to parse using the parser
        self.parse_input = parse_input + '$'
        self.rec_mode = rec_mode
        self.terminals = grammar.terminals(grammar)
        self.table = grammar.table(grammar)

    def parse(self):
        # Checks if there are any invalid symbols within the parse input
        for char in parse_input:
            if char not in ll.terminals:
                return 'ERROR_INVALID_SYMBOL'

        # Parse stack appended with $ and L -> stack = 'L$'
        stack = []
        stack.append('$')
        stack.append('L')
        accepted = []

        # The priority in which the suggestions are ordered in
        # Terminals are considered first priority since it will not add anymore variables to the stack
        # Technically, the print function has the most number of changes however, in terms of moving between variables,
        # the parentheses add a terminal AND a variable. Thus placing it at last priority.
        first_priority = ['a', 'b', 'c', 'd', '0', '1', '2', '3']
        second_priority = ['+', '-', '*', 'p', 'r', 'i', 'n', 't', 'f']
        third_priority = [')', '(']

        while True:
            expected = [] # Quick way to keep track of what input the parse table was expecting
            T = stack[-1] # T assigned to top of stack
            c = ll.parse_input[0] # c assigned to first character of parse input
            print('{input:{fill}{align}{width}}{stack}'.format(
                input=ll.parse_input,
                fill=' ',
                align='<',
                width=35,
                stack=''.join(stack[::-1]))
            ) # Formatting to print out trace of execution in a neat manner

            if T == '$' and c[0] == '$': # self explanatory
                return 'ACCEPTED {}'.format(''.join(accepted))
            elif T in ll.terminals or T == '$': # if T is a defined terminal or is '$'
                if T == c: # consume input + pop stack if T == c
                    stack.pop()
                    accepted.append(c)
                    ll.parse_input = ll.parse_input[1:]
                else:
                    # Documentation for recovery mode
                    if ll.rec_mode:
                        print('Error: got {0}, but expected {{{1}}}'.format(c, T))
                        print('Description: Terminal value of parse input does not match given value for top of stack')
                        while True: # loop until an input has been fixed, from which it will rerun the parse
                            parse_len = len(ll.parse_input)
                            stack_len = len(stack)
                            # Band-aid method to select between adding and deleting an input by artificially adjusting
                            # the lengths of the parse input or parse stack
                            if parse_len == stack_len:
                                fudge = input("Option: add / delete ")
                                if fudge == 'add':
                                    stack_len += 1
                                else:
                                    parse_len += 1
                            if parse_len < stack_len: # if the parse input is less than what is in the stack, add input
                                fix = input('Add input from expected? ')
                                if fix not in T:
                                    print('Following input will not repair parsed input. Please try a given option.')
                                else:
                                    ll.parse_input = fix + ll.parse_input
                                    break
                            else: # otherwise delete from input to balance out
                                fix = input('Delete character from parse input? ')
                                if fix not in ll.parse_input:
                                    print('Following character not found in parse input. Please try again.')
                                else:
                                    ll.parse_input = ll.parse_input[1:]
                                    break
                    else:
                        return 'REJECTED'
            elif (stack[-1], c) in ll.table: # check if corresponding rule of [T,c] exists within parse table
                rule = ll.table.get((stack[-1], c))[::-1] # add rule to stack in reverse order
                stack.pop()
                for char in rule:
                    stack.append(char)
            else:
                if ll.rec_mode:
                    for rule in ll.table:
                        if (rule[0] == T): # grabs all expected terminals that had T as its variable
                            expected.append(rule[1])
                    expected_str = ', '.join(expected)
                    print('Error: got {0}, but expected {{{1}}}'.format(c, expected_str))
                    print('Description: Top of stack not $ or a terminal and rule where P[T, parse_input] not found in '
                          'parse table')
                    if T == 'B' or T == 'R': # check to see if an epsilon can be passed
                        print('Suggestions in order for minimal number of changes: {0}'.format(
                            [terminal for terminal in third_priority if terminal in expected] +
                            [terminal for terminal in first_priority if terminal in expected] +
                            [terminal for terminal in second_priority if terminal in expected])
                        )  # slightly modified priority defined above, print suggestions in order of priority
                    else:
                        print('Suggestions in order for minimal number of changes: {0}'.format(
                            [terminal for terminal in first_priority if terminal in expected] +
                            [terminal for terminal in second_priority if terminal in expected] +
                            [terminal for terminal in third_priority if terminal in expected] )
                        ) # Using the priority defined above, print suggestions in order of priority

                    while True:
                        parse_len = len(ll.parse_input)
                        stack_len = len(stack)
                        # Snippet from above
                        if parse_len == stack_len:
                            fudge = input("Option: add / delete ")
                            if fudge == 'add':
                                stack_len += 1
                            else:
                                parse_len += 1

                        if parse_len < stack_len: # snippet from above
                            fix = input('Add input from suggestions? ')
                            if fix not in expected:
                                print('Following input will not repair parsed input. Please try a given option.')
                            else:
                                ll.parse_input = fix + ll.parse_input
                                break
                        else: # snippet from above
                            fix = input('Delete character from parse input? ')
                            if fix not in ll.parse_input:
                                print('Following character not found in parse input. Please try again.')
                            else:
                                ll.parse_input = ll.parse_input[1:]
                                break
                else:
                    return 'REJECTED'

if __name__ == '__main__':
    parse_input = ''
    rec_mode = False

    # Checks if recovery mode has been enabled
    if len(sys.argv) == 3 and sys.argv[2] == 'error':
        rec_mode = True

    infile = sys.argv[1]
    with open(infile, 'r') as file:
        parse_input = parse_input.join(file.read().split())

    print('Input string to test: {0}'.format(parse_input))
    print('Recovery mode: {0}'.format(rec_mode))

    # Load grammar from grammar.py
    grammar = grammar.Grammar
    ll = LL(parse_input, rec_mode, grammar)
    print(ll.parse())