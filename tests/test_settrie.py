#!/usr/bin/env python3
# coding: utf8
"""
Unit tests for module PySetTrie (see settrie.py).

Author: Márton Miháltz 
https://sites.google.com/site/mmihaltz/
"""

import unittest
from settrie import SetTrie, SetTrieMap, SetTrieMultiMap


class TestSetTrie(unittest.TestCase):
  """
  UnitTest for SetTrie class
  """

  def setUp(self):
    self.t = SetTrie([{1, 3}, {1, 3, 5}, {1, 4}, {1, 2, 4}, {2, 4}, {2, 3, 5}])

  def test_print(self):
    expected = """None
  1
    2
      4#
    3#
      5#
    4#
  2
    3
      5#
    4#
"""
    from io import StringIO
    outp = StringIO()
    self.t.pprint(stream=outp)
    self.assertEqual(outp.getvalue(), expected)

  def test_iter(self):
    a = []
    for s in self.t:
      a.append(s)
    self.assertEqual(a, [{1, 2, 4}, {1, 3}, {1, 3, 5}, {1, 4}, {2, 3, 5}, {2, 4}])

  def test_iter2(self):
    it = iter(self.t)
    for s in it:
      pass
    self.assertRaises(StopIteration, it.__next__)

  def test_iter3(self):
    t2 = SetTrie()
    it = iter(t2)
    self.assertRaises(StopIteration, it.__next__)

  def test_aslist(self):
    self.assertEqual(list(self.t), [{1, 2, 4}, {1, 3}, {1, 3, 5}, {1, 4}, {2, 3, 5}, {2, 4}])
    
  def test_str(self):
    self.assertEqual(str(self.t), "[{1, 2, 4}, {1, 3}, {1, 3, 5}, {1, 4}, {2, 3, 5}, {2, 4}]")

  def test_contains(self):
    self.assertTrue(self.t.__contains__( {1, 3} ))
    self.assertFalse(self.t.__contains__( {1} ))
    self.assertTrue(self.t.__contains__( {1, 3, 5} ))
    self.assertFalse(self.t.__contains__( {1, 3, 5, 7} ))

  def test_in(self):
    self.assertTrue({1, 3} in self.t)
    self.assertFalse({1} in self.t)
    self.assertTrue({1, 3, 5} in self.t)
    self.assertFalse({1, 3, 5, 7} in self.t)
    
  def test_hassuperset(self):
    self.assertTrue(self.t.hassuperset({3, 5}))
    self.assertFalse(self.t.hassuperset({6}))
    self.assertTrue(self.t.hassuperset({1, 2, 4}))
    self.assertFalse(self.t.hassuperset({2, 4, 5} ))
    
  def test_supersets(self):
    self.assertEqual(list(self.t.supersets({3, 5})), [{1, 3, 5}, {2, 3, 5}])
    self.assertEqual(list(self.t.supersets({1, 4})), [{1, 2, 4}, {1, 4}])
    self.assertEqual(list(self.t.supersets({1, 3, 5})),  [{1, 3, 5}])
    self.assertEqual(list(self.t.supersets({2})),  [{1, 2, 4}, {2, 3, 5}, {2, 4}])
    self.assertEqual(list(self.t.supersets({1})),  [{1, 2, 4}, {1, 3}, {1, 3, 5}, {1, 4}])
    self.assertEqual(list(self.t.supersets({1, 2, 5})),  [])
    self.assertEqual(list(self.t.supersets({1, 2, 4, 5})),  [])
    self.assertEqual(list(self.t.supersets({6})),  [])

  def test_hassubset(self):
    self.assertTrue(self.t.hassubset({1, 2, 3}))
    self.assertTrue(self.t.hassubset({2, 3, 4, 5}))
    self.assertTrue(self.t.hassubset({1, 4}))
    self.assertTrue(self.t.hassubset({2, 3, 5}))
    self.assertFalse(self.t.hassubset({3, 4, 5}))
    self.assertFalse(self.t.hassubset({6, 7, 8, 9, 1000}))

  def test_subsets(self):
    self.assertEqual(list(self.t.subsets({1, 2, 4, 11})), [{1, 2, 4}, {1, 4}, {2, 4}])
    self.assertEqual(list(self.t.subsets({1, 2, 4})), [{1, 2, 4}, {1, 4}, {2, 4}])
    self.assertEqual(list(self.t.subsets({1, 2})), [])
    self.assertEqual(list(self.t.subsets({1, 2, 3, 4, 5})), [{1, 2, 4}, {1, 3}, {1, 3, 5}, {1, 4}, {2, 3, 5}, {2, 4}])
    self.assertEqual(list(self.t.subsets({0, 1, 3, 5})), [{1, 3}, {1, 3, 5}])
    self.assertEqual(list(self.t.subsets({1, 2, 5})), [])
    self.assertEqual(list(self.t.subsets({1, 4})), [{1, 4}]) # :)   
    self.assertEqual(list(self.t.subsets({1, 3, 5})), [{1, 3}, {1, 3, 5}])
    self.assertEqual(list(self.t.subsets({1, 3, 5, 111})), [{1, 3}, {1, 3, 5}])
    self.assertEqual(list(self.t.subsets({1, 4, 8})), [{1, 4}])
    self.assertEqual(list(self.t.subsets({2, 3, 4, 5})), [{2, 3, 5}, {2, 4}])
    self.assertEqual(list(self.t.subsets({2, 3, 5, 6})), [{2, 3, 5}])


class TestSetTrieMap(unittest.TestCase):
  """
  UnitTest for SetTrieMap class
  """

  def setUp(self):
    self.t = SetTrieMap([({1, 3}, 'A'), ({1, 3, 5}, 'B'), ({1, 4}, 'C'),
                         ({1, 2, 4}, 'D'), ({2, 4}, 'E'), ({2, 3, 5}, 'F')])
    #self.t.pprint()

  def test_print(self):
    expected = """None
  1
    2
      4: 'D'
    3: 'A'
      5: 'B'
    4: 'C'
  2
    3
      5: 'F'
    4: 'E'
"""
    from io import StringIO
    outp = StringIO()
    self.t.pprint(stream=outp)
    self.assertEqual(outp.getvalue(), expected)
  
  def test_contains(self):
    self.assertTrue(self.t.__contains__( {1, 3} ))
    self.assertFalse(self.t.__contains__( {1} ))
    self.assertTrue(self.t.__contains__( {1, 3, 5} ))
    self.assertFalse(self.t.__contains__( {1, 3, 5, 7} ))

  def test_in(self):
    self.assertTrue({1, 3} in self.t)
    self.assertFalse({1} in self.t)
    self.assertTrue({1, 3, 5} in self.t)
    self.assertFalse({1, 3, 5, 7} in self.t)

  def test_get(self):
    self.assertEqual(self.t.get({1, 3}), 'A')
    self.assertEqual(self.t.get({1, 3, 5}), 'B')
    self.assertEqual(self.t.get({1, 4}), 'C')
    self.assertEqual(self.t.get({1, 2, 4}), 'D')
    self.assertEqual(self.t.get({2, 4}), 'E')
    self.assertEqual(self.t.get({2, 3, 5}), 'F')
    self.assertEqual(self.t.get({1, 2, 3}), None)
    self.assertEqual(self.t.get({100, 101, 102}, 0xDEADBEEF), 0xDEADBEEF)
    self.assertEqual(self.t.get({}), None)
  
  def test_assign(self):
    self.assertEqual(self.t.get({1, 3}), 'A')
    self.t[{1, 3}] = 'AAA'
    self.assertEqual(self.t.get({1, 3}), 'AAA')
    self.assertEqual(self.t.get({100, 200}), None)
    self.t[{100, 200}] = 'FOO'
    self.assertEqual(self.t.get({100, 200}), 'FOO')
    self.setUp()

  def test_hassuperset(self):
    self.assertTrue(self.t.hassuperset({3, 5}))
    self.assertFalse(self.t.hassuperset({6}))
    self.assertTrue(self.t.hassuperset({1, 2, 4}))
    self.assertFalse(self.t.hassuperset({2, 4, 5} ))
  
  def test_supersets(self):
    self.assertEqual(list(self.t.supersets({3, 5})), [({1, 3, 5}, 'B'), ({2, 3, 5}, 'F')])
    self.assertEqual(list(self.t.supersets({1})), [({1, 2, 4}, 'D'), ({1, 3}, 'A'), ({1, 3, 5}, 'B'), ({1, 4}, 'C')])
    self.assertEqual(list(self.t.supersets({1, 2, 5})), [])
    self.assertEqual(list(self.t.supersets({3, 5}, mode='keys')), [{1, 3, 5}, {2, 3, 5}])
    self.assertEqual(list(self.t.supersets({1}, mode='keys')), [{1, 2, 4}, {1, 3}, {1, 3, 5}, {1, 4}])
    self.assertEqual(list(self.t.supersets({1, 2, 5}, mode='keys')), [])
    self.assertEqual(list(self.t.supersets({3, 5}, mode='values')), ['B', 'F'])
    self.assertEqual(list(self.t.supersets({1}, mode='values')), ['D', 'A', 'B', 'C'])
    self.assertEqual(list(self.t.supersets({1, 2, 5}, mode='values')), [])
    
  def test_hassubset(self):
    self.assertTrue(self.t.hassubset({1, 2, 3}))
    self.assertTrue(self.t.hassubset({2, 3, 4, 5}))
    self.assertTrue(self.t.hassubset({1, 4}))
    self.assertTrue(self.t.hassubset({2, 3, 5}))
    self.assertFalse(self.t.hassubset({3, 4, 5}))
    self.assertFalse(self.t.hassubset({6, 7, 8, 9, 1000}))

  def test_subsets(self):
    self.assertEqual(list(self.t.subsets({1, 2, 4, 11})), [({1, 2, 4}, 'D'), ({1, 4}, 'C'), ({2, 4}, 'E')])
    self.assertEqual(list(self.t.subsets({1, 2, 4})), [({1, 2, 4}, 'D'), ({1, 4}, 'C'), ({2, 4}, 'E')])
    self.assertEqual(list(self.t.subsets({1, 2})), [])
    self.assertEqual(list(self.t.subsets({1, 2, 3, 4, 5})), [({1, 2, 4}, 'D'),
      ({1, 3}, 'A'),
      ({1, 3, 5}, 'B'),
      ({1, 4}, 'C'),
      ({2, 3, 5}, 'F'),
      ({2, 4}, 'E')] )
    self.assertEqual(list(self.t.subsets({0, 1, 3, 5})), [({1, 3}, 'A'), ({1, 3, 5}, 'B')])
    self.assertEqual(list(self.t.subsets({1, 2, 5})), [])
    self.assertEqual(list(self.t.subsets({1, 2, 4, 11}, mode='keys')), [{1, 2, 4}, {1, 4}, {2, 4}])
    self.assertEqual(list(self.t.subsets({1, 2, 4}, mode='keys')), [{1, 2, 4}, {1, 4}, {2, 4}])
    self.assertEqual(list(self.t.subsets({1, 2}, mode='keys')), [])
    self.assertEqual(list(self.t.subsets({1, 2, 3, 4, 5}, mode='keys')), [{1, 2, 4}, {1, 3}, {1, 3, 5}, {1, 4}, {2, 3, 5}, {2, 4}])
    self.assertEqual(list(self.t.subsets({0, 1, 3, 5}, mode='keys')), [{1, 3}, {1, 3, 5}])
    self.assertEqual(list(self.t.subsets({1, 2, 5}, mode='keys')), [])
    self.assertEqual(list(self.t.subsets({1, 2, 4, 11}, mode='values')), ['D', 'C', 'E'])
    self.assertEqual(list(self.t.subsets({1, 2, 4}, mode='values')), ['D', 'C', 'E'])
    self.assertEqual(list(self.t.subsets({1, 2}, mode='values')), [])
    self.assertEqual(list(self.t.subsets({1, 2, 3, 4, 5}, mode='values')), ['D', 'A', 'B', 'C', 'F', 'E'])
    self.assertEqual(list(self.t.subsets({0, 1, 3, 5}, mode='values')), ['A', 'B'])
    self.assertEqual(list(self.t.subsets({1, 2, 5}, mode='values')), [])
    self.assertEqual(list(self.t.subsets({1, 4})), [({1, 4}, 'C')])
    self.assertEqual(list(self.t.subsets({1, 3, 5})), [({1, 3}, 'A'), ({1, 3, 5}, 'B')])
    self.assertEqual(list(self.t.subsets({1, 3, 5, 111})), [({1, 3}, 'A'), ({1, 3, 5}, 'B')])
    self.assertEqual(list(self.t.subsets({1, 4, 8})), [({1, 4}, 'C')])
    self.assertEqual(list(self.t.subsets({2, 3, 4, 5})), [({2, 3, 5}, 'F'), ({2, 4}, 'E')])
    self.assertEqual(list(self.t.subsets({2, 3, 5, 6})), [({2, 3, 5}, 'F')])    
    
    

  def test_iters(self):
    self.assertEqual(list(self.t), 
      [{1, 2, 4}, {1, 3}, {1, 3, 5}, {1, 4}, {2, 3, 5}, {2, 4}] )
    self.assertEqual(list(self.t.keys()), [{1, 2, 4}, {1, 3}, {1, 3, 5}, {1, 4}, {2, 3, 5}, {2, 4}] )
    self.assertEqual(list(self.t.values()), ['D', 'A', 'B', 'C', 'F', 'E'] )
    self.assertEqual(list(self.t.__iter__()), list(self.t.keys()))


class TestSetTrieMultiMap(unittest.TestCase):
  """
  UnitTest for SetTrieMultiMap class
  """

  def setUp(self):
    self.t = SetTrieMultiMap([({1, 3}, 'A'), ({1, 3}, 'AA'), ({1, 3, 5}, 'B'), ({1, 4}, 'C'), ({1, 4}, 'CC'),
                         ({1, 2, 4}, 'D'), ({1, 2, 4}, 'DD'), ({2, 4}, 'E'), ({2, 3, 5}, 'F'),
                         ({2, 3, 5}, 'FF'), ({2, 3, 5}, 'FFF')])
    
  def test_aslist(self):
    self.assertEqual(list(self.t), 
      [{1, 2, 4}, {1, 3}, {1, 3, 5},
       {1, 4}, {2, 3, 5}, {2, 4}] )

  def test_get(self):
    self.assertEqual(self.t.get({1, 3}), ['A', 'AA'])
    self.assertEqual(self.t.get({1, 2, 4}), ['D', 'DD'])
    self.assertEqual(self.t.get({1, 3, 5}), ['B'])
    self.assertEqual(self.t.get({2, 3, 5}), ['F', 'FF', 'FFF'])
    self.assertEqual(self.t.get({2, 4}), ['E'])
    self.assertEqual(self.t.get({1, 3, 4}), None)
    self.assertEqual(self.t.get({44}, []), [])
    
  def test_hassuperset(self):
    self.assertTrue(self.t.hassuperset({3, 5}))
    self.assertFalse(self.t.hassuperset({6}))
    self.assertTrue(self.t.hassuperset({1, 2, 4}))
    self.assertFalse(self.t.hassuperset({2, 4, 5} ))

  def test_supersets(self):
    self.assertEqual(list(self.t.supersets({3, 5})), [({1, 3, 5}, 'B'), ({2, 3, 5}, 'F'), ({2, 3, 5}, 'FF'), ({2, 3, 5}, 'FFF')])
    self.assertEqual(list(self.t.supersets({3, 5}, mode='values')), ['B', 'F', 'FF', 'FFF'])
    self.assertEqual(list(self.t.supersets({3, 5}, mode='keys')), [{1, 3, 5}, {2, 3, 5}])
    self.assertEqual(list(self.t.supersets({1})), [({1, 2, 4}, 'D'), ({1, 2, 4}, 'DD'), ({1, 3}, 'A'), 
                                             ({1, 3}, 'AA'), ({1, 3, 5}, 'B'), ({1, 4}, 'C'), ({1, 4}, 'CC')])
    self.assertEqual(list(self.t.supersets({1}, mode='keys')), [{1, 2, 4}, {1, 3}, {1, 3, 5}, {1, 4}])
    self.assertEqual(list(self.t.supersets({1}, mode='values')), ['D', 'DD', 'A', 'AA', 'B', 'C', 'CC'])
    self.assertEqual(list(self.t.supersets({1, 2, 5})), [])
    self.assertEqual(list(self.t.supersets({1, 2, 5}, mode='keys')), [])
    self.assertEqual(list(self.t.supersets({1, 2, 5}, mode='values')), [])

  def test_hassubset(self):
    self.assertTrue(self.t.hassubset({1, 2, 3}))
    self.assertTrue(self.t.hassubset({2, 3, 4, 5}))
    self.assertTrue(self.t.hassubset({1, 4}))
    self.assertTrue(self.t.hassubset({2, 3, 5}))
    self.assertFalse(self.t.hassubset({3, 4, 5}))
    self.assertFalse(self.t.hassubset({6, 7, 8, 9, 1000}))

  def test_subsets(self):
    self.assertEqual(list(self.t.subsets({1, 2, 4, 11})), [({1, 2, 4}, 'D'), ({1, 2, 4}, 'DD'), ({1, 4}, 'C'), 
                                                     ({1, 4}, 'CC'), ({2, 4}, 'E')] )
    self.assertEqual(list(self.t.subsets({1, 2, 4, 11}, mode='keys')), [{1, 2, 4}, {1, 4}, {2, 4}])
    self.assertEqual(list(self.t.subsets({1, 2, 4, 11}, mode='values')), ['D', 'DD', 'C', 'CC', 'E'])
    self.assertEqual(list(self.t.subsets({1, 2, 4})), [({1, 2, 4}, 'D'), ({1, 2, 4}, 'DD'), ({1, 4}, 'C'), ({1, 4}, 'CC'),
                                                 ({2, 4}, 'E')])
    self.assertEqual(list(self.t.subsets({1, 2, 4}, mode='keys')), [{1, 2, 4}, {1, 4}, {2, 4}])
    self.assertEqual(list(self.t.subsets({1, 2, 4}, mode='values')), ['D', 'DD', 'C', 'CC', 'E'])
    self.assertEqual(list(self.t.subsets({1, 2})), [])
    self.assertEqual(list(self.t.subsets({1, 2}, mode='keys')), [])
    self.assertEqual(list(self.t.subsets({1, 2}, mode='values')), [])
    self.assertEqual(list(self.t.subsets({1, 2, 3, 4, 5})), 
      [({1, 2, 4}, 'D'), ({1, 2, 4}, 'DD'), ({1, 3}, 'A'), ({1, 3}, 'AA'), ({1, 3, 5}, 'B'), 
       ({1, 4}, 'C'), ({1, 4}, 'CC'), ({2, 3, 5}, 'F'), ({2, 3, 5}, 'FF'), ({2, 3, 5}, 'FFF'), ({2, 4}, 'E')] )
    self.assertEqual(list(self.t.subsets({1, 2, 3, 4, 5})), list(self.t.items()))
    self.assertEqual(list(self.t.subsets({1, 2, 3, 4, 5}, mode='keys')), list(self.t.keys()))
    self.assertEqual(list(self.t.subsets({1, 2, 3, 4, 5}, mode='keys')), [{1, 2, 4}, {1, 3}, {1, 3, 5}, {1, 4}, {2, 3, 5}, {2, 4}])
    self.assertEqual(list(self.t.subsets({1, 2, 3, 4, 5}, mode='values')), 
      ['D', 'DD', 'A', 'AA', 'B', 'C', 'CC', 'F', 'FF', 'FFF', 'E'])
    self.assertEqual(list(self.t.subsets({1, 2, 3, 4, 5}, mode='values')), list(self.t.values()))
    self.assertEqual(list(self.t.subsets({0, 1, 3, 5})), [({1, 3}, 'A'), ({1, 3}, 'AA'), ({1, 3, 5}, 'B')])
    self.assertEqual(list(self.t.subsets({0, 1, 3, 5}, mode='keys')), [{1, 3}, {1, 3, 5}])
    self.assertEqual(list(self.t.subsets({0, 1, 3, 5}, mode='values')), ['A', 'AA', 'B'])
    self.assertEqual(list(self.t.subsets({1, 2, 5})), [])
    self.assertEqual(list(self.t.subsets({1, 2, 5}, mode='keys')), [])
    self.assertEqual(list(self.t.subsets({1, 2, 5}, mode='values')), [])
    self.assertEqual(list(self.t.subsets({1, 4})), [({1, 4}, 'C'), ({1, 4}, 'CC')])
    self.assertEqual(list(self.t.subsets({1, 3, 5})), [({1, 3}, 'A'), ({1, 3}, 'AA'), ({1, 3, 5}, 'B')])
    self.assertEqual(list(self.t.subsets({1, 3, 5, 111})), [({1, 3}, 'A'), ({1, 3}, 'AA'), ({1, 3, 5}, 'B')])
    self.assertEqual(list(self.t.subsets({1, 4, 8})), [({1, 4}, 'C'), ({1, 4}, 'CC')])
    self.assertEqual(list(self.t.subsets({2, 3, 4, 5})), [({2, 3, 5}, 'F'), ({2, 3, 5}, 'FF'), ({2, 3, 5}, 'FFF'), ({2, 4}, 'E')])
    self.assertEqual(list(self.t.subsets({2, 3, 5, 6})), [({2, 3, 5}, 'F'), ({2, 3, 5}, 'FF'), ({2, 3, 5}, 'FFF')])     

# - - - - - - -

# If module is executed from command line, perform tests:
if __name__ == "__main__":
  unittest.main(verbosity=2)
