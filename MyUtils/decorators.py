import time
from functools import wraps


def duration_from(t_start) -> str:
    return f'{time.perf_counter() - t_start :.02f}s'


def func_call_str(func, args, kwargs) -> str:
    args_str_list = list(args)
    kwargs_str_list = [f'{key}={value}' for key, value in kwargs.items()]
    call_params = ', '.join(args_str_list + kwargs_str_list)
    return f'{func.__name__}({call_params})'


def exception_str(e: Exception) -> str:
    return f'{type(e).__name__}({e})'


class FailedAllRetries(Exception):
    """Custom exception for retry decorator"""
    pass


def retry(tries=4, first_delay=0.1, multiply_delay=2, continue_if_failed=True):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            delay = first_delay
            remaining_tries = tries
            while remaining_tries > 0:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    remaining_tries -= 1

                    msg = f'{exception_str(e)} when calling: {func_call_str(func, args, kwargs)}. '
                    retry_msg = f'Retrying ({tries-remaining_tries}/{tries}) in {delay} seconds...'
                    print(msg+retry_msg)

                    time.sleep(delay)
                    delay *= multiply_delay   # multiply the waiting time for next try

            if continue_if_failed:
                # return False, and keep running the program
                return False
            else:
                # return an exception to force the program to stop
                raise FailedAllRetries(f'Failed after all {tries} tries')

        return wrapper
    return decorator


def log(before_call=True, after_call=True, logger=None):
    def log_msg(msg):
        if logger:
            logger.info(msg)
        else:
            print(msg)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            t_start = time.perf_counter()

            if before_call:
                log_msg(f'Calling {func_call_str(func, args, kwargs)}')

            result = func(*args, **kwargs)

            if after_call:
                log_msg(f'call for {func.__name__} finished after {duration_from(t_start)}')

            return result
        return wrapper
    return decorator


if __name__ == '__main__':
    @retry(continue_if_failed=True)
    def test_retry(param1='param1', param2='param2'):
        raise ValueError('value not supported')


    print('\nTest retry decorator:')
    test_retry('param1', param2='param2')


    @log()
    def test_log():
        print('Inside logged function')
        time.sleep(0.2)


    print('\nTest log decorator:')
    test_log()
