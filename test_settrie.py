#!/usr/bin/env python3
"""
Unit tests for module PySetTrie (see settrie.py).

Author: Márton Miháltz 
<mmihaltz@gmail.com>
https://sites.google.com/site/mmihaltz/
"""

import unittest
from settrie import SetTrie, SetTrieMap


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
    self.t.printtree(stream=outp)
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
    self.assertEqual(self.t.aslist(), [{1, 2, 4}, {1, 3}, {1, 3, 5}, {1, 4}, {2, 3, 5}, {2, 4}])
    
  def test_str(self):
    self.assertEqual(str(self.t), "[{1, 2, 4}, {1, 3}, {1, 3, 5}, {1, 4}, {2, 3, 5}, {2, 4}]")

  def test_contains(self):
    self.assertTrue(self.t.contains( {1, 3} ))
    self.assertFalse(self.t.contains( {1} ))
    self.assertTrue(self.t.contains( {1, 3, 5} ))
    self.assertFalse(self.t.contains( {1, 3, 5, 7} ))

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
    self.assertEqual(self.t.supersets({3, 5}), [{1, 3, 5}, {2, 3, 5}])
    self.assertEqual(self.t.supersets({1, 4}), [{1, 2, 4}, {1, 4}])
    self.assertEqual(self.t.supersets({1, 3, 5}),  [{1, 3, 5}])
    self.assertEqual(self.t.supersets({2}),  [{1, 2, 4}, {2, 3, 5}, {2, 4}])
    self.assertEqual(self.t.supersets({1}),  [{1, 2, 4}, {1, 3}, {1, 3, 5}, {1, 4}])
    self.assertEqual(self.t.supersets({1, 2, 5}),  [])
    self.assertEqual(self.t.supersets({1, 2, 4, 5}),  [])
    self.assertEqual(self.t.supersets({6}),  [])

  def test_hassubset(self):
    self.assertTrue(self.t.hassubset({1, 2, 3}))
    self.assertTrue(self.t.hassubset({2, 3, 4, 5}))
    self.assertTrue(self.t.hassubset({1, 4}))
    self.assertTrue(self.t.hassubset({2, 3, 5}))
    self.assertFalse(self.t.hassubset({3, 4, 5}))
    self.assertFalse(self.t.hassubset({6, 7, 8, 9, 1000}))

  def test_subsets(self):
    self.assertEqual(self.t.subsets({1, 2, 4, 11}), [{1, 2, 4}, {1, 4}, {2, 4}])
    self.assertEqual(self.t.subsets({1, 2, 4}), [{1, 2, 4}, {1, 4}, {2, 4}])
    self.assertEqual(self.t.subsets({1, 2}), [])
    self.assertEqual(self.t.subsets({1, 2, 3, 4, 5}), [{1, 2, 4}, {1, 3}, {1, 3, 5}, {1, 4}, {2, 3, 5}, {2, 4}])
    self.assertEqual(self.t.subsets({0, 1, 3, 5}), [{1, 3}, {1, 3, 5}])
    self.assertEqual(self.t.subsets({1, 2, 5}), [])


class TestSetTrieMap(unittest.TestCase):
  """
  UnitTest for SetTrie class
  """

  def setUp(self):
    self.t = SetTrieMap([({1, 3}, 'A'), ({1, 3, 5}, 'B'), ({1, 4}, 'C'),
                         ({1, 2, 4}, 'D'), ({2, 4}, 'E'), ({2, 3, 5}, 'F')])
    #self.t.printtree()

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
    self.t.printtree(stream=outp)
    self.assertEqual(outp.getvalue(), expected)
  
  def test_contains(self):
    self.assertTrue(self.t.contains( {1, 3} ))
    self.assertFalse(self.t.contains( {1} ))
    self.assertTrue(self.t.contains( {1, 3, 5} ))
    self.assertFalse(self.t.contains( {1, 3, 5, 7} ))

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
    self.t.assign({1, 3}, 'AAA')
    self.assertEqual(self.t.get({1, 3}), 'AAA')
    self.assertEqual(self.t.get({100, 200}), None)
    self.t.assign({100, 200}, 'FOO')
    self.assertEqual(self.t.get({100, 200}), 'FOO')
    self.setUp()

  def test_hassuperset(self):
    self.assertTrue(self.t.hassuperset({3, 5}))
    self.assertFalse(self.t.hassuperset({6}))
    self.assertTrue(self.t.hassuperset({1, 2, 4}))
    self.assertFalse(self.t.hassuperset({2, 4, 5} ))
  
  def test_supersets(self):
    self.assertEqual(self.t.supersets({3, 5}), [({1, 3, 5}, 'B'), ({2, 3, 5}, 'F')])
    self.assertEqual(self.t.supersets({1}), [({1, 2, 4}, 'D'), ({1, 3}, 'A'), ({1, 3, 5}, 'B'), ({1, 4}, 'C')])
    self.assertEqual(self.t.supersets({1, 2, 5}), [])
    self.assertEqual(self.t.supersets({3, 5}, mode='keys'), [{1, 3, 5}, {2, 3, 5}])
    self.assertEqual(self.t.supersets({1}, mode='keys'), [{1, 2, 4}, {1, 3}, {1, 3, 5}, {1, 4}])
    self.assertEqual(self.t.supersets({1, 2, 5}, mode='keys'), [])
    self.assertEqual(self.t.supersets({3, 5}, mode='values'), ['B', 'F'])
    self.assertEqual(self.t.supersets({1}, mode='values'), ['D', 'A', 'B', 'C'])
    self.assertEqual(self.t.supersets({1, 2, 5}, mode='values'), [])
    
  def test_hassubset(self):
    self.assertTrue(self.t.hassubset({1, 2, 3}))
    self.assertTrue(self.t.hassubset({2, 3, 4, 5}))
    self.assertTrue(self.t.hassubset({1, 4}))
    self.assertTrue(self.t.hassubset({2, 3, 5}))
    self.assertFalse(self.t.hassubset({3, 4, 5}))
    self.assertFalse(self.t.hassubset({6, 7, 8, 9, 1000}))

  def test_subsets(self):
    self.assertEqual(self.t.subsets({1, 2, 4, 11}), [({1, 2, 4}, 'D'), ({1, 4}, 'C'), ({2, 4}, 'E')])
    self.assertEqual(self.t.subsets({1, 2, 4}), [({1, 2, 4}, 'D'), ({1, 4}, 'C'), ({2, 4}, 'E')])
    self.assertEqual(self.t.subsets({1, 2}), [])
    self.assertEqual(self.t.subsets({1, 2, 3, 4, 5}), [({1, 2, 4}, 'D'),
      ({1, 3}, 'A'),
      ({1, 3, 5}, 'B'),
      ({1, 4}, 'C'),
      ({2, 3, 5}, 'F'),
      ({2, 4}, 'E')] )
    self.assertEqual(self.t.subsets({0, 1, 3, 5}), [({1, 3}, 'A'), ({1, 3, 5}, 'B')])
    self.assertEqual(self.t.subsets({1, 2, 5}), [])
    self.assertEqual(self.t.subsets({1, 2, 4, 11}, mode='keys'), [{1, 2, 4}, {1, 4}, {2, 4}])
    self.assertEqual(self.t.subsets({1, 2, 4}, mode='keys'), [{1, 2, 4}, {1, 4}, {2, 4}])
    self.assertEqual(self.t.subsets({1, 2}, mode='keys'), [])
    self.assertEqual(self.t.subsets({1, 2, 3, 4, 5}, mode='keys'), [{1, 2, 4}, {1, 3}, {1, 3, 5}, {1, 4}, {2, 3, 5}, {2, 4}])
    self.assertEqual(self.t.subsets({0, 1, 3, 5}, mode='keys'), [{1, 3}, {1, 3, 5}])
    self.assertEqual(self.t.subsets({1, 2, 5}, mode='keys'), [])
    self.assertEqual(self.t.subsets({1, 2, 4, 11}, mode='values'), ['D', 'C', 'E'])
    self.assertEqual(self.t.subsets({1, 2, 4}, mode='values'), ['D', 'C', 'E'])
    self.assertEqual(self.t.subsets({1, 2}, mode='values'), [])
    self.assertEqual(self.t.subsets({1, 2, 3, 4, 5}, mode='values'), ['D', 'A', 'B', 'C', 'F', 'E'])
    self.assertEqual(self.t.subsets({0, 1, 3, 5}, mode='values'), ['A', 'B'])
    self.assertEqual(self.t.subsets({1, 2, 5}, mode='values'), [])

  def test_iters(self):
    self.assertEqual(self.t.aslist(), 
      [({1, 2, 4}, 'D'), ({1, 3}, 'A'), ({1, 3, 5}, 'B'), ({1, 4}, 'C'), ({2, 3, 5}, 'F'), ({2, 4}, 'E')] )
    self.assertEqual(list(self.t.keys()), [{1, 2, 4}, {1, 3}, {1, 3, 5}, {1, 4}, {2, 3, 5}, {2, 4}] )
    self.assertEqual(list(self.t.values()), ['D', 'A', 'B', 'C', 'F', 'E'] )
    self.assertEqual(list(self.t.__iter__()), list(self.t.keys()))

# - - - - - - -

# If module is executed from command line, perform tests:
if __name__ == "__main__":
  unittest.main(verbosity=2)