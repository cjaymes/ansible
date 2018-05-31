# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible import errors

def eq(value, content):
    try:
        return value == content
    except Exception, e:
        raise errors.AnsibleFilterError('Test error: %s, value=%s, content=%s' % (str(e),str(value),str(content)) )

def even(value):
    try:
        return value % 2 == 0
    except Exception, e:
        raise errors.AnsibleFilterError('Test error: %s, value=%s' % (str(e),str(value)) )

def ge(value, content):
    try:
        return value >= content
    except Exception, e:
        raise errors.AnsibleFilterError('Test error: %s, value=%s, content=%s' % (str(e),str(value),str(content)) )

def gt(value, content):
    try:
        return value > content
    except Exception, e:
        raise errors.AnsibleFilterError('Test error: %s, value=%s, content=%s' % (str(e),str(value),str(content)) )

def _in(value, content):
    try:
        return value in content
    except Exception, e:
        raise errors.AnsibleFilterError('Test error: %s, value=%s, content=%s' % (str(e),str(value),str(content)) )

def not_in(value, content):
    try:
        return value not in content
    except Exception, e:
        raise errors.AnsibleFilterError('Test error: %s, value=%s, content=%s' % (str(e),str(value),str(content)) )

def le(value, content):
    try:
        return value <= content
    except Exception, e:
        raise errors.AnsibleFilterError('Test error: %s, value=%s, content=%s' % (str(e),str(value),str(content)) )

def lt(value, content):
    try:
        return value < content
    except Exception, e:
        raise errors.AnsibleFilterError('Test error: %s, value=%s, content=%s' % (str(e),str(value),str(content)) )

def ne(value, content):
    try:
        return value != content
    except Exception, e:
        raise errors.AnsibleFilterError('Test error: %s, value=%s, content=%s' % (str(e),str(value),str(content)) )

def none(value):
    try:
        return value is None
    except Exception, e:
        raise errors.AnsibleFilterError('Test error: %s, value=%s' % (str(e),str(value)) )

def odd(value):
    try:
        return value % 2 == 1
    except Exception, e:
        raise errors.AnsibleFilterError('Test error: %s, value=%s' % (str(e),str(value)) )


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
