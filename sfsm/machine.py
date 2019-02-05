from functools import wraps
from typing import List

from sfsm.errors import (
    LoaderException,
    LoaderNotFound,
    InvalidStateError,
    MachineNotFound,
    InvalidMoveError,
)


def machine(states: List, init: str):
    def decorator(cls):
        @wraps(cls)
        def func(*args, **kwargs):
            obj = cls(*args, **kwargs)
            obj.states = states
            try:
                current_state = getattr(obj, init)()
            except AttributeError:
                raise LoaderNotFound("Given loader wasn't found in the class.")
            except Exception as e:
                raise LoaderException(e)

            if current_state not in states:
                raise InvalidStateError(f"Current state - {current_state} is not known")

            obj.current_state = current_state
            obj.is_sfsm = True
            return obj

        return func

    return decorator


def transition(sources: List[str], destination: str):
    def decorator(f):
        def func(self, *args, **kwargs):
            if not hasattr(self, "is_sfsm"):
                raise MachineNotFound(
                    "Transition can only be applied on a machine's method."
                )

            [validate_state(source, self.states) for source in sources]
            validate_state(destination, self.states)
            if self.current_state not in sources:
                raise InvalidMoveError(
                    f"Current state - {self.current_state} is not in source states - {', '.join(sources)}"
                )
            f(self, *args, **kwargs)
            self.current_state = destination

        return func

    return decorator


def validate_state(state: str, valid_states: List[str]):
    if state not in valid_states:
        raise InvalidStateError(
            f"{state} is not a valid state. Valid states are {', '.join(valid_states)}"
        )
