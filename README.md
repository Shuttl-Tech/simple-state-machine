# Simple State Machine

It is a python library with which you can `decorate` your class to make it a state machine.

## Finite State Machine

A finite state machine is a mathematical concept in which the machine has a state and uses transitions to move from one state to another. Finite state machines can be of 2 types - deterministic and non-deterministic

A deterministic finite state machine produces the same result after given transitions, hence we can "determine" and so the name. In a non-deterministic finite state machine, for some state and input symbol, the next state may be nothing or one or two or more possible states.

This library provides a **deterministic finite state machine**.

## Usage


```python
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

For eg. You live in the plains and depending on the weather you want to go to a mountain or a beach for a vacation. If its cold, you'd like to go to a beach else mountain 

```python
@machine(states=["plains", "mountain", "beach"])
class VacationPlan:
    def __init__(self):
        self.is_cold_weather = False
        self.on_vacation = False
        
    def load_state(self):
        if not self.on_vacation:
            return "plains"
        
        return "beach" if self.is_cold_weather else "mountain"
        
    @transition(sources=["plains"], destination="beach")
    def get_away_from_cold_weather(self):
        self.is_cold_weather = True
        self.on_vacation = True
        print("We're going to the beach")
    
    
    @transition(sources=["plains"], destination="mountain")
    def get_away_from_warm_weather(self):
        self.is_cold_weather = False
        self.on_vacation = True
        
    def get_away(self, temperature: int): # Temperature is in Celsius
        assert self.load_state() == "plains"
        
        if temperature > 20:
            return self.get_away_from_warm_weather()
        
        return self.get_away_from_cold_weather()
        
        
plan = VacationPlan()
plan.get_away(23)
# We're going to the mountain

plan = VacationPlan()
plan.get_away(10)
# We're going to the beach

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
