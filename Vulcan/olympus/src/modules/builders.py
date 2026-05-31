"""
Builders for the various components of the system, such as exercises, sessions, day plans, week plans, and events.
"""

from src.modules.dtypes import (
    Step, 
    Exercise, 
    Session, 
    DayPlan, 
    WeekPlan, 
    Event,
    SeasonPlan,
    TrainingBlock,
    AthleteProfile,
    StudentAthleteProfile,
)

from awpc.src.types.color_dtypes import x_color_text as color_text
from questionary import select, text
from pathlib import Path
from json import JSONDecodeError, load, dump 

_JSON_ROOT = Path(__file__).parent.parent / "data" / "json"

_DAYS            = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
_MONTHS          = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]

_PRIORITY_LEVELS = ["primary", "secondary", "tertiary", "supporting"]
_ATHLETE_LEVELS  = ["beginner", "intermediate", "advanced", "elite", "professional"]

_EVENT_TYPES     = ["race", "competition", "training camp", "other"]

_MULTISPORTS: dict[str, tuple[str, ...]] = {
    "triathlon": ["swim", "bike", "run"], 
    "duathlon": ["run", "bike", "run"], 
    "aquathlon": ["swim", "run"],
    "aqua bike": ["swim", "bike"],
    "swimrun": ["swim", "run"],
    "brick": ["bike", "run"]
}

_SESSION_TYPES = [
    "warm-up", 
    "aerobic base", 
    "threshold",
    "tempo", 
    "VO2-MAX",
    "technique",  
    "top speed", 
    "strength - maximal", 
    "strength - explosive", 
    "strength - enduring", 
    "durability", 
    "recovery", 
    "mobility", 
    "plyometrics",
    "mental",
    "flexibility", 
    "breathwork", 
    "meditation", 
    "rest", 
    "mixed",
    "other"
]

_HR_ZONES: list[str] = ["1", "2", "3", "4", "5"]
_RPE_RANGE: list[str] = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

def _load_steps() -> list[Step]:
    try:
        with open(_JSON_ROOT / "steps.json", "r") as f:
            raw_load: list = load(f)
    except (FileNotFoundError, JSONDecodeError):
        return []

    if not isinstance(raw_load, list):
        return []

    saved_steps: list[Step] = []
    for step in raw_load:
        if not isinstance(step, dict):
            continue

        normalized_step = dict(step)
        if "duration" in normalized_step and "_duration" not in normalized_step:
            normalized_step["_duration"] = normalized_step.pop("duration")

        if "description" in normalized_step and "desc" not in normalized_step:
            normalized_step["desc"] = normalized_step.pop("description")

        saved_steps.append(Step(**normalized_step))

    return saved_steps
def _load_exercises() -> list[Exercise]:
    try:
        with open(_JSON_ROOT / "exercises.json", "r") as f:
            raw_load: list = load(f)
    except (FileNotFoundError, JSONDecodeError):
        return []

    if not isinstance(raw_load, list):
        return []

    saved_exercises: list[Exercise] = []
    for exercise in raw_load:
        if not isinstance(exercise, dict):
            continue

        normalized_exercise = dict(exercise)
        if "description" in normalized_exercise and "desc" not in normalized_exercise:
            normalized_exercise["desc"] = normalized_exercise.pop("description")

        if "steps" in normalized_exercise and isinstance(normalized_exercise["steps"], list):
            normalized_steps = []
            for step in normalized_exercise["steps"]:
                if not isinstance(step, dict):
                    continue

                normalized_step = dict(step)
                if "duration" in normalized_step and "_duration" not in normalized_step:
                    normalized_step["_duration"] = normalized_step.pop("duration")

                if "description" in normalized_step and "desc" not in normalized_step:
                    normalized_step["desc"] = normalized_step.pop("description")

                normalized_steps.append(Step(**normalized_step))
            normalized_exercise["steps"] = normalized_steps

        saved_exercises.append(Exercise(**normalized_exercise))

    return saved_exercises
def _load_sessions() -> list[Exercise]:
    try:
        with open(_JSON_ROOT / "sessions.json", "r") as f:
            raw_load: list = load(f)
    except (FileNotFoundError, JSONDecodeError):
        return []

    if not isinstance(raw_load, list):
        return []

    saved_sessions: list[Session] = []
    for session in raw_load:
        if not isinstance(session, dict):
            continue

        normalized_session = dict(session)
        if "description" in normalized_session and "desc" not in normalized_session:
            normalized_session["desc"] = normalized_session.pop("description")

        if "exercises" in normalized_session and isinstance(normalized_session["exercises"], list):
            normalized_exercises = []
            for exercise in normalized_session["exercises"]:
                if not isinstance(exercise, dict):
                    continue

                normalized_exercise = dict(exercise)
                if "duration" in normalized_exercise and "_duration" not in normalized_exercise:
                    normalized_exercise["_duration"] = normalized_exercise.pop("duration")

                if "description" in normalized_exercise and "desc" not in normalized_exercise:
                    normalized_exercise["desc"] = normalized_exercise.pop("description")

                normalized_exercises.append(Step(**normalized_exercise))
            normalized_session["steps"] = normalized_exercises

        saved_sessions.append(Exercise(**normalized_session))

    return saved_sessions

def _get_distances(_sport: str) -> list[float] | None:
    """
    Helper function to get distances for both single-sport events, multisport events and distanceless events.
    """
    
    if _sport is None:
        return None

    normalized_sport = _sport.lower().strip()
    
    # Returns none since the given sport was pure white-space
    if not normalized_sport: 
        return None

    if normalized_sport in _MULTISPORTS:
        distances: list[float] = []
        
        for sport_part in _MULTISPORTS[normalized_sport]:
            while True:
                raw_distance = text(f"Enter {sport_part} distance (leave blank if none):").ask()
                if raw_distance is None or raw_distance.strip() == "": return None
                try: distances.append(float(raw_distance)); break
                except ValueError: print(f"Only {color_text('floats', 'blue', Bold=True)} or {color_text('ints', 'blue', Bold=True)} are allowed!")
        
        return distances

    while True:
        raw_distance: str = text(f"Enter {_sport} distance (leave blank if none): ").ask()
        if raw_distance is None or raw_distance.strip() == "": return None
        try: return [float(raw_distance)]
        except ValueError: print(f"Only {color_text('floats', 'blue', Bold=True)} or {color_text('ints', 'blue', Bold=True)} are allowed!")

def cli_create_step() -> Step:
    """
    Create a new step via CLI.
    """
    step_name = text("Enter step name:").ask()
    step_desc = text("Enter step description (optional):").ask()
    sport = text("Enter sport (optional):").ask()
    step_type = select("Select step type:", choices=_SESSION_TYPES).ask()
    step_duration = text("Enter step duration in minutes (optional):").ask()
    step_thrz = select("Select step heart rate zone (optional):", choices=_HR_ZONES).ask()
    step_trpe = select("Select step RPE range (optional):", choices=_RPE_RANGE).ask() 
    
    new_step = Step(
        name=step_name, 
        desc=step_desc if step_desc else None,
        sport=sport if sport else None, # None means rest
        type=step_type,
        _duration=float(step_duration) * 60 if step_duration else None, # Minutes to seconds | None means no specified/optional duration or rest
        thrz=int(step_thrz),        
        trpe=int(step_trpe)
    )
    
    saved_steps = _load_steps()
    saved_steps.append(new_step)

    with open(_JSON_ROOT / "steps.json", "w") as f:
        dump([step.to_dict() for step in saved_steps], f, indent=4)

    return new_step
def cli_create_exercise() -> Exercise:
    """
    Create a new exercise via CLI. \n
    Automatically saves the exercise to the `exercises.json` file for future reuse.
    Also allows adding existing steps from `steps.json` to the exercise.
    """
    
    saved_steps = _load_steps()
        
    exercise_name = text("Enter exercise name:").ask()
    exercise_desc = text("Enter exercise description (optional):").ask()
    exercise_type = select("Select exercise type:", choices=_SESSION_TYPES).ask()
    exercise_steps: list[Step] = []
    
    while True:
        choice = select(
            "Select an option:", 
            choices=[
                "Build new step", 
                "Add a saved step", 
                "Finish exercise"
            ]).ask()
        
        if choice == "Build new step":
            step = cli_create_step()
            exercise_steps.append(step)
            saved_steps = _load_steps()
        
        elif choice == "Add a saved step":
            if not saved_steps:
                print("No saved steps found. Please build a new step.")
                continue
            
            step_names = [step.name for step in saved_steps]
            selected_step_name = select("Select a step to add:", choices=step_names).ask()
            selected_step_data = next(step for step in saved_steps if step.name == selected_step_name)
            exercise_steps.append(selected_step_data)
        
        elif choice == "Finish exercise":
            break
        
    new_exercise = Exercise(
        name=exercise_name, 
        desc=exercise_desc if exercise_desc else None,
        type=exercise_type,
        steps=exercise_steps
    )
    
    new_exercise_dict = new_exercise.to_dict()
    
    with open(_JSON_ROOT / "exercises.json", "r") as f:
        existing_exercises = load(f)
        existing_exercises.append(new_exercise_dict)
    
    with open(_JSON_ROOT / "exercises.json", "w") as f:
        dump(existing_exercises, f, indent=4)

    return new_exercise
def cli_create_session() -> Session:
    """
    Create a new session via CLI. \n
    Automatically saves the session to the `sessions.json` file for future reuse.
    Also allows adding existing exercises from `exercises.json` to the session.
    """
    
    saved_exercises = _load_exercises()
        
    session_name: str = text("Enter session name:").ask()
    session_desc: str = text("Enter session description (optional):").ask()
    session_type: str = select("Select session type:", choices=_SESSION_TYPES).ask()
    exercises: list[Exercise] = []
    
    while True:
        choice: str = select(
            "Select an option:", 
            choices=[
                "Build new exercise", 
                "Add a saved exercise", 
                "Finish session"
            ]).ask()
        
        if choice == "Build new exercise":
            exercise = cli_create_exercise()
            exercises.append(exercise)
        
        elif choice == "Add a saved exercise":
            if not saved_exercises:
                print("No saved exercises found. Please build a new exercise.")
                continue
            
            exercise_names = [exercise.name for exercise in saved_exercises]
            selected_exercise_name = select("Select an exercise to add:", choices=exercise_names).ask()
            selected_exercise_data = next(exercise for exercise in saved_exercises if exercise.name == selected_exercise_name)
            exercises.append(selected_exercise_data)
        
        elif choice == "Finish session":
            break
        
        else:
            print("What the fuck? Hackerman!")
        
    new_session = Session(
        name=session_name, 
        desc=session_desc if session_desc else None,
        type=session_type,
        exercises=exercises,
        start_at=None, # To be set in day plan builder
    )
    
    new_session_dict = new_session.to_dict()
    
    with open(_JSON_ROOT / "sessions.json", "r") as f:
        existing_sessions: list = load(f)
        existing_sessions.append(new_session_dict)
    
    with open(_JSON_ROOT / "sessions.json", "w") as f:
        dump(existing_sessions, f, indent=4)

    return new_session
def cli_create_day_plan() -> DayPlan:
    """
    Create a new day plan via CLI.
    """
    
    saved_sessions = _load_sessions()
    added_sessions = []    
    
    while True:
        choice: str = select(
            "Select an option:", 
            choices=[
                "Build new session", 
                "Add a saved session", 
                "Finish day plan"
            ]).ask()
        
        if choice == "Build new session":
            session = cli_create_session()
            added_sessions.append(session)
        
        elif choice == "Add a saved session":
            if not saved_sessions:
                print("No saved exercises found. Please build a new exercise.")
                continue
            
            session_names = [session.name for session in saved_sessions]
            selected_session_name = select("Select a session to add:", choices=session_names).ask()
            selected_exercise_data = next(session for session in saved_sessions if session.name == selected_session_name)
            added_sessions.append(selected_exercise_data)
        
        elif choice == "Finish day plan":
            break
        
        else:
            print("What the fuck? Hackerman!")
    
    _name: str = text("Enter name for day plan:").ask()
    
    day_plan = DayPlan(
        name=_name, 
        sessions=added_sessions
    )
    
    return day_plan
def cli_create_week_plan() -> WeekPlan:
    """
    Create a new week plan via CLI.
    """
    pass
def cli_create_training_block() -> TrainingBlock:
    """
    Create a new training block via CLI.
    """
    pass
def cli_create_event() -> Event:
    """
    Create a new event via CLI.
    """
    
    event_name: str = text("Enter Event name:").ask()
    start_time: int = int(text("Enter session start time (military time e.g. 1430):").ask())
    event_date: str = text("Enter Event Date (DD-MM-YYYY):").ask()
    event_sport: str = text("Enter Event Sport:").ask()
    event_city: str = text("Enter Event City:").ask()
    event_state: str = text("Enter Event State:").ask()
    event_country: str = text("Enter Event Country:").ask()
    event_distances = _get_distances(event_sport)
    event_priority: str = select("Select Event priority:", choices=_PRIORITY_LEVELS).ask()
    event_notes: str = text("Enter notes for Event (optional):").ask()
    
    new_event = Event(
        name=event_name,
        start_time=start_time,
        date=event_date,
        sport=event_sport,
        city=event_city,
        state=event_state,
        country=event_country,
        distance=event_distances,
        priority=event_priority,
        notes=event_notes,  
    )
    
    with open(_JSON_ROOT / "events.json", "r") as f:
        existing_events = load(f)
        existing_events.append(new_event.to_dict())
    
    with open(_JSON_ROOT / "events.json", "w") as f:
        dump(existing_events, f, indent=4)

    return new_event
def cli_create_season_plan() -> SeasonPlan:
    """
    Create a new training cycle via CLI.
    """
    pass
def cli_create_athlete_profile() -> AthleteProfile:
    """
    Create a new athlete profile via CLI.
    """
    pass
def cli_create_student_athlete_profile() -> StudentAthleteProfile:
    """
    Create a new student-athlete profile via CLI.
    """
    pass
    
def view_steps() -> None:
    """
    View all saved steps.
    """
def view_exercises() -> None:
    """
    View all saved exercises.
    """
def view_sessions() -> None:
    """
    View all saved sessions.
    """
def view_day_plans() -> None:
    """
    View all current day plans.
    """
def view_week_plan() -> None:
    """
    View the current week plan.
    """  
def view_event() -> None:
    """
    View upcoming events.
    """
def view_season_plan() -> None:
    """
    View the current and future season plans.
    """
def view_training_block() -> None:
    """
    View the current training block.
    """
def view_student_athlete_profile() -> None:
    """
    View the current student-athlete profile.
    """     
def view_athlete_profile(_student: bool = False) -> None:
    """
    View the current athlete profile.
    """
    if _student:
        view_student_athlete_profile()
    