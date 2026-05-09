
from typing import Literal

class Step:
    def __init__(
        self, 
        name: str, 
        workout: str,
        _duration: int, 
        thrz: int, 
        trpe: int
    ):
        self.name = name
        self.workout = workout
        self._duration = _duration
        self.thrz = thrz
        self.trpe = trpe 
    
    def __str__(self):
        pass
    
    @property
    def duration(self):
        return self._duration 

    def to_dict(self):
        return {
            "name": self.name,
            "workout": self.workout,
            "duration": self.duration,
            "thrz": self.thrz,
            "trpe": self.trpe
        }

    @classmethod
    def from_dict(cls, data):
        return cls(**data)   
class Exercise:
    def __init__(
        self, 
        name: str,
        steps: list[Step]
    ):
        
        self.name = name
        self.steps: list[Step] = steps
       
    @property
    def stepcount(self):
        return len(self.steps) 
        
    def to_dict(self):
        return {
            "name": self.name,
            "steps": [s.to_dict() for s in self.steps]
        }
    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            steps=[Step.from_dict(s) for s in data["steps"]]
        )     
class Session:
    def __init__(
        self,
        name: str,
        seshtype: str,
        exercises: list[Exercise],
    ):
        self.name = name
        self.seshtype = seshtype
        self.exercises = exercises

    @property
    def duration(self) -> int:
        return sum(
            step.duration
            for exercise in self.exercises
            for step in exercise.steps
        )
    
    @property
    def exercisecount(self):
        return len(self.exercises)

    def to_dict(self):
        return {
            "name": self.name,
            "seshtype": self.seshtype,
            "exercises": [e.to_dict() for e in self.exercises],
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            seshtype=data["seshtype"],
            exercises=[Exercise.from_dict(e) for e in data["exercises"]],
        )
class LoggedSession(Session):
    def __init__(
        self, 
        completed: bool, 
        perceived_effort: int | None = None, 
        notes: str | None = None, 
        **kwargs
    ):
        super().__init__(**kwargs)
        self.completed = completed
        self.perceived_effort = perceived_effort
        self.notes = notes

class DayPlan:
    def __init__(self, date: str, sessions: list[Session]):
        self.date = date
        self.sessions = sessions

    def to_dict(self):
        return {
            "date": self.date,
            "sessions": [s.to_dict() for s in self.sessions]
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            date=data["date"],
            sessions=[Session.from_dict(s) for s in data["sessions"]]
        )
class WeekPlan:
    def __init__(self):
        self.days: dict[str, list[Session]] = {
            "monday": [],
            "tuesday": [],
            "wednesday": [],
            "thursday": [],
            "friday": [],
            "saturday": [],
            "sunday": [],
        }

    @property
    def sessioncount(self):
        return sum(len(self.days[i] for i, _ in enumerate(self.days)))
    
    def add_session(self, day: str, session: Session):
        self.days[day.lower()].append(session)

    def get_day(self, day: str) -> list[Session]:
        return self.days.get(day.lower(), [])

class Event:
    def __init__(
        self,
        name: str,
        date: str,
        type: str,
        city: str,
        state: str,
        country: str,
        distance: float | list[float] | None = None,
        priority: Literal["Primary", "Secondary", "Tertiary", "Supporting"] | None = None,
        notes: str | None = None
    ):
        self.name = name
        self.date = date
        self.type = type
        self.distance = distance
        self.location = [city, state, country]
        self.priority = priority
        self.notes = notes

    def to_dict(self):
        return {
            "name": self.name,
            "date": self.date,
            "type": self.type,
            "distance": self.distance,
            "location": self.location,
            "priority": self.priority,
            "notes": self.notes,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(**data)  

