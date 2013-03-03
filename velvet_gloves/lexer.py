import ply.lex as lex

literals = (':', ',', ';', '.', '!', '=')

reserved_words = (
   'refines',
   'concept',
   'mandatory',
   'abstract',
   'feature',
   'someof',
   'oneof',
   'constraint'
)

reserved = dict([(x, x.upper()) for x in reserved_words])

tokens = [
   'LCURLY',
   'RCURLY',
   'LPARENS',
   'RPARENS',
   'ID',
   'AND',
   'OR',
   'XOR',
   'IMPL',
   'EQUIV',
] + reserved.values()

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

t_LPARENS = r'\('
t_RPARENS = r'\)'
t_LCURLY = r'\{'
t_RCURLY = r'\}'

t_AND = r'&&'
t_OR = r'\|\|'
t_XOR = r'xor'
t_IMPL = r'->'
t_EQUIV = r'<->'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore  = ' \t'

def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

lexer = lex.lex()
