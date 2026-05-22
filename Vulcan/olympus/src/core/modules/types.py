
from typing import Literal, get_args, get_origin, get_type_hints
import inspect
import json


def _insertJSON(PathToJSON: str, ContentDict: dict) -> None:
    """Inserts a dictionary into a `JSON` file. If the file does not exist, it creates it."""

    with open(PathToJSON, "w", encoding="utf-8") as JSONFile:
        json.dump(ContentDict, JSONFile, indent=4, sort_keys=True)


def _extractJSON(PathToJSON: str) -> dict | None:
    """Extracts a `JSON` file and returns the content as a dictionary."""

    try:
        with open(PathToJSON, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        return None


_DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]


class _Serializable:
    """
    Base class for serializable objects. 
    
    Provides methods for converting to and from dictionaries, which can be easily serialized to JSON. 
    All data types within this file inherit from this class to ensure consistent serialization and deserialization behavior across the application.
    """
    @staticmethod
    def _serialize_value(value):
        if isinstance(value, _Serializable):
            return value.to_dict()
        if isinstance(value, dict):
            return {key: _Serializable._serialize_value(item) for key, item in value.items()}
        if isinstance(value, (list, tuple)):
            return [_Serializable._serialize_value(item) for item in value]
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

        if isinstance(annotation, type) and issubclass(annotation, _Serializable):
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

class PRTable(_Serializable):
    def __init__(self, sport: str, pr_data: dict[str, float]):
        self.sport = sport
        self.pr_data = pr_data

class Step(_Serializable):
    def __init__(
        self,
        name: str,
        workout: str,
        _duration: int,
        thrz: int,
        trpe: int,
    ):
        self.name = name
        self.workout = workout
        self._duration = _duration
        self.thrz = thrz
        self.trpe = trpe

    def __str__(self):
        return f"{self.name} - {self.workout} for {self.duration} minutes at {self.thrz} bpm (TRPE: {self.trpe})"

    @property
    def duration(self):
        return self._duration
class Exercise(_Serializable):
    def __init__(self, name: str, steps: list[Step]):
        self.name = name
        self.steps: list[Step] = steps

    @property
    def stepcount(self):
        return len(self.steps)
class Session(_Serializable):
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
        return sum(step.duration for exercise in self.exercises for step in exercise.steps)

    @property
    def exercisecount(self):
        return len(self.exercises)
class LoggedSession(Session):
    def __init__(
        self,
        name: str,
        seshtype: str,
        exercises: list[Exercise],
        completed: bool,
        perceived_effort: int | None = None,
        notes: str | None = None,
    ):
        super().__init__(name=name, seshtype=seshtype, exercises=exercises)
        self.completed = completed
        self.perceived_effort = perceived_effort
        self.notes = notes

class DayPlan(_Serializable):
    def __init__(self, date: str, sessions: list[Session]):
        self.date = date
        self.sessions = sessions
class WeekPlan(_Serializable):
    def __init__(self, days: dict[str, list[Session]] | None = None):
        self.days: dict[str, list[Session]] = days or {day: [] for day in _DAYS}

    @property
    def sessioncount(self):
        return sum(len(sessions) for sessions in self.days.values())

    def add_session(self, day: str, session: Session):
        self.days[day.lower()].append(session)

    def get_day(self, day: str) -> list[Session]:
        return self.days.get(day.lower(), [])

    def to_json(self):
        return json.dumps(self.to_dict(), indent=4)

class Event(_Serializable):
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
        notes: str | None = None,
    ):
        self.name = name
        self.date = date
        self.type = type
        self.distance = distance
        self.location = [city, state, country]
        self.priority = priority
        self.notes = notes

class AthleteProfile(_Serializable):
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

class TrainingBlock(_Serializable):
    def __init__(
        self,
        name: str,
        focus: str,
        duration_weeks: int,
        sessions: list[Session],
    ):
        self.name = name
        self.focus = focus
        self.duration_weeks = duration_weeks
        self.sessions = sessions


