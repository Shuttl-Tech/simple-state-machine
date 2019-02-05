from typing import List

from sfsm.errors import LoaderException, UnknownStateError, LoaderNotFound


def machine(states: List, loader: str):
    def decorator(cls):
        def f(*args, **kwargs):
            obj = cls(*args, **kwargs)
            obj.states = states
            try:
                current_state = getattr(obj, loader)()
            except AttributeError:
                raise LoaderNotFound("Given loader wasn't found in the class.")
            except Exception as e:
                raise LoaderException(e)

            if current_state not in states:
                raise UnknownStateError(f"Current state - {current_state} is not known")

            obj.current_state = current_state
            return obj
        return f
    return decorator

