# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import stat
from ansible import errors, vars

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

def less_permissive(value, content):
    try:
        if isinstance(value, str):
            value = int(value, 8)
        if isinstance(content, str):
            content = int(content, 8)
        val_owner = value & stat.S_IRWXU
        val_group = value & stat.S_IRWXG
        val_other = value & stat.S_IRWXO
        con_owner = content & stat.S_IRWXU
        con_group = content & stat.S_IRWXG
        con_other = content & stat.S_IRWXO

        return val_owner < con_owner or val_group < con_group or val_other < con_other

    except Exception, e:
        raise errors.AnsibleFilterError('Test error: %s, value=%s, content=%s' % (str(e),str(value),str(content)) )

def more_permissive(value, content):
    try:
        if isinstance(value, (str, AnsibleUnsafeText)):
            v = int(value, 8)
        else:
            v = value
        if isinstance(content, (str, AnsibleUnsafeText)):
            c = int(content, 8)
        else:
            c = content
        val_owner = v & stat.S_IRWXU
        val_group = v & stat.S_IRWXG
        val_other = v & stat.S_IRWXO
        con_owner = c & stat.S_IRWXU
        con_group = c & stat.S_IRWXG
        con_other = c & stat.S_IRWXO

        return val_owner > con_owner or val_group > con_group or val_other > con_other

    except Exception, e:
        raise errors.AnsibleFilterError('Test error: %s, value=%s, content=%s' % (str(e),str(value),str(content)) )

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

            'less_permissive': less_permissive,
            'more_permissive': more_permissive,

            'ne': ne,
            'notequalto': ne,

            'none': none,

            'odd': odd,
        }
