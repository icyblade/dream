import json
import logging
import traceback


def helper(function):
    """Decorator to mark helper functions.

    Will do nothing to the original function.
    """
    return function


def flask_method(function):
    """Decorator to handle errors."""
    def generate_errcode(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception as e:
            logging.error(str(e))
            traceback.print_exc()
            return json.dumps({
                'errcode': 1,
                'error_message': str(e)
            })

    return generate_errcode
