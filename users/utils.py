import datetime
import os


def lock(lock_file):
    """
    Usage:
        @lock('file.lock')
        def run():
            # Function action
    """
    def decorator(target):

        def wrapper(*args, **kwargs):

            if os.path.exists(lock_file):
                raise Exception('Unable to get exclusive lock.')
            else:
                with open(lock_file, "w") as f:
                    d = datetime.datetime.utcnow()
                    epoch = datetime.datetime(1970, 1, 1)
                    t = (d - epoch).total_seconds()
                    f.write(str(t))

            # Execute the target
            result = target(*args, **kwargs)

            remove_attempts = 10
            os.remove(lock_file)
            while os.path.exists(lock_file) and remove_attempts >= 1:

                os.remove(lock_file)
                remove_attempts-=1

            return result
        return wrapper
    return decorator