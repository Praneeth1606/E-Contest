# !/usr/bin/env python3
import random
import sys

class Program:
    # Dic: string->list
    rules = None
    # String
    state = None

    debug = False

    def __init__(self):
        pass

    # Parse code to determine rules and initial state
    def load(self, code):
        self.rules = {}
        self.state = ""
        lines = code.split("\n")
        # If we are adding rules or adding initial state
        adding_rules = True

        for line in lines:
            if adding_rules:
                if "::=" in line:
                    if line.replace(" ", "").replace("\t", "") == "::=":
                        adding_rules = False
                    else:
                        # Add new rule
                        lh = line[0:line.find("::=")]
                        rh = line[line.find("::=")+3::]
                        if lh not in self.rules:
                            self.rules[lh] = [rh]
                        else:
                            self.rules[lh].append(rh)
            else:
                if self.state!="" or line!="":
                    if self.state!="":
                        self.state+="\n"
                    self.state+=line

    def run(self):
        # Just keep stepping through code until we can't
        if self.debug:
            print(self.state);
        while self.step():
            if self.debug:
                print(self.state);

    # Select usable rule and trigger it to change the state
    # Return True if rule was used
    # False elsewise
    def step(self):
        if self.rules is None or self.state is None:
            raise Exception("Program not initialized")

        # First select which rules we can use
        rule_keys = []
        for r in self.rules:
            if r in self.state:
                rule_keys.append(r);
        if len(rule_keys) == 0:
            return False

        # Pick a random rule
        rkey = random.choice(rule_keys);
        rval = random.choice(self.rules[rkey]);

        # Get random location
        locations = set([])
        for i in range(len(self.state)):
            loc = self.state[i::].find(rkey)+i
            if loc-i != -1:
                locations.add(loc)
        loc = random.choice(list(locations))

        # And replace 
        # If it begins with a tilde, though, just output
        if len(rval)>0 and rval[0] == "~":
            sys.stdout.write(rval[1::])
            sys.stdout.flush()
            rval = ""
        elif rval == ":::":
        # ":::" replace with user input
            rval = input()

        self.state = self.state[0:loc]+rval+self.state[loc+len(rkey)::]

        return True

def test():
    p = Program()
    p.load("""_::=~Hello World
    ::=
_""")
    assert(p.rules["_"][0] == "~Hello World")
    assert(len(p.rules["_"]) == 1)
    assert(len(p.rules) == 1)
    assert(p.state == "_")

if __name__=="__main__":
    usage = f"Usage: {sys.argv[0]} [-d] file"
    p = Program()

    # Parse arguments
    if len(sys.argv)<2:
        print(usage)
        exit(1)
    fname = None
    if len(sys.argv)>2:
        fname = sys.argv[2]
        if(sys.argv[1] == "-d"):
            p.debug = True
    else:
        fname = sys.argv[1]


    with open(fname, "r") as fp:
        p.load(fp.read())
        p.run()
