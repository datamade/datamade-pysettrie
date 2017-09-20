#!/usr/bin/env python3
# coding: utf-8
"""
Module settrie

Requires Python3

Version 0.1.3
Release date: 2015-05-22

Author: Márton Miháltz
Project home: https://github.com/mmihaltz/pysettrie

See README.md for more information.

Licensed under the GNU LESSER GENERAL PUBLIC LICENSE, Version 3.
See https://www.gnu.org/licenses/lgpl.html
"""

import sys
import sortedcontainers

__version__ = "0.1.3"

class BaseNode(object):
    
    # comparison operators to support rich comparisons, sorting
    # etc. using self.data as key
    def __eq__(self, other): return self.data == other.data
    
    def __ne__(self, other): return self.data != other.data
    
    def __lt__(self, other): return self.data < other.data

    def __le__(self, other): return self.data <= other.data
    
    def __gt__(self, other): return self.data > other.data

    def __ge__(self, other): return self.data >= other.data

class SetTrie(object):
    """Set-trie container of sets for efficient supersets/subsets of a set
       over a set of sets queries.

       Usage:
       ------
       >>> from settrie import SetTrie
       >>> t = SetTrie( [{1, 3}, {1, 2, 3}] )
       >>> t.add( {3, 4, 5} )
       >>> t
       [{1, 2, 3}, {1, 3}, {3, 4, 5}]
       >>> {1, 3} in t
       True
       >>> t.hassuperset( {1, 3} )
       True
       >>> t.supersets( {1, 3} )
       [{1, 2, 3}, {1, 3}]
       >>> t.subsets({1, 2, 3, 5})
       [{1, 2, 3}, {1, 3}]

    """

    class Node(BaseNode):
        """Node object used by SetTrie."""

        def __init__(self, data=None):
            # child nodes a.k.a. children
            self.children = sortedcontainers.SortedList()
            # if True, this is the last element of a set in the
            # set-trie use this to store user data (a set
            # element). Must be a hashable (i.e. hash(data) should
            # work) and comparable/orderable (i.e. data1 < data2
            # should work; see
            # https://wiki.python.org/moin/HowTo/Sorting/) type.
            self.flag_last = False
            self.data = data
            
    def __init__(self, iterable=None):
        """Initialize this set-trie. If iterable is specified, set-trie is
           populated from its items.
        """
        self.root = self.Node()
        if iterable is not None:
            for s in iterable:
                self.add(s)

    def add(self, aset):
        """Add set aset to the container.  aset must be a sortable and
           iterable container type.
        """
        self._add(self.root, iter(sorted(aset)))

    @classmethod
    def _add(cls, node, it):
        """Recursive function used by self.insert().
           node is a SetTrieNode object
           it is an iterator over a sorted set"""
        try:
            data = next(it)
            nextnode = None
            try:
                # find first child with this data
                nextnode = node.children[node.children.index(
                    cls.Node(data))]
            except ValueError:  # not found
                nextnode = cls.Node(data)  # create new node
                node.children.add(nextnode)  # add to children & sort
            cls._add(nextnode, it)  # recurse
        except StopIteration:  # end of set to add
            node.flag_last = True

    def contains(self, aset):
        """Returns True iff this set-trie contains set aset."""
        return self._contains(self.root, iter(sorted(aset)))

    def __contains__(self, aset):
        """Returns True iff this set-trie contains set aset.

           This method definition allows the use of the 'in' operator,
           for example:
           >>> t = SetTrie()
           >>> t.add( {1, 3} )
           >>> {1, 3} in t
           True
        """
        return self.contains(aset)

    @classmethod
    def _contains(cls, node, it):
        """Recursive function used by self.contains()."""
        try:
            data = next(it)
            try:
                # find first child with this data
                matchnode = node.children[node.children.index(
                    cls.Node(data))]
                return cls._contains(matchnode, it)  # recurse
            except ValueError:  # not found
                return False
        except StopIteration:
            return node.flag_last

    def hassuperset(self, aset):
        """Returns True iff there is at least one set in this set-trie that is
           the superset of set aset.
        """
        # TODO: if aset is not a set, convert it to a set first to
        # collapse multiply existing elements
        return self._hassuperset(self.root, list(sorted(aset)), 0)

    @classmethod
    def _hassuperset(cls, node, setarr, idx):
        """Used by hassuperset()."""
        if idx > len(setarr) - 1:
            return True
        found = False
        for child in node.children:
            # don't go to subtrees where current element cannot be
            if child.data > setarr[idx]:
                break
            if child.data == setarr[idx]:
                found = cls._hassuperset(child, setarr, idx + 1)
            else:
                found = cls._hassuperset(child, setarr, idx)
            if found:
                break
        return found

    def itersupersets(self, aset):
        """Return an iterator over all sets in this set-trie that are (proper
           or not proper) supersets of set aset.
        """
        path = []
        return self._itersupersets(self.root, sorted(aset), path)

    @classmethod
    def _itersupersets(cls, node, setarr, path, *args):
        """Used by itersupersets()."""
        path.append(node.data)
        if setarr:
            current = setarr[0]
            for child in node.children:
                if child.data < current:
                    yield from cls._itersupersets(child, setarr,
                                                  path, *args)
                elif child.data == current:
                    yield from cls._itersupersets(child, setarr[1:],
                                                  path, *args)
                else:
                    break
        else:
            if node.flag_last:
                yield from cls._terminate(node, path[1:], *args)

            for child in node.children:
                yield from cls._iter(child, path, *args)

        path.pop()

    def supersets(self, aset):
        """Return a list containing all sets in this set-trie that are
           supersets of set aset.
        """
        return list(self.itersupersets(aset))

    def hassubset(self, aset):
        """Return True iff there is at least one set in this set-trie that is
           the (proper or not proper) subset of set aset.
        """
        return self._hassubset(self.root, list(sorted(aset)), 0)

    @classmethod
    def _hassubset(cls, node, setarr, idx):
        """Used by hassubset()."""
        if node.flag_last:
            return True
        if idx > len(setarr) - 1:
            return False
        found = False
        try:
            c = node.children.index(cls.Node(setarr[idx]))
            found = cls._hassubset(node.children[c], setarr, idx + 1)
        except ValueError:
            pass
        if not found:
            return cls._hassubset(node, setarr, idx + 1)
        else:
            return True

    def itersubsets(self, aset):
        """Return an iterator over all sets in this set-trie that are (proper
           or not proper) subsets of set aset.
        """
        path = []
        return self._itersubsets(self.root, aset, path)

    @classmethod
    def _itersubsets(cls, node, setarr, path, *args):
        """Used by itersubsets()."""
        path.append(node.data)

        if node.flag_last:
            yield from cls._terminate(node, path[1:], *args)
        for child in node.children:
            if child.data in setarr:
                yield from cls._itersubsets(child, setarr, path, *args)

        path.pop()

    def subsets(self, aset):
        """Return a list of sets in this set-trie that are (proper or not
           proper) subsets of set aset.
        """
        return list(self.itersubsets(aset))

    def iter(self):
        """Returns an iterator over the sets stored in this set-trie (with
           pre-order tree traversal).  The sets are returned in sorted
           order with their elements sorted.
        """
        return self.__iter__()

    def __iter__(self):
        """Returns an iterator over the sets stored in this set-trie (with
           pre-order tree traversal).  The sets are returned in sorted
           order with their elements sorted.

           This method definition enables direct iteration over a
           SetTrie, for example:

           >>> t = SetTrie([{1, 2}, {2, 3, 4}])
           >>> for s in t:
           >>>   print(s)
           {1, 2}
           {2, 3, 4}
        """
        path = []
        yield from self._iter(self.root, path)

    @classmethod
    def _iter(cls, node, path, *args):
        """Recursive function used by self.__iter__()."""
        path.append(node.data)
        if node.flag_last:
            yield from cls._terminate(node, path[1:], *args)
        for child in node.children:
            yield from cls._iter(child, path, *args)
        path.pop()

    def aslist(self):
        """Return an array containing all the sets stored in this set-trie.
           The sets are in sorted order with their elements sorted."""
        return list(self)

    def printtree(self, tabchr=' ', tabsize=2, stream=sys.stdout):
        """Print a mirrored 90-degree rotation of the nodes in this trie to
           stream (default: sys.stdout).  Nodes marked as flag_last
           are trailed by the '#' character.  tabchr and tabsize
           determine the indentation: at tree level n, n*tabsize
           tabchar characters will be used.
        """
        self._printtree(self.root, 0, tabchr, tabsize, stream)

    @classmethod
    def _printtree(cls, node, level, tabchr, tabsize, stream):
        """Used by self.printTree(), recursive preorder traverse and printing
           of trie node
        """
        print(str(node.data).rjust(len(repr(node.data)) + level *
                                   tabsize, tabchr) +
              ('#' if node.flag_last else ''),
              file=stream)
        for child in node.children:
            cls._printtree(child, level + 1, tabchr, tabsize, stream)

    def __str__(self):
        """Returns str(self.aslist())."""
        return str(self.aslist())

    def __repr__(self):
        """Returns str(self.aslist())."""
        return str(self.aslist())

    @staticmethod
    def _terminate(node, path):
        yield set(path)


class SetTrieMap(SetTrie):
    """Mapping container for efficient storage of key-value pairs where
      the keys are sets.  Uses efficient trie
      implementation. Supports querying for values associated to
      subsets or supersets of stored key sets.

      Usage:
      ------
      >>> from settrie import SetTrieMap
      >>> m.assign({1,2}, 'A')
      >>> m.assign({1,2,3}, 'B')
      >>> m.assign({2,3,5}, 'C')
      >>> m
      [({1, 2}, 'A'), ({1, 2, 3}, 'B'), ({2, 3, 5}, 'C')]
      >>> m.get( {1,2,3} )
      'B'
      >>> m.get( {1, 2, 3, 4}, 'Nope!')
      'Nope!'
      >>> list(m.keys())
      [{1, 2}, {1, 2, 3}, {2, 3, 5}]
      >>> m.supersets( {1,2} )
      [({1, 2}, 'A'), ({1, 2, 3}, 'B')]
      >>> m.supersets({1, 2}, mode='keys')
      [{1, 2}, {1, 2, 3}]
      >>> m.supersets({1, 2}, mode='values')
      ['A', 'B']
    """

    class Node(BaseNode):
        """Node object used by SetTrieMap. You probably don't need to use it
           from the outside.
        """

        def __init__(self, data=None, value=None):
            # child nodes a.k.a. children
            self.children = sortedcontainers.SortedList()
            # if True, this is the last element of a key set store a
            # member element of the key set. Must be a hashable
            # (i.e. hash(data) should work) and comparable/orderable
            # (i.e. data1 < data2 should work; see
            # https://wiki.python.org/moin/HowTo/Sorting/) type.
            self.flag_last = False
            self.data = data
            # the value associated to the key set if flag_last ==
            # True, otherwise None
            self.value = None

    def __init__(self, iterable=None):
        """Set up this SetTrieMap object.  If iterable is specified, it must
           be an iterable of (keyset, value) pairs from which set-trie
           is populated.
        """
        self.root = self.Node()
        if iterable is not None:
            for key, value in iterable:
                self.assign(key, value)

    def assign(self, akey, avalue):
        """Add key akey with associated value avalue to the container.
           akey must be a sortable and iterable container type."""
        self._assign(self.root, iter(sorted(akey)), avalue)

    @classmethod
    def _assign(cls, node, it, val):
        """Recursive function used by self.assign()."""
        try:
            data = next(it)
            nextnode = None
            try:
                # find first child with this data
                nextnode = node.children[node.children.index(
                    cls.Node(data))]
            except ValueError:  # not found
                nextnode = cls.Node(data)  # create new node
                node.children.add(nextnode)  # add to children & sort
            cls._assign(nextnode, it, val)  # recurse
        except StopIteration:  # end of set to add
            node.flag_last = True
            node.value = val

    def get(self, keyset, default=None):
        """Return the value associated to keyset if keyset is in this
           SetTrieMap, else default.
        """
        return self._get(self.root, iter(sorted(keyset)), default)

    @classmethod
    def _get(cls, node, it, default):
        """Recursive function used by self.get()."""
        try:
            data = next(it)
            try:
                # find first child with this data
                matchnode = node.children[node.children.index(
                    cls.Node(data))]
                return cls._get(matchnode, it, default)  # recurse
            except ValueError:  # not found
                return default
        except StopIteration:
            return (node.value if node.flag_last else default)

    def itersupersets(self, aset, mode=None):
        """Return an iterator over all (keyset, value) pairs from this
           SetTrieMap for which set keyset is a superset (proper or
           not proper) of set aset.  If mode is not None, the
           following values are allowed:

           mode='keys': return an iterator over only the keysets that
                        are supersets of aset is returned
           mode='values': return an iterator over only the values that
                          are associated to keysets that are supersets
                          of aset

           If mode is neither of 'keys', 'values' or None, behavior is
           equivalent to mode=None.

        """
        path = []
        return self._itersupersets(self.root, sorted(aset), path,
                                   mode)

    def supersets(self, aset, mode=None):
        """Return a list containing pairs of (keyset, value) for which keyset
           is superset of set aset.

           Parameter mode: see documentation for itersupersets().
        """
        return list(self.itersupersets(aset, mode))

    def itersubsets(self, aset, mode=None):
        """Return an iterator over pairs (keyset, value) from this SetTrieMap
           for which keyset is (proper or not proper) subset of set aset.
           If mode is not None, the following values are allowed:

           mode='keys': return an iterator over only the keysets that
                        are subsets of aset is returned

           mode='values': return an iterator over only the values that
                          are associated to keysets that are subsets of aset

           If mode is neither of 'keys', 'values' or None, behavior is
           equivalent to mode=None.
        """
        path = []
        return self._itersubsets(self.root, aset, path, mode)

    def subsets(self, aset, mode=None):
        """Return a list of (keyset, value) pairs from this set-trie
           for which keyset is (proper or not proper) subset of set aset.
           Parameter mode: see documentation for itersubsets().
        """
        return list(self.itersubsets(aset, mode))

    def iter(self, mode=None):
        """Returns an iterator to all (keyset, value) pairs stored in this
           SetTrieMap (using pre-order tree traversal).  The pairs are
           returned sorted to their keys, which are also sorted.  If
           mode is not None, the following values are allowed:

           mode='keys': return an iterator over only the keysets that
                        are subsets of aset

           mode='values': return an iterator over only the values that
                          are associated to keysets that are subsets
                          of aset

           If mode is neither of 'keys', 'values' or None, behavior is
           equivalent to mode=None.
        """
        path = []
        yield from self._iter(self.root, path, mode)

    def keys(self):
        """Alias for self.iter(mode='keys')."""
        return self.iter(mode='keys')

    def values(self):
        """Alias for self.iter(mode='values')."""
        return self.iter(mode='values')

    def items(self):
        """Alias for self.iter(mode=None)."""
        return self.iter(mode=None)

    def __iter__(self):
        """Same as self.iter(mode='keys')."""
        return self.keys()

    def aslist(self):
        """Return a list containing all the (keyset, value) pairs stored in
           this SetTrieMap.  The pairs are returned sorted to their
           keys, which are also sorted.
        """
        return list(self.iter())

    @classmethod
    def _printtree(cls, node, level, tabchr, tabsize, stream):
        """Used by self.printTree(), recursive preorder traverse and printing
           of trie node
        """
        print((str(node.data).rjust(len(repr(node.data)) + level * tabsize,
                                    tabchr) +
               (': {}'.format(repr(node.value)) if
                node.flag_last else
                '')),
              file=stream)
        for child in node.children:
            cls._printtree(child, level + 1, tabchr, tabsize, stream)

    @staticmethod
    def _terminate(node, path, mode):
        if mode == 'keys':
            yield set(path)
        elif mode == 'values':
            yield node.value
        else:
            yield (set(path), node.value)



class SetTrieMultiMap(SetTrieMap):
    """Like SetTrieMap, but the associated values are lists that can have
       multiple items added.

       Usage:
       ------
       >>> from settrie import SetTrieMultiMap
       >>> m.assign({1,2}, 'A')
       >>> m.assign({1,2,3}, 'B')
       >>> m.assign({1,2,3}, 'BB')
       >>> m.assign({2,3,5}, 'C')
       >>> m
       [({1, 2}, 'A'), ({1, 2, 3}, 'B'), ({1, 2, 3}, 'BB'), ({2, 3, 5}, 'C')]
       >>> m.get( {1,2,3} )
       ['B', 'BB']
       >>> m.get( {1, 2, 3, 4}, 'Nope!')
       'Nope!'
       >>> list(m.keys())
       [{1, 2}, {1, 2, 3}, {2, 3, 5}]
       >>> m.supersets( {1,2} )
       [({1, 2}, 'A'), ({1, 2, 3}, 'B'), ({1, 2, 3}, 'BB')]
       >>> m.supersets({1, 2}, mode='keys')
       [{1, 2}, {1, 2, 3}]
       >>> m.supersets({1, 2}, mode='values')
       ['A', 'B', 'BB']

    """

    def __init__(self, iterable=None):
        """Set up this SetTrieMultiMap object.  If iterable is specified, it
           must be an iterable of (keyset, value) pairs from which
           set-trie is populated; key may be repeated, all associated
           values will be stored.
        """
        self.root = self.Node()
        if iterable is not None:
            for key, value in iterable:
                self.assign(key, value)

    def assign(self, akey, avalue):
        """Add key akey with associated value avalue to the container.  akey
           must be a sortable and iterable container type.  If akey is
           an already exising key, avalue will be appended to the
           associated values.

           Multiple occurrences of the same value for the same key are
           preserved.

           Returns number of values associated to akey after the
           assignment, ie. returns 1 if akey was a nonexisting key
           before this function call, returns (number of items before
           call + 1) if akey was an already existing key.
        """
        valcnt = [0]
        self._assign(self.root, iter(sorted(akey)), avalue, valcnt)
        return valcnt[0]

    @classmethod
    def _assign(cls, node, it, val, valcnt):
        """Recursive function used by self.assign()."""
        try:
            data = next(it)
            nextnode = None
            try:
                # find first child with this data
                nextnode = node.children[node.children.index(
                    cls.Node(data))]
            except ValueError:  # not found
                nextnode = cls.Node(data)  # create new node
                node.children.add(nextnode)  # add to children & sort
            cls._assign(nextnode, it, val, valcnt)  # recurse
        except StopIteration:  # end of set to add
            node.flag_last = True
            if node.value is None:
                node.value = []
            node.value.append(val)
            # return # of values for key after this assignment
            valcnt[0] = len(node.value)

    def count(self, keyset):
        """Returns the number of values associated to keyset. If keyset is
           unknown, returns 0.
        """
        return self._count(self.root, iter(sorted(keyset)))

    @classmethod
    def _count(cls, node, it):
        """Recursive function used by self.count()."""
        try:
            data = next(it)
            try:
                # find first child with this data
                matchnode = node.children[node.children.index(
                    cls.Node(data))]
                return cls._count(matchnode, it)  # recurse
            except ValueError:  # not found
                return 0
        except StopIteration:
            if node.flag_last and node.value is not None:
                return len(node.value)
            else:
                return 0

    def iterget(self, keyset):
        """Return an iterator to the values associated to keyset."""
        return self._iterget(self.root, iter(sorted(keyset)))

    @classmethod
    def _iterget(cls, node, it):
        """Recursive function used by self.get()."""
        try:
            data = next(it)
            try:
                # find first child with this data
                matchnode = node.children[node.children.index(
                    cls.Node(data))]
                yield from cls._iterget(matchnode, it)  # recurse
            except ValueError:  # not found
                return None
        except StopIteration:
            if node.flag_last:
                yield from node.value

    @classmethod
    def _printtree(cls, node, level, tabchr, tabsize, stream):
        """Used by self.printTree(), recursive preorder traverse and printing
           of trie node
        """
        print((str(node.data).rjust(len(repr(node.data)) + level * tabsize,
                                    tabchr) +
               (': {}'.format(repr(node.value)) if node.flag_last else '')),
              file=stream)
        for child in node.children:
            cls._printtree(child, level + 1, tabchr, tabsize, stream)

    @staticmethod
    def _terminate(node, path, mode):
        if mode == 'keys':
            yield set(path)
        elif mode == 'values':
            yield from node.value
        else:
            yield from [(set(path), val) for val in node.value]

