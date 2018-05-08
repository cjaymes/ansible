from ansible import errors

def contains(value, content):
    try:
        return content in value
    except Exception, e:
        raise errors.AnsibleFilterError('contains plugin error: %s, string=%s' % str(e),str(string) )

class TestModule(object):
    def tests(self):
        return {
            'contains': contains,
        }
