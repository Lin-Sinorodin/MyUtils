import time
from functools import wraps


def duration_from(t_start: float) -> str:
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


def decorator_with_args(no_param_decorator):
    """Decorates another decorator to make it accept parameters. Source: https://gist.github.com/lnhote/7875074"""
    def decorator(*args, **kwargs):
        def wrapper(func):
            return no_param_decorator(func, *args, **kwargs)
        return wrapper
    return decorator


@decorator_with_args
def retry(func, tries=4, first_delay=0.1, multiply_delay=2, continue_if_failed=True):
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


@decorator_with_args
def log(func, before_call=True, after_call=True, logger=None, logger_disp_level='INFO'):

    def log_msg(msg: str) -> None:
        """Display a message with logger or print"""
        if logger:
            if logger_disp_level == 'DEBUG':
                logger.debug(msg)
            else:
                logger.info(msg)
        else:
            print(msg)

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
