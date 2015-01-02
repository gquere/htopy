==========
htopy v0.1
==========

Author: Guillaume Quéré


Introduction
============

htopy converts a C header file to an *autonomous* ctypes-compatible python file
importable from a python program that uses a shared library that the header
previously converted defines.

Dependencies
============

CParser library:
https://code.launchpad.net/~luke-campagnola/pyclibrary/main

Usage
=====

Note: this is python2.7 for now because of the dependency.
htopy example.h > c_example.py

