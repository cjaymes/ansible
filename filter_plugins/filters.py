# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible import errors

def duplicates(list_):
    try:
        unique = {}
        duplicates = []

        for x in list_:
            if x not in unique:
                unique[x] = 1
            else:
                if unique[x] == 1:
                    duplicates.append(x)
                unique[x] += 1

        return duplicates
    except Exception, e:
        raise errors.AnsibleFilterError('Filter error: %s, list_=%s' % (str(e),str(list_)) )


class FilterModule(object):
    def filters(self):
        return {
            'duplicates': duplicates,
        }
