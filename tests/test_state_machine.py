import pytest

from state_machine.errors import (
    LoaderNotFound,
    LoaderException,
    MachineNotFound,
    InvalidStateError,
    InvalidMoveError,
    UnintendedOperationError)
from state_machine.machine import machine, transition


def test_no_load_function_declared_raises_no_loader_found_exception():
    @machine(states=["A", "B"])
    class MyMachine:
        pass

    with pytest.raises(LoaderNotFound):
        MyMachine()


def test_raise_loader_exception_if_loader_throws_any_exception():
    @machine(states=["A", "B"])
    class MyMachine:
        def load_state(self):
            raise Exception("Haha! You caught me.")

    with pytest.raises(LoaderException):
        MyMachine()


def test_machine_raises_unknown_state_exception_when_load_function_sets_unknown_state():
    @machine(states=[])
    class MyMachine:
        def load_state(self):
            return "STATE"

    with pytest.raises(InvalidStateError):
        MyMachine()


def test_machine_raises_invalid_move_error_when_current_state_is_not_source_state():
    @machine(states=["A", "B"])
    class MyMachine:
        def load_state(self):
            return "B"

        @transition(sources=["A"], destination="B")
        def move(self):
            pass

    with pytest.raises(InvalidMoveError):
        m = MyMachine()
        m.move()


def test_non_transition_functions_are_accessible():
    @machine(states=["A", "B"])
    class MyMachine:
        def __init__(self):
            self.moving = False

        def load_state(self):
            return "B" if self.moving else "A"

        def some_func(self):
            return "Hello"

        @transition(sources=["A"], destination="B")
        def move(self):
            self.moving = True

    m = MyMachine()
    assert m.some_func() == "Hello"
    m.move()
    assert m.current_state == "B"


def test_transition_raises_not_machine_error_if_class_is_not_machine():
    class MyMachine:
        @transition(sources=["a"], destination="b")
        def func(self):
            pass

    with pytest.raises(MachineNotFound):
        m = MyMachine()
        m.func()


def test_transition_raises_invalid_state_error_if_sources_are_not_valid():
    @machine(states=["A", "B"])
    class MyMachine:
        def __init__(self):
            self.moving = False

        def load_state(self):
            return "A"

        @transition(sources=["A", "C"], destination="B")
        def move(self):
            self.moving = True

    with pytest.raises(InvalidStateError):
        m = MyMachine()
        m.move()


def test_transition_raises_invalid_state_error_if_destination_is_not_valid():
    @machine(states=["A", "B"])
    class MyMachine:
        def __init__(self):
            self.moving = False

        def load_state(self):
            return "C" if self.moving else "B"

        @transition(sources=["A"], destination="C")
        def move(self):
            self.moving = True

    with pytest.raises(InvalidStateError):
        m = MyMachine()
        m.move()


def test_transition_from_multiple_states():
    @machine(states=["sky", "tree", "ground"])
    class MyMachine:
        def __init__(self):
            self.flying = True
            self.stuck_on_tree = False

        def load_state(self):
            if self.flying:
                return "sky"

            if self.stuck_on_tree:
                return "tree"

            return "ground"

        @transition(sources=["sky"], destination="tree")
        def fall_on_tree(self):
            self.flying = False
            self.stuck_on_tree = True

        @transition(sources=["tree", "sky"], destination="ground")
        def fall(self):
            self.flying = False
            self.stuck_on_tree = False

    m1 = MyMachine()
    assert m1.current_state == "sky"
    m1.fall_on_tree()
    assert m1.current_state == "tree"
    with pytest.raises(InvalidMoveError):
        m1.fall_on_tree()

    m2 = MyMachine()
    assert m2.current_state == "sky"
    m2.fall_on_tree()
    assert m2.current_state == "tree"
    m2.fall()
    assert m2.current_state == "ground"

    m3 = MyMachine()
    assert m3.current_state == "sky"
    m3.fall()
    assert m3.current_state == "ground"


def test_simple_transition():
    @machine(states=["ground", "sky"])
    class MyMachine:
        def __init__(self):
            self.moving = False

        def load_state(self):
            if self.moving:
                return "sky"
            return "ground"

        @transition(sources=["ground"], destination="sky")
        def jump(self):
            self.moving = True

    m = MyMachine()
    assert m.current_state == "ground"
    m.jump()
    assert m.current_state == "sky"
    with pytest.raises(InvalidMoveError):
        m.jump()


def test_class_with_constructor():
    @machine(states=["earth", "space"])
    class MyMachine(object):
        def __init__(self, name):
            self.name = name
            self.state = "rest"

        def load_state(self):
            if self.state == "rest":
                return "earth"
            elif self.state == "moving":
                return "space"

        @transition(sources=["earth"], destination="space")
        def launch(self):
            self.state = "moving"
            pass

    m = MyMachine("Rocket")
    assert m.name == "Rocket"
    assert m.current_state == "earth"

    m.launch()
    assert m.current_state == "space"


def test_transition_checks_load_state_before_moving_to_destination():
    @machine(states=["delhi", "gurgaon"])
    class ShuttlBus:
        def load_state(self):
            return "delhi"

        @transition(sources=["delhi"], destination="gurgaon")
        def run(self):
            return "AC SEAT GUARANTEED!"

    with pytest.raises(UnintendedOperationError):
        bus = ShuttlBus()
        bus.run()
