from __future__ import annotations

from durapy.src.types.color_dtypes import x_color_text as color_text
from typing import Literal, get_args, get_origin, get_type_hints
import json, inspect

_DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

def _insert_json(path_to_json: str, content_dict: dict) -> None:
    """Inserts a dictionary into a `JSON` file. If the file does not exist, it creates it."""

    with open(path_to_json, "w", encoding="utf-8") as JSONFile:
        json.dump(content_dict, JSONFile, indent=4, sort_keys=True)
def _extract_json(path_to_json: str) -> dict | None:
    """Extracts a `JSON` file and returns the content as a dictionary."""

    try:
        with open(path_to_json, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        return None

def _color_from_zone(zone: float) -> str | None:
    """Returns a color name based on the given heart rate zone."""
    if zone is None or not isinstance(zone, (int, float)) or zone < 0:
        return None
    if 0 <= zone < 1:
        return "gray"
    elif 1 <= zone < 2:
        return "blue"
    elif 2 <= zone < 3:
        return "green"
    elif 3 <= zone < 4:
        return "yellow"
    elif 4 <= zone < 5:
        return "orange"
    elif 5 <= zone:
        return "red"
    else:
        return None
def _color_from_trpe(trpe: int) -> str | None:
    """Returns a color name based on the given TRPE value."""
    if trpe is None or not isinstance(trpe, int) or trpe < 0:
        return None
    if 0 <= trpe < 2:
        return "gray"
    elif 2 <= trpe < 4:
        return "blue"
    elif 4 <= trpe < 6:
        return "green"
    elif 6 <= trpe < 8:
        return "yellow"
    elif 8 <= trpe < 10:
        return "orange"
    elif trpe >= 10:
        return "red"
    else:
        return None
def _color_from_priority(priority: str) -> str | None:
    """Returns a color name based on the given priority level."""
    if priority is None or not isinstance(priority, str):
        return None
    priority = priority.lower()
    if priority == "primary":
        return "red"
    elif priority == "secondary":
        return "orange"
    elif priority == "tertiary":
        return "yellow"
    elif priority == "supporting":
        return "green"
    else:
        return None

class _serializable:
    """
    Base class for serializable objects. 
    
    Provides methods for converting to and from dictionaries, which can be easily serialized to `JSON`. 
    All data types within this file inherit from this class to ensure consistent serialization and deserialization behavior across the application.
    """
    @staticmethod
    def _serialize_value(value):
        if isinstance(value, _serializable):
            return value.to_dict()
        if isinstance(value, dict):
            return {key: _serializable._serialize_value(item) for key, item in value.items()}
        if isinstance(value, (list, tuple)):
            return [_serializable._serialize_value(item) for item in value]
        return value

    @classmethod
    def _deserialize_value(cls, value, annotation=None):
        if annotation is None:
            if isinstance(value, dict):
                return {key: cls._deserialize_value(item) for key, item in value.items()}
            if isinstance(value, list):
                return [cls._deserialize_value(item) for item in value]
            if isinstance(value, tuple):
                return tuple(cls._deserialize_value(item) for item in value)
            return value

        origin = get_origin(annotation)
        args = get_args(annotation)

        if origin in (list, tuple):
            item_annotation = args[0] if args else None
            return [cls._deserialize_value(item, item_annotation) for item in value]

        if origin is dict:
            value_annotation = args[1] if len(args) > 1 else None
            return {key: cls._deserialize_value(item, value_annotation) for key, item in value.items()}

        if isinstance(annotation, type) and issubclass(annotation, _serializable):
            return annotation.from_dict(value)

        return value

    def to_dict(self):
        data = {}
        for key, value in self.__dict__.items():
            output_key = "duration" if key == "_duration" else key
            data[output_key] = self._serialize_value(value)
        return data

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            raise TypeError(f"Expected a dictionary for {cls.__name__}.from_dict, got {type(data).__name__}")

        annotations = get_type_hints(cls.__init__)
        signature = inspect.signature(cls.__init__)
        kwargs = {}
        consumed = set()

        for param_name, parameter in signature.parameters.items():
            if param_name == "self":
                continue
            if parameter.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
                continue

            if param_name == "days" and param_name not in data and isinstance(data, dict) and data:
                kwargs[param_name] = cls._deserialize_value(data, annotations.get(param_name))
                consumed.add(param_name)
                continue

            if param_name == "_duration" and "duration" in data:
                kwargs[param_name] = cls._deserialize_value(data["duration"], annotations.get(param_name))
                consumed.add("duration")
                continue

            if param_name in {"city", "state", "country"} and "location" in data:
                location = data["location"]
                if isinstance(location, list) and len(location) >= 3:
                    normalized = {"city": location[0], "state": location[1], "country": location[2]}
                    kwargs[param_name] = cls._deserialize_value(normalized[param_name], annotations.get(param_name))
                    consumed.add("location")
                    continue

            if param_name in data:
                kwargs[param_name] = cls._deserialize_value(data[param_name], annotations.get(param_name))
                consumed.add(param_name)
                continue

            if parameter.default is inspect._empty:
                raise KeyError(f"Missing required field '{param_name}' when deserializing {cls.__name__}")

        instance = cls(**kwargs)

        for key, value in data.items():
            if key in consumed:
                continue
            if key == "location":
                continue
            setattr(instance, key, cls._deserialize_value(value))

        return instance

class PRTable(_serializable):
    def __init__(self, sport: str, pr_data: dict[str, float]):
        self.sport = sport
        self.pr_data = pr_data
        
    def __str__(self) -> str:
        pr_summary = ", ".join(f"{dist}: {time:.2f}s" for dist, time in self.pr_data.items())
        return f"PR Table for {self.sport}: {pr_summary}"

class Step(_serializable):
    """
    Class for a single step within an exercise.\n 
    Each step has a name, optional description, sport, type, duration in seconds, target heart rate zone (THRZ), and target rate of perceived exertion (TRPE).\n
    
    An example step could be::
    
        Step(name="Warm-up", description="A gentle warm-up before the main workout", sport="running", type="warm-up", duration=900, thrz=120, trpe=3),
        
    which represents a 15-minute warm-up at 120 bpm with a perceived effort of 3.
    """
    def __init__(
        self,
        name: str,
        desc: str | None,
        sport: str,
        type: str,
        _duration: int,
        thrz: int,
        trpe: int,
    ):
        self.name = name
        self.desc = desc
        self.sport = sport
        self.type = type
        self._duration = _duration
        self.thrz = thrz
        self.trpe = trpe

    def __str__(self) -> str: 
        return f"{self.name} | {self.sport} | {self.type} - {self.desc} for {self._duration // 3600} hours and {self._duration % 60} minutes at {color_text(self.thrz, _color_from_zone(self.thrz))} bpm (TRPE: {color_text(self.trpe, _color_from_trpe(self.trpe))})"
    def __repr__(self) -> str:
        return f"Step(name={self.name!r}, description={self.desc!r}, sport={self.sport!r}, type={self.type!r}, duration={self._duration!r}, thrz={self.thrz!r}, trpe={self.trpe!r})"
    def __eq__(self, other) -> bool:
        if not isinstance(other, Step):
            return NotImplemented
        return (
            self.name == other.name and
            self.desc == other.desc and
            self.sport == other.sport and
            self.type == other.type and
            self._duration == other._duration and
            self.thrz == other.thrz and
            self.trpe == other.trpe
        )
    def __hash__(self) -> int:
        return hash((self.name, self.desc, self.sport, self.type, self._duration, self.thrz, self.trpe))
   
    @property
    def duration(self):
        return self._duration
class Exercise(_serializable):
    """
    Class for an exercise, which consists of a name, optional description, type, and a list of steps.\n
    
    An example exercise could be::
    
        Exercise(name="Interval Training", description="High-intensity intervals with recovery periods", type="threshold", steps=...),
    
    which represents a threshold workout focused on interval training.
    """
    def __init__(
        self, 
        name: str, 
        desc: str | None,
        type: str,
        steps: list[Step]
    ):
        self.name = name
        self.desc = desc
        self.type = type
        self.steps: list[Step] = steps
    def __str__(self) -> str:
        return f"{self.name} | {self.type} \n {self.desc} \n --- \n Steps: {len(self.steps)} Duration: {self.duration // 3600} hours and {self.duration % 60} minutes"
    
    @property
    def step_count(self):
        return len(self.steps)
    
    @property
    def duration(self):
        return sum(step.duration for step in self.steps)
class Session(_serializable):
    """
    Class for a training session, which consists of a name, optional description, type, and a list of exercises.\n
    
    An example session could be::
    
        Session(name="Brick Session", description="Bike followed by a run", type="mixed", exercises=...),
        
    which represents a triathlon-specific brick workout.
    """
    def __init__(
        self,
        name: str,
        desc: str | None,
        type: str,
        exercises: list[Exercise],
        start_at: int, # Start time in seconds from the beginning of the day (e.g., 3600 for 1:00 AM)
    ):
        self.name = name
        self.desc = desc
        self.type = type
        self.exercises = exercises
        self.start_at = start_at
        self.end_at = start_at + self.duration
    def __str__(self) -> str:
        return f"{self.name} | {self.type} \n {self.desc} \n --- \n Exercises: {len(self.exercises)} Duration: {self.duration // 3600} hours and {self.duration % 60} minutes"

    @property
    def duration(self) -> int:
        """The total session duration in seconds."""
        return sum(exercise.duration for exercise in self.exercises)

    @property
    def exercise_count(self):
        """The total number of exercises in the session."""
        return len(self.exercises)
class LoggedSession(Session):
    """
    Class for a logged training session, inherited from `Session`\n
    """
    def __init__(
        self,
        name: str,
        desc: str | None,
        type: str,
        exercises: list[Exercise],
        started_at: int,
        ended_at: int,
        completed: bool,
        perceived_effort: int | None = None,
        notes: str | None = None,
    ):
        super().__init__(name=name, desc=desc, type=type, exercises=exercises)
        self.started_at = started_at
        self.ended_at = ended_at
        self.completed = completed
        self.perceived_effort = perceived_effort
        self.notes = notes

class DayPlan(_serializable):
    """
    Class for a daily training plan, which consists of a list of sessions.\n
    
    An example day plan could be:: 
        
        DayPlan(
            name='Z2 Run and Swim Sprints',
            sessions=[...]
        ),
        
    which represents a single day's worth of training sessions.
    """
    def __init__(self, name: str, day: str, sessions: list[Session]):
        self.name = name
        self.day = day
        self.sessions = sessions
    def __str__(self) -> str:
        return f"Day Plan: {len(self.sessions)} sessions, total duration {self.duration // 3600} hours and {self.duration % 60} minutes"
        
    @property
    def session_count(self):
        return len(self.sessions)
    
    @property
    def duration(self):
        return sum(session.duration for session in self.sessions)
    
    def append_session(self, session: Session):
        self.sessions.append(session)
    def insert_session(self, session: Session, index: int):
        self.sessions.insert(index, session)
    def remove_session(self, session_name: str):
        self.sessions = [s for s in self.sessions if s.name != session_name]
    def clear_sessions(self):
        self.sessions = []
class WeekPlan(_serializable):
    def __init__(
        self, 
        weeknum: int, # ISO week number (1-52)
        days: dict[str, list[Session]] | None = None
    ):
        self.weeknum = weeknum
        self.days = days or {day: [] for day in _DAYS}
    def __str__(self) -> str:
        total_sessions = self.session_count
        total_duration = self.duration
        return f"Week {self.weeknum} Plan: {total_sessions} sessions, total duration {total_duration // 3600} hours and {total_duration % 60} minutes"
    
    @property
    def session_count(self):
        return sum(len(sessions) for sessions in self.days.values())
    
    @property
    def duration(self):
        return sum(session.duration for sessions in self.days.values() for session in sessions)
    
    def append_session(self, day: str, session: Session):
        self.days[day.lower()].append(session)
    def insert_session(self, day: str, session: Session, index: int):
        self.days[day.lower()].insert(index, session)
    def remove_session(self, day: str, session_name: str):
        sessions = self.days.get(day.lower(), [])
        self.days[day.lower()] = [s for s in sessions if s.name != session_name]
        
    def get_day(self, day: str) -> list[Session]:
        return self.days.get(day.lower(), [])
    def clear_day(self, day: str):
        self.days[day.lower()] = []

    def to_json(self):
        return json.dumps(self.to_dict(), indent=4)
class TrainingBlock(_serializable):
    """Class for Training blocks, with name, focus, week duration"""
    def __init__(
        self,
        name: str,
        focus: str,
        duration_weeks: int,
        weeks: list[WeekPlan],
    ):
        self.name = name
        self.focus = focus
        self.duration_weeks = duration_weeks
        self.weeks = weeks
    def __str__(self) -> str:
        return f"{self.name} | Focus: {self.focus} | Duration: {self.duration_weeks} weeks \n Sessions: {sum(week.session_count for week in self.weeks)} Total Duration: {sum(week.duration for week in self.weeks) // 3600} hours and {self.duration % 60} minutes"
class SeasonPlan(_serializable):
    def __init__(
        self,
        year: int,
        training_blocks: list[TrainingBlock],
        events: list[Event],
    ):
        self.year = year
        self.training_blocks = training_blocks
        self.events = events
    def __str__(self) -> str:
        blocks_summary = "\n".join(str(block) for block in self.training_blocks)
        events_summary = "\n".join(str(event) for event in self.events)
        return f"Season Plan for {self.year}\nTraining Blocks:\n{blocks_summary}\n\nEvents:\n{events_summary}"
      
class Event(_serializable):
    def __init__(
        self,
        name: str,
        start_time: int, # Military Time (e.g. 1430)
        date: str,
        sport: str,
        city: str,
        state: str,
        country: str,
        distance: list[float] | None = None,
        priority: Literal["Primary", "Secondary", "Tertiary", "Supporting"] | None = None,
        notes: str | None = None,
    ):
        self.name = name
        self.start_time=start_time
        self.date = date
        self.sport = sport
        self.distance = distance
        self.location = [city, state, country]
        self.priority = priority
        self.notes = notes

class AthleteProfile(_serializable):
    def __init__(
        self,
        name: str,
        age: int,
        weight: float,
        height: float,
        sports: list[str],
        pr_tables: list[PRTable],
        level: Literal["Beginner", "Intermediate", "Advanced", "Elite", "Professional"] | None = None,
    ):
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height
        self.sports = sports
        self.pr_tables = pr_tables
        self.level = level
    def __str__(self) -> str:
        pr_summary = "\n".join(str(pr) for pr in self.pr_tables)
        return f"Athlete Profile: {self.name}, Age: {self.age}, Weight: {self.weight} kg, Height: {self.height} cm, Sports: {', '.join(self.sports)}, Level: {self.level}\nPR Tables:\n{pr_summary}"
class StudentAthleteProfile(AthleteProfile):
    def __init__(
        self,
        name: str,
        age: int,
        weight: float,
        height: float,
        sports: list[str],
        pr_tables: list[PRTable],
        level: Literal["Beginner", "Intermediate", "Advanced", "Elite", "Professional"] | None,
        school: str,
        graduation_year: int,
    ):
        super().__init__(
            name=name,
            age=age,
            weight=weight,
            height=height,
            sports=sports,
            pr_tables=pr_tables,
            level=level,
        )
        self.school = school
        self.graduation_year = graduation_year
    def __str__(self) -> str:
        base_profile = super().__str__()
        return f"{base_profile}\nStudent Athlete Profile: School: {self.school}, Graduation Year: {self.graduation_year}"


