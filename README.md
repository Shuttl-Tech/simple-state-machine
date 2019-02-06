# Simple State Machine

It is a python library with which you can `decorate` your class to make it a state machine.

## Installation

```bash
pip install simple-state-machine
```

## What is a state machine?

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
        
        if self.payment == "SUCCESS":
            self.payment_success()
        elif self.payment == "FAILED":
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
Decisions are not a concept in deterministic FSMs, hence we won't be supporting it. This means you will have to assert the current state for a decision accordingly.

## Development
To develop this, initialise a virtualenv
```
python3 -m venv venv
. ./venv/bin/activate
```
Inside the venv
```
pipenv install --dev --system
```

### Tests
```
make tests
```
