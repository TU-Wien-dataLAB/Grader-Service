#!/usr/bin/env python3 

__doc__ = """Simple scheme-like evaluator for git.

The code borrows heavily from the excellent articles by Peter Norvig on 
(How to Write a (Lisp) Interpreter (in Python)) https://norvig.com/lispy.html

The purpose of this module is to provide a simple API that can be used to
calculate filesystem paths to git repositories and git commands. The 'lookup'
function can be used to evaluate s-expressions.
"""

__all__ = ["lookup"]

Symbol = str  # A git service symbol is implemented as a Python str
List   = list

def lookup(data):
    """Evaluate an s-expression and return its value.

    Examples:
    
    Specify Filesystem Path to Git repository

        (repo <rtype> <args>)

    >>> lookup('(repo lxuser l102 a1 johnny)')       
    '/home/johnny/l102/a1'
    
    >>> lookup('(repo lxsource jaas20 1 amccartn)')
    '/home/amccartn/source/jaas20/1'
    
    >>> lookup('(repo lxrelease jaas20 1 amccartn)') 
    '/home/amccartn/release/jaas20/1'

    >>> lookup('(repo gssource jaas20 1)')
    '/var/lib/grader-service/git/jaas20/1/source'

    >>> lookup('(repo gsrelease jaas20 1)')
    '/var/lib/grader-service/git/jaas20/1/release'

    >>> lookup('(repo gsuser jaas20 1 amccartn)')
    '/var/lib/grader-service/git/jaas20/1/user/amccartn'

    >>> lookup('(repo autograde jaas20 1 ewimmer)')
    '/var/lib/grader-service/git/jaas20/1/autograde/user/ewimmer'

    >>> lookup('(repo feedback jaas20 1 ewimmer)')
    '/var/lib/grader-service/git/jaas20/1/feedback/user/ewimmer'

    >>> lookup('(repo edit jaas20 1 6)')
    '/var/lib/grader-service/git/jaas20/1/edit/6'


    Prepare A Git Command to Run on a repo

        (git <cmd> (repo <rtype> <args>))

    >>> lookup('(prep init (repo gssource jaas20 1))')
    'git init --bare /var/lib/grader-service/git/jaas20/1/source'
    """

    #pudb.set_trace()
    val = eval(parse(data))
    if val is not None:
        return lispstr(val)

############## Definition of repository types 

def gitpath(ctx):
    """Create a repo  object based on context.
    A repo object is 
    """
    if ctx[0] == 'lxuser':
        return LabXUser(*ctx[1:])
    elif ctx[0] in ['lxsource', 'lxrelease']:
        _rtype = ctx[0].strip("lx")
        return LabXSourceRelease(rtype=_rtype, lcode=ctx[1],
                               aid=ctx[2], uname=ctx[3])
    elif ctx[0] in ['gsuser', 'autograde', 'feedback']:
        _rtype = ctx[0].strip("gs")
        return Extended(rtype=_rtype, lcode=ctx[1],
                            aid=ctx[2], uname=ctx[3])
    elif ctx[0] in ['gssource', 'gsrelease']:
        _rtype = ctx[0][2:]
        return SourceRelease(_rtype, lcode=ctx[1], aid=ctx[2])
    elif ctx[0] == 'edit':
        return Edit(lcode=ctx[1], aid=ctx[2], sid=ctx[3])
    else:
        raise SyntaxError('Unknown repo type requested')


###################### Jupyterlab extension 

class GitPath():
    "Represent the  path to directory tree containing all GitPaths"
    def __init__(self, base):
        self.base = base

    def __str__(self):
        return f"{self.base}"

class LabXUser(GitPath):
    "Define path for us er, occurs in the context of a Jupyter Lab Extension" 
    def __init__(self, lcode, aid, uname):
        super().__init__(base="/home")
        self.lcode, self.aid, self.uname = lcode, aid, uname

    def __str__(self):
        return f"{self.base}/{self.uname}/{self.lcode}/{self.aid}"

class LabXSourceRelease(GitPath):
    "Define path for user' s source or release GitPath in the context of lab ext"
    def __init__(self, rtype, lcode, aid, uname):
        super().__init__(base="/home")
        self.rtype, self.lcode, self.aid, self.uname = rtype, lcode, aid, uname 

    def __str__(self):
        return f"{self.base}/{self.uname}/{self.rtype}/{self.lcode}/{self.aid}"

###################### Grader service 

class Grader(GitPath):
    "Represent the path to d irectory tree containing all GitPaths"
    def __init__(self, base="/var/lib/grader-service/git"):
        super().__init__(base)


class SourceRelease(Grader):
    "Represent a type of git GitPath under the grader git tree" 
    def __init__(self, rtype, lcode, aid): 
        super().__init__()
        self.rtype, self.lcode, self.aid = rtype, lcode, aid

    def __str__(self):
        return f"{self.base}/{self.lcode}/{self.aid}/{self.rtype}"

class Extended(Grader):
    "This type is valid for rtype 'autograde', 'feedback' and 'user'"
    def __init__(self, rtype, lcode, aid, uname):
        super().__init__()
        self.rtype, self.lcode, self.aid, self.uname = rtype, lcode, aid, uname

    def __str__(self):
        _base = f"{self.base}/{self.lcode}/{self.aid}/{self.rtype}"
        if self.rtype in ['autograde', 'feedback']:
            rep = f"{_base}/user/{self.uname}"
        elif self.rtype == 'user':
            rep = f"{_base}/{self.uname}"
        else:
            raise ValueError("Unexpected GitPath type")
        return rep

class Edit(Grader):
    "This type is valid only for rtype 'edit'"
    def __init__(self, lcode, aid, sid, rtype='edit'):
        super().__init__()
        self.lcode, self.aid, self.sid, self.rtype = lcode, aid, sid, rtype
    
    def __str__(self):
        return f"{self.base}/{self.lcode}/{self.aid}/{self.rtype}/{self.sid}"

############### Global Environment

def standard_env():
    "An envir onment with some standard procedures for our git service."
    env = {}
    env.update({
        'checkout': lambda x: f' checkout {x}',    # go_to_commit
        'commit': lambda x: f' add -A &&  commit --allow-empty -m {x}',
        'fetch_all': ' fetch --all',
        'prep' : lambda *x: 'git {0} {1}'.format(*x),
        'init': 'init --bare',
        'push': lambda x, force="": f' push {x} {force}',
        'pull': lambda *x: ' pull {}'.format(*x),
        'remote?': lambda *x: ' ls-remote --exit-code {0} {1}'.format(*x),
        'switch_branch': lambda x: f" fetch --all &&  checkout {x}",
        'authuser?':  None,
        'list':       lambda *x: list(x), 
        'list?':      lambda x: isinstance(x,list), 
        'released?':  None,
        })
    return env


global_env = standard_env()

############ Parsing: parse, tokenize, and read_from_tokens


def parse(program):
    "Read a git service expression from string."
    return read_from_tokens(tokenize(program))

def tokenize(s):
    "Convert a string into a list of tokens"
    return s.replace('(', ' ( ').replace(')', ' ) ').split()

def read_from_tokens(tokens):
    "Read an expression for a sequence of tokens"
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF while reading')
    token = tokens.pop(0)
    if '(' == token:
        L = []
        while tokens[0] != ')':
            L.append(read_from_tokens(tokens))
        tokens.pop(0) # pop off ')'
        return L
    elif ')' == token:
        raise SyntaxError('unexpected )')
    else:
        return Symbol(token)
    

################### Interaction: A repl 

def repl(prompt='git.service> '):
    while True:
        #pudb.set_trace()
        val = eval(parse(input(prompt)))
        if val is not None:
            print(lispstr(val))

def lispstr(exp):
    "Convert a Python object back into a Lisp-readable string."
    if isinstance(exp, List):
        return '(' + ' '.join(map(lispstr, exp)) + ')' 
    else:
        return str(exp)


################# eval 

def eval(x, env=global_env):
    "Evaluate an expression i n an environment"
    if isinstance(x, Symbol):                 # variable reference
        return env[x]
    elif not isinstance(x, List):             # constant literal
        return x
    elif x[0] == 'repo':                      
        ctx = x[1:]
        return str(gitpath(ctx))
    else:                     
        proc = eval(x[0], env)
        args = [eval(exp, env) for exp in x[1:]]
        return proc(*args)

if __name__ == '__main__':
    repl()
