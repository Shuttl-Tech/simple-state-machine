import pytest

from sfsm.errors import LoaderNotFound, LoaderException, UnknownStateError
from sfsm.machine import machine


def test_no_load_function_declared_raises_no_loader_found_exception():
    @machine(states=["INIT", "FINAL"], loader="abc")
    class MyMachine:
        pass
    with pytest.raises(LoaderNotFound):
        MyMachine()


def test_raise_loader_exception_if_loader_throws_any_exception():
    @machine(states=["INIT", "FINAL"], loader="load_state")
    class MyMachine:
        def load_state(self):
            raise Exception("Haha! You caught me.")
    with pytest.raises(LoaderException):
        MyMachine()


def test_sfsm_raises_unknown_state_exception_when_load_function_sets_unknown_state():
    @machine(states=[], loader="load_state")
    class MyMachine:
        def load_state(self):
            return "STATE"

    with pytest.raises(UnknownStateError):
        MyMachine()


def test_sfsm_raises_invalid_state_exception_when_current_state_is_not_source_state():
    pass


def test_non_transition_functions_are_accessible():
    pass


def test_transition_raises_not_machine_error_if_class_is_not_machine():
    pass
