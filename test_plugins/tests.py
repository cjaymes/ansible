from ansible import errors

def contains(value, content):
    try:
        return content in value
    except Exception, e:
        raise errors.AnsibleFilterError('contains plugin error: %s, string=%s' % str(e),str(string) )

def not_contains(value, content):
    try:
        return content not in value
    except Exception, e:
        raise errors.AnsibleFilterError('contains plugin error: %s, string=%s' % str(e),str(string) )


class TestModule(object):
    def tests(self):
        return {
            'contains': contains,
            'not_contains': not_contains,
        }
