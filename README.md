# Simple State Machine

It is a python library with which you can `decorate` your class to make it a state machine.
<!-- toc -->

- [Installation](#installation)
- [State Machine](#state-machine)
- [Basic Usage](#basic-usage)
  * [What if my function has 2(or more) possible transitions?](#what-if-my-function-has-2or-more-possible-transitions)
  * [Error Handling](#error-handling)
- [Developers Guide](#developers-guide)
  * [Setup](#setup)
  * [Testing Mode](#testing-mode)
<!-- tocstop -->

## Installation

```bash
pip install simple-state-machine
```

## State Machine

A state machine which has a finite set of states is called a finite state machine. The one which doesn't have finite states is called a non-finite state machine.

A finite state machine is a mathematical concept in which the machine has a state and uses transitions to move from one state to another. Finite state machines can be of 2 types - deterministic and non-deterministic

A deterministic finite state machine produces the same result after given transitions, hence we can "determine" and so the name. In a non-deterministic finite state machine, for some state and input symbol, the next state may be nothing or one or two or more possible states.

This library provides a **deterministic finite state machine**.

## Basic Usage


```python
from state_machine.machine import machine, transition


@machine(states=["earth", "space"])
class Rocket(object):
    def __init__(self):
        self.moving = False
          
    # Mandatory to define this method
    def load_state(self):
        return "space" if self.moving else "earth"

    @transition(sources=["earth"], destination="space")
    def launch(self):
        self.moving = True
            
rocket = Rocket()
# assert m.current_state == "earth"
rocket.launch()
# assert m.current_state == "space"

rocket.launch()
# InvalidMoveError: Current state - space is not in source states - earth
```

### What if my function has 2(or more) possible transitions?
It is quite common to have functions which have 2 or more possible transitions. 

For eg. You are collecting a payment for an order. If the payment is valid, you want to complete the payment, else you want to fail it.

```python
from state_machine.machine import machine, transition


@machine(states=["INIT", "PAYMENT_IN_PROGRESS", "PAYMENT_COMPLETE", "PAYMENT_FAILED"])
class Order:
    def __init__(self):
        self.payment = ""
        
    def load_state(self):
        if not self.payment:
            return "INIT"
        
        if self.payment == "SUCCESS":
            return "PAYMENT_COMPLETE"
        
        if self.payment == "FAILED":
            return "PAYMENT_FAILED"
        
        return "PAYMENT_IN_PROGRESS"
        
    @transition(sources=["INIT"], destination="PAYMENT_IN_PROGRESS")
    def create_payment_request(self):
        self.payment = "IN_PROGRESS"
        
    def collect_payment(self, payment):
        assert self.load_state() == "PAYMENT_IN_PROGRESS"
        
        if payment == "SUCCESS":
            self.payment_success()
        elif payment == "FAILED":
            self.payment_failed()
            
    @transition(sources=["PAYMENT_IN_PROGRESS"], destination="PAYMENT_COMPLETE")
    def payment_success(self):
        self.payment = "SUCCESS"
        
    @transition(sources=["PAYMENT_IN_PROGRESS"], destination="PAYMENT_FAILED")
    def payment_failed(self):
        self.payment = "FAILED"
        
        
order1 = Order()
# assert order.current_state == "INIT"
order1.create_payment_request()
# assert order.current_state == "PAYMENT_IN_PROGRESS"
order1.collect_payment("SUCCESS")
# assert order.current_state == "PAYMENT_COMPLETE"


order2 = Order()
# assert order.current_state == "INIT"
order2.create_payment_request()
# assert order.current_state == "PAYMENT_IN_PROGRESS"
order2.collect_payment("FAILED")
# assert order.current_state == "PAYMENT_FAILED"
```

####  Note
Decision is not a concept in deterministic FSMs, hence we won't be supporting it. This means you will have to assert the current state for a decision accordingly.

### Error Handling
The library raises the following errors.

   1. `LoaderNotFound` - If your class doesn't implement a **load_state** method.
   2. `LoaderException` - If the **load_state** method threw an exception.
   3. `MachineNotFound` - If you used a **transition** decorator on a method whose class is not **machine** decorated.
   4. `InvalidStateError` - This is raised when the state machine encounters an unknown state. The state machine raises this error in 2 situations. One, when **load_state** returns an invalid state. And, when you pass invalid source or destination in a **transition**.
   5. `InvalidMoveError` - It is raised when you enter a transition with a *non-source* state.
   6. `UnintendedOperationError` - The state machine calls **load_state** function after each transition to ensure that the state has been updated to the destination. If a transition doesn't update the state of the machine to destination, this error is raised. For eg-
   
```python

@transition(source=["earth"], destination="sky")
def launch(self):
    pass # the function didn't do anything.
```

## Developer's Guide
### Setup
We use [pipenv](https://pipenv.readthedocs.io) to manage python packages. To setup your dev environment, locate yourself in the project directory and execute 
```
pipenv install --dev
pipenv shell
```

### Testing mode
```
make tests
```
