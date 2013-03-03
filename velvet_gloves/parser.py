import ply.yacc as yacc
from .lexer import tokens

def p_concept(p):
    '''Concept : RefinesOpt CONCEPT ConceptName ConceptBasesOpt ConceptBody'''
    p[0] = [p[1], p[3], p[4], p[5]]

def p_refines_opt(p):
    '''RefinesOpt : REFINES
                  | empty
    '''
    p[0] = p[1]

def p_conceptbases_opt(p):
    '''ConceptBasesOpt : ':' ConceptBases
                       | empty
    '''
    if len(p) == 3:
        p[0] = p[2]
    else:
        p[0] = []

def p_conceptbases(p):
    '''ConceptBases : ConceptBases ',' ID
                    | ID
    '''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

def p_conceptname(p):
    '''ConceptName : ID'''
    p[0] = p[1]

def p_conceptbody(p):
    '''ConceptBody : DefinitionBlock
    '''
    p[0] = p[1]

def p_definitionblock(p):
    """DefinitionBlock : LCURLY Definitions RCURLY
                       | LCURLY RCURLY
    """
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = []

def p_definitions(p):
    '''Definitions : Definitions Definition
                   | Definition
    '''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_definition(p):
    '''Definition : Feature
                  | FeatureGroup
    '''
    #              | Constraint
    #'''
                  #| Instance
                  #| Attribute
    p[0] = p[1]

def p_feature(p):
    '''Feature : MandatoryFlagOpt AbstractFlagOpt FEATURE FeatureName FeatureBody
    '''
    modifiers = [x for x in (p[1], p[2]) if x]
    p[0] = ('feature', p[4], modifiers, p[5])

def p_mandatoryflag_opt(p):
    '''MandatoryFlagOpt : MANDATORY
                        | empty
    '''
    p[0] = p[1]

def p_abstractflag_opt(p):
    '''AbstractFlagOpt : ABSTRACT
                       | empty
    '''
    p[0] = p[1]

def p_featurename(p):
    '''FeatureName : FeatureName "." ID
                   | ID
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_featurebody(p):
    '''FeatureBody : FeatureDef
                   | FeatureGroup
                   | ";"
    '''
    p[0] = [] if p[1] == ";" else p[1]

def p_featuredef(p):
    '''FeatureDef : DefinitionBlock
    '''
    p[0] = p[1]

def p_featuregroup(p):
    '''FeatureGroup : GroupType LCURLY GroupChilds RCURLY
    '''
    p[0] = (p[1], p[3])

def p_grouptype(p):
    '''GroupType : SOMEOF
                 | ONEOF
    '''
    p[0] = p[1]

def p_groupchilds(p):
    '''GroupChilds : GroupChilds Feature
                   | Feature
    '''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]


def p_empty(p):
    'empty :'
    p[0] = None

def p_error(p):
    raise Exception("Syntax error in input!", p)
    if p is None:
        print 'Reached end of file!'

parser = yacc.yacc()

def parse(inp):
    res = parser.parse(inp)
    if res is None:
        raise Exception('expecting token but reached EOF!')
    return res
