import unittest


class TestLexer(unittest.TestCase):

    def test_smoketest(self):
        from velvet_gloves.lexer import lexer
        self.assertTrue(bool(lexer))

    def tokenize(self, instr):
        self.lexer.input(instr)
        while True:
            tok = self.lexer.token()
            if not tok: break
            yield tok

    @property
    def lexer(self):
        from velvet_gloves.lexer import lexer
        return lexer

    def test_lexer(self):
        self.lexer.input('')
        self.assertFalse(self.lexer.token())
        self.lexer.input('concept')
        self.assertEquals('CONCEPT', self.lexer.token().type)


class TestParser(unittest.TestCase):

    def test_smoketest(self):
        from velvet_gloves.parser import parse
        self.assertTrue(bool(parse), 'Parser exists')

    def parse(self, instr, **kws):
        from velvet_gloves.parser import parse
        return parse(instr, **kws)

    def test_empty(self):
        self.assertRaises(Exception, self.parse, '')

    def test_minimal_concept(self):
        ast = self.parse('''
        concept test {}
        ''')
        self.assertEquals(
            [None, 'test', [], []],
            ast
        )

    def test_refines_concept(self):
        ast = self.parse('''
        refines concept test {}
        ''')
        self.assertEquals(
            ['refines', 'test', [], []],
            ast
        )

    def test_concept_inheritance(self):
        ast = self.parse('''
        concept sub : base {}
        ''')
        self.assertEquals(
            [None, 'sub', ['base'], []],
            ast
        )

    def test_concept_multiple_inheritance(self):
        ast = self.parse('''
        concept sub : base, base2, base3 {}
        ''')
        self.assertEquals(
            [None, 'sub', ['base', 'base2', 'base3'], []],
            ast
        )

    def test_feature(self):
        ast = self.parse('''
        concept test {
            feature a;
        }
        ''')
        self.assertEquals(
            [None, 'test', [], [
                    ('feature', 'a', [], [])
                ]
            ],
            ast
        )

    def test_mandatory_feature(self):
        ast = self.parse('''
        concept test {
            mandatory feature a;
        }
        ''')
        self.assertEquals(
            [None, 'test', [], [
                    ('feature', 'a', ['mandatory'], [])
                ]
            ],
            ast
        )

    def test_mandatory_feature(self):
        ast = self.parse('''
        concept test {
            mandatory feature a;
        }
        ''')
        self.assertEquals(
            [None, 'test', [], [
                    ('feature', 'a', ['mandatory'], [])
                ]
            ],
            ast
        )

    def test_abstract_feature(self):
        ast = self.parse('''
        concept test {
            abstract feature a;
        }
        ''')
        self.assertEquals(
            [None, 'test', [], [
                    ('feature', 'a', ['abstract'], [])
                ]
            ],
            ast
        )

    def test_mandatory_abstract_feature(self):
        ast = self.parse('''
        concept test {
            mandatory abstract feature a;
        }
        ''')
        self.assertEquals(
            [None, 'test', [], [
                    ('feature', 'a', ['mandatory', 'abstract'], [])
                ]
            ],
            ast
        )

    def test_featuredef(self):
        ast = self.parse('''
        concept test {
            feature a {}
        }
        ''')
        self.assertEquals(
            [None, 'test', [], [
                    ('feature', 'a', [], [])
                ]
            ],
            ast
        )

    def test_featuredef_subfeature(self):
        ast = self.parse('''
        concept test {
            feature a {
                feature b;
            }
        }
        ''')
        self.assertEquals(
            [None, 'test', [], [
                    ('feature', 'a', [], [
                        ('feature', 'b', [], [])
                    ])
                ]
            ],
            ast
        )

    def test_featuregroup_oneof(self):
        ast = self.parse('''
        concept test {
            feature a oneof {
                feature b;
            }
        }
        ''')
        self.assertEquals(
            [None, 'test', [], [
                    ('feature', 'a', [], ('oneof', [
                        ('feature', 'b', [], [])
                    ]))
                ]
            ],
            ast
        )

    def test_featuregroup_someof(self):
        ast = self.parse('''
        concept test {
            feature a someof {
                mandatory feature b;
                feature c;
            }
        }
        ''')
        self.assertEquals(
            [None, 'test', [], [
                    ('feature', 'a', [], ('someof', [
                        ('feature', 'b', ['mandatory'], []),
                        ('feature', 'c', [], []),
                    ]))
                ]
            ],
            ast
        )

if __name__ == '__main__':
    import sys
    result = unittest.main()
    retval = 0 if result.wasSuccessful() else 1
    sys.exit(retval)
