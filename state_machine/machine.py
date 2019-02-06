from typing import List

from state_machine.errors import (
    LoaderException,
    LoaderNotFound,
    InvalidStateError,
    MachineNotFound,
    InvalidMoveError,
    UnintendedOperationError,
)


def machine(states: List):
    def decorator(cls):
        def init(self, states):
            self.states = states

            try:
                current_state = getattr(self, "load_state")()
            except AttributeError:
                raise LoaderNotFound("load_state method not defined in the class.")
            except Exception as e:
                raise LoaderException(e)

            if current_state not in states:
                raise InvalidStateError(f"Current state - {current_state} is not known")

            self.current_state = current_state

            # Tag the class that its a simple state state_machine
            self.is_sfsm = True

        class_constructor = cls.__init__

        def __init__(self, *args, **kwargs):
            class_constructor(self, *args, **kwargs)
            init(self, states)

        setattr(cls, "__init__", __init__)
        return cls

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
                raise UnintendedOperationError(
                    "The transition didn't update the state to intended destination"
                )

            self.current_state = destination

        return func

    return decorator


def validate_state(state: str, valid_states: List[str]):
    if state not in valid_states:
        raise InvalidStateError(
            f"{state} is not a valid state. Valid states are {', '.join(valid_states)}"
        )
