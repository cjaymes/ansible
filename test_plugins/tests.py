from ansible import errors

def containing(value, content):
    try:
        print(str(value))
        print(str(content))
        return content in value
    except Exception, e:
        raise errors.AnsibleFilterError('containing plugin error: %s, string=%s' % str(e),str(string) )

def not_containing(value, content):
    try:
        return content not in value
    except Exception, e:
        raise errors.AnsibleFilterError('not_containing plugin error: %s, string=%s' % str(e),str(string) )


class TestModule(object):
    def tests(self):
        return {
            'containing': containing,
            'not_containing': not_containing,
        }
