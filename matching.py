# Grace Keane
# Graph Theory
# BSc in Computing in Software Development
# Matching to strings

class State:
    # Every state has 0, 1 or 2 edges from it
    edges = []

    # Label for the arrows. None means epsilon
    label = None

    def __init__(self, label=None, edges=[]):
        self.edges = edges
        self.label = label

class Fragment:
    # Start state of NFA fragment
    start = None
    # Accept state of NFA fragment
    accept = None

    # Constructor
    def __init__(self, start, accept):
        self.start = start
        self.accept = accept

def shunt(infix):
    infix = list(infix)[::-1]

    # Operator stack
    opers = []

    # Output list
    postfix = []

    # Operator precidence * - . - |
    prec = {'*': 100, '.': 80, '|': 60, ')': 40, '(': 20}

    # Loop through the input one character at a time
    while infix:
        # Pop a character from the list
        c = infix.pop() # Removes the last element in infix as a list & returns whatever is poped off

        if c == '(':
            # Push an open bracket to the stack
            opers.append(c)
        elif c == ')':
            # Pop operators stack until open bracket is found
            while opers[-1] != '(':
                postfix.append(opers.pop())

            # Remove open bracket
            opers.pop()

        elif c in prec:
            # Push the operator stack until you find an open bracket
            while opers and  prec[c] < prec[opers[-1]]:
                # Push c to the operator stack with higher precidence to the output
                postfix.append(opers.pop())
            # Push c to the operator stack
            opers.append(c)
        else:
            # Typically we just push the character to the output
            postfix.append(c)

    # Pop all operators to the output
    while opers:
        postfix.append(opers.pop())

    # Convert output list to string
    return ''.join(postfix)


def compile(infix):
    postfix = shunt(infix)
    postfix = list(postfix)[::-1]

    nfa_stack = []

    while postfix:
        # Pop a character from postfix
        c = postfix.pop()
        if c == '.':
            # Pop two fragments off the stack
            frag1 = nfa_stack.pop()
            frag2 = nfa_stack.pop()
            # Point frag2 accept state at frag1 start state
            frag2.accept.edges.append(frag1.start)
            # Create new instance of Fragment to represent the new NFA
            newfrag = Fragment(frag2.start, frag1.accept)
        elif c == '|':
            # Pop two fragments off the stack
            frag1 = nfa_stack.pop()
            frag2 = nfa_stack.pop()
            # Create new start and accept states
            accept = State()
            start = State (edges=[frag2.start, frag1.start])
            # Point the old accept state at the new accept state
            frag1.accept.edges.append(accept)
            frag2.accept.edges.append(accept)
            # Create new instance of the fragment
            newfrag = Fragment(start, accept)
        elif c == '*':
            # Pop a single fragment off the stack
            frag = nfa_stack.pop()
            accept = State()
            start = State(edges=[frag.start, accept])
            # Point the arrows
            frag.accept.edges = ([frag.start, accept])
            # Create new instance of the fragment
            newfrag = Fragment(start, accept)
        else:
            accept = State()
            start = State(label=c, edges=[accept])
            # Create new instance of the fragment
            newfrag = Fragment(start, accept)
        # Push new nfa to the stack
        nfa_stack.append(newfrag)

    # The NFA stack should have exactly one NFA on it
    return nfa_stack.pop()
#--------------------------

# Add a state to a set and follow all of the e arrows
def followes(state, current):
    # Only do something when we haven't already seen the state
    if state not in current:
    # Put the state itself into current
        current.add(state)
        # See whether state is labeled by e (epsilon)
        # Epsilon = empty string
        if state.label is None:
            # Loop through the states pointed by this state
            for x in state.edges:
                # Follow all of their epsilons too
                followes(x, current)

def match(regex, s):
    # This function will return true if the regular expression
    # regex fully matches the string s. It returns false otherwise

    # Compile the regular expression into an NFA
    nfa = compile(regex)
    
    # Try to match the regular expression to the string s
    # The current set of states
    current = set()
    # Add the first state and follow all epsilon arrows
    followes = (nfa.start, current)
    # The previous set of states
    previous = set()

    # Loop through characters in s
    for c in s:
        # Keep track of where you were
        previous = current
        # Create a new empty set for states we're about to be in
        current = set()
        # Loop through the previous states
        for state in previous:
            # Only follow arrows not labeled e(epsilon) 
            if state.label is not None:
                # If the label of the state is equal to the character we've read
                if state.label == c:
                    # Add the state at the end of the arrow to current
                    followes(state.edges[0], current)
                    
    # Ask the NFA if it matches the string s
    return nfa.accept in current

print(match("a.b|b*", "xbbbbbbbbbbb"))






