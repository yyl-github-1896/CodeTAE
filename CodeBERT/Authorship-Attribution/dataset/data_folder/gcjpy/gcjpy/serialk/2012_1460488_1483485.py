#!/usr/bin/env python2.6
 
 translate = {'a': 'y', 'c': 'e', 'b': 'h', 'e': 'o', 'd': 's', 'g': 'v', 'f': 'c', 'i': 'd', 'h': 'x', 'k': 'i', 'j': 'u', 'm': 'l', 'l': 'g', 'o': 'k', 'n': 'b', 'q': 'z', 'p': 'r', 's': 'n', 'r': 't', 'u': 'j', 't': 'w', 'w': 'f', 'v': 'p', 'y': 'a', 'x': 'm', 'z': 'q'}
 
 nb = int(raw_input())
 for i in xrange(nb):
     s = ''.join([translate[char] if char in translate.keys() else char for char in str(raw_input())])
     print 'Case #{0}:'.format(i+1), s
