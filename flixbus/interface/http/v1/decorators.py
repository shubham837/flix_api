import json
from functools import wraps

from flask import make_response, request


def _handle_unauthorized():
    '''The default way of handling unauthorized requests.

    Returns:
        A 401 - Unauthorized HTTP Response
    '''
    return make_response(
        json.dumps({'message': "Unauthorized"}), 401,
        {'Content-Type': 'application/json'}
    )


def authenticate_user(unauthorized_hook=_handle_unauthorized,
                      unauthorized_hook_kwargs={}):
    '''Return a decorator that authenticates a user.

    Args:
        unauthorized_hook (function): A function that would be called if
            the request is unauthorized. Defaults to `_handle_unauthorized()`.
        unauthorized_hook_kwargs (dict): A dictionary mapping function
            parameters to their values, to be passed to `unauthorized_hook()`.

    Returns:
        (function): A decorator that authenticates a user.
    '''
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user = request.headers.get('user')
            if not user:
                return unauthorized_hook(**unauthorized_hook_kwargs)
            return func(*args, **kwargs)
        return wrapper
    return decorator


def authorize_service(allowed_clients,
                      unauthorized_hook=_handle_unauthorized,
                      unauthorized_hook_kwargs={}):
    '''Return a decorator that authorizes a service.

    Args:
        allowed_clients (list): A list of client names which are allowed.
        unauthorized_hook (function): A function that would be called if
            the request is unauthorized. Defaults to `_handle_unauthorized()`.
        unauthorized_hook_kwargs (dict): A dictionary mapping function
            parameters to their values, to be passed to `unauthorized_hook()`.

    Returns:
        (function): A decorator that authorizes a service.
    '''
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            client_type = request.headers.get('client_type')
            if (client_type not in
                    [client.lower() for client in allowed_clients]):
                return unauthorized_hook(**unauthorized_hook_kwargs)
            return func(*args, **kwargs)
        return wrapper
    return decorator


def allow_user_or_service(allowed_clients,
                          unauthorized_hook=_handle_unauthorized,
                          unauthorized_hook_kwargs={}):
    '''Return a decorator that authenticates either a user or a service.

    Args:
        allowed_clients (list): A list of client names which are allowed.
        unauthorized_hook (function): A function that would be called if
            the request is unauthorized. Defaults to `_handle_unauthorized()`.
        unauthorized_hook_kwargs (dict): A dictionary mapping function
            parameters to their values, to be passed to `unauthorized_hook()`.

    Returns:
        (function): A decorator that authenticates a user or a service.
    '''
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return (
                authorize_service(
                    allowed_clients, unauthorized_hook=lambda: False
                )(func)(*args, **kwargs) or
                authenticate_user(
                    unauthorized_hook=unauthorized_hook,
                    unauthorized_hook_kwargs=unauthorized_hook_kwargs
                )(func)(*args, **kwargs)
            )
        return wrapper
    return decorator
