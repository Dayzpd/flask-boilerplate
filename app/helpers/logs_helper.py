class LogsHelper(object):
    @staticmethod
    def log_entry(err):
        msg = getattr(err, 'message', None)
        if msg:
            print(err.message)
        else:
            print(str(err))
