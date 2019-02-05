# Simple State Machine

It is a python library with which you can `decorate` your class to make it a state machine.

## Finite State Machine

A finite state machine is a mathematical concept in which the machine has a state and uses transitions to move from one state to another. Finite state machines can be of 2 types - deterministic and non-deterministic

A deterministic finite state machine produces the same result after given transitions, hence we can "determine" and so the name. In a non-deterministic finite state machine, for some state and input symbol, the next state may be nothing or one or two or more possible states.

This library provides a **deterministic finite state machine**.

## Usage


```python
@machine(states=["earth", "space"], init="load_state")
class MyMachine(object):
    def __init__(self, name):
        self.name = name
          
    def load_state(self):
        return "earth"

    @transition(sources=["earth"], destination="space")
    def launch(self):
        pass
            
m = MyMachine("Rocket")
# assert m.current_state == "earth"
m.launch()
# assert m.current_state == "space"

m.launch()
# InvalidMoveError: Current state - space is not in source states - earth
```
