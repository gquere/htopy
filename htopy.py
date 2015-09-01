#!/usr/bin/env python2.7

import sys
import os
from CParser import CParser

LIBNAME = 'example'

# Correlation table for direct types
cor =    {
    'bool': 'ctypes.c_bool',
    'char': 'ctypes.c_char',
    'byte': 'ctypes.c_byte',
    'unsigned byte': 'ctypes.c_ubyte',
    'short': 'ctypes.c_short',
    'unsigned short': 'ctypes.c_ushort',
    'int': 'ctypes.c_int',
    'unsigned int': 'ctypes.c_uint',
    'long': 'ctypes.c_long',
    'unsigned long': 'ctypes.c_ulong',
    'long long': 'ctypes.c_longlong',
    'unsigned long long': 'ctypes.c_ulonglong',
    'float': 'ctypes.c_float',
    'double': 'ctypes.c_double',
    'void': 'None',

    'int8_t': 'ctypes.c_int8',
    'int16_t': 'ctypes.c_int16',
    'int32_t': 'ctypes.c_int32',
    'int64_t': 'ctypes.c_int64',

    'uint8_t': 'ctypes.c_uint8',
    'uint16_t': 'ctypes.c_uint16',
    'uint32_t': 'ctypes.c_uint32',
    'uint64_t': 'ctypes.c_uint64',

    'size_t': 'ctypes.c_int',
    'sem_t': 'ctypes.c_int',
    }

# Correlation table for pointer types
corp =    {
    'char': 'ctypes.c_char_p',
    'void': 'ctypes.c_void_p',
    }

def getCor(member_type):
    if '*' in member_type:
        try:
            pytype = corp[member_type[0]]
        except KeyError:
            pytype = 'ctypes.c_void_p'
    else:
        try:
            pytype = cor[member_type[0]]
        except KeyError:
            pytype = 'ctypes.c_void_p'

    return pytype

def getMult(member_type):
    try:
        if member_type[2] is not None:
            value = member_type[2][0]
            return str(value)
        else:
            return None
    except Exception:
        return None


########################### STRUCTURES #########################################
def doStruct(struct, name):
    print('class ' + name + '(Structure):')
    print('_fields_ = [')
    for member in struct['members']:
        pytype = getCor(member[1])
        mult = getMult(member[1])
        if mult is not None:
            print('\t("' + member[0] + '", ' + pytype + ' * ' + mult + '),')
        else:
            print('\t("' + member[0] + '", ' + pytype + '),')
    print('\t]\n')

def doStructs(structs):
    for struct in structs:
        doStruct(structs[struct], struct)


########################### FUNCTIONS ##########################################
def getArgs(arguments):
    pyargs = []

    for argument in arguments:
        pyargs.append(getCor(argument[1]))

    return pyargs

def doArgs(arguments):
    pyargs = getArgs(arguments)
    print('['),
    for pyarg in pyargs:
        print(pyarg + ',' ),
    print(']')

def doFunction(function, name):
    print('self.' + name + ' = ' + 'self._lib.' + name)
    print('self.' + name + '.argtypes = '),
    doArgs(function[1])
    print('self.' + name + '.restype = ' + getCor(function[0]))
    print

def doFunctions(functions):
    for function in functions:
        doFunction(functions[function], function)


########################### TYPES ##############################################
def doType(c_type):
    cor[c_type] = c_type
    corp[c_type] = 'POINTER(' + c_type + ')'

def doTypes(c_types):
    print(c_types)
    for c_type in c_types:
        doType(c_type)


################################################################################
if __name__ == '__main__':
    cheader = sys.argv[1]
    p = CParser(cheader)
    p.processAll()

    for k in p.dataList:
        if bool(p.defs[k]):
            if k is 'types':
                doTypes(p.defs[k])
            if k is 'structs':
                doStructs(p.defs[k])
            if k is 'functions':
                doFunctions(p.defs[k])

