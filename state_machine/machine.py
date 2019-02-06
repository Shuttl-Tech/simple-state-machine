from functools import wraps
from typing import List

from state_machine.errors import (
    LoaderException,
    LoaderNotFound,
    InvalidStateError,
    MachineNotFound,
    InvalidMoveError,
    UnintendedOperationError)


def machine(states: List):
    def decorator(cls):
        @wraps(cls)
        def func(*args, **kwargs):
            obj = cls(*args, **kwargs)
            obj.states = states
            try:
                current_state = getattr(obj, "load_state")()
            except AttributeError:
                raise LoaderNotFound("load_state method not defined in the class.")
            except Exception as e:
                raise LoaderException(e)

            if current_state not in states:
                raise InvalidStateError(f"Current state - {current_state} is not known")

            obj.current_state = current_state

            # Tag the class that its a simple state state_machine
            obj.is_sfsm = True
            return obj

        return func

    return decorator


def transition(sources: List[str], destination: str):
    def decorator(f):
        def func(self, *args, **kwargs):
            if not hasattr(self, "is_sfsm"):
                raise MachineNotFound(
                    "Transition can only be applied on a state_machine's method."
                )

            [validate_state(source, self.states) for source in sources]
            validate_state(destination, self.states)

            if self.current_state not in sources:
                raise InvalidMoveError(
                    f"Current state - {self.current_state} is not in source states - {', '.join(sources)}"
                )
            f(self, *args, **kwargs)
            if self.load_state() != destination:
                raise UnintendedOperationError("The transition didn't update the state to intended destination")

            self.current_state = destination

        return func

    return decorator


def validate_state(state: str, valid_states: List[str]):
    if state not in valid_states:
        raise InvalidStateError(
            f"{state} is not a valid state. Valid states are {', '.join(valid_states)}"
        )
