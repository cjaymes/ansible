# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible import errors

def eq(value, content):
    try:
        return value == content
    except Exception, e:
        raise errors.AnsibleFilterError('Test error: %s, string=%s' % str(e),str(string) )

def even(value):
    try:
        return value % 2 == 0
    except Exception, e:
        raise errors.AnsibleFilterError('Test error: %s, string=%s' % str(e),str(string) )

def ge(value):
    try:
        return value >= content
    except Exception, e:
        raise errors.AnsibleFilterError('Test error: %s, string=%s' % str(e),str(string) )

def gt(value):
    try:
        return value > content
    except Exception, e:
        raise errors.AnsibleFilterError('Test error: %s, string=%s' % str(e),str(string) )

def _in(value, content):
    try:
        return content in value
    except Exception, e:
        raise errors.AnsibleFilterError('Test error: %s, string=%s' % str(e),str(string) )

def not_in(value, content):
    try:
        return content not in value
    except Exception, e:
        raise errors.AnsibleFilterError('Test error: %s, string=%s' % str(e),str(string) )

def le(value, content):
    try:
        return value <= content
    except Exception, e:
        raise errors.AnsibleFilterError('Test error: %s, string=%s' % str(e),str(string) )

def lt(value, content):
    try:
        return value < content
    except Exception, e:
        raise errors.AnsibleFilterError('Test error: %s, string=%s' % str(e),str(string) )

def ne(value, content):
    try:
        return value != content
    except Exception, e:
        raise errors.AnsibleFilterError('Test error: %s, string=%s' % str(e),str(string) )

def none(value):
    try:
        return value is None
    except Exception, e:
        raise errors.AnsibleFilterError('Test error: %s, string=%s' % str(e),str(string) )

def odd(value):
    try:
        return value % 2 == 1
    except Exception, e:
        raise errors.AnsibleFilterError('Test error: %s, string=%s' % str(e),str(string) )


class TestModule(object):
    def tests(self):
        return {
            'eq': eq,
            'equalto': eq,

            'even': even,
            'ge': ge,
            'greaterthanequalto': ge,

            'gt': gt,
            'greaterthan': gt,

            'in': _in,
            'not_in': not_in,

            'le': le,
            'lessthanequalto': le,

            'lt': lt,
            'lessthan': lt,

            'ne': ne,
            'notequalto': ne,

            'none': none,

            'odd': odd,
        }
