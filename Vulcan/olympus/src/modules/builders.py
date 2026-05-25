"""
Builders for the various components of the system, such as exercises, sessions, day plans, week plans, and events.
"""

from dtypes import (
    Step, 
    Exercise, 
    Session, 
    DayPlan, 
    WeekPlan, 
    TrainingBlock,
    Event
)

from questionary import confirm, select, text
from pathlib import Path
import json

_JSON_ROOT = Path(__file__).parent.parent / "data" / "json"

_DAYS            = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
_MONTHS          = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]

_PRIORITY_LEVELS = ["primary", "secondary", "tertiary", "supporting"]
_ATHLETE_LEVELS  = ["beginner", "intermediate", "advanced", "elite", "professional"]

_EVENT_TYPES     = ["race", "competition", "training camp", "other"]
_SESSION_TYPES   = ["warm-up", "aerobic base", "threshold", "VO2-MAX", "top speed", "tempo", "technique", "maximal strength", "explosive strength", "enduring strength", "durability", "recovery", "mobility", "flexibility", "breathwork", "meditation", "rest", "mixed", "other"]

_HR_ZONES: list[str] = ["1", "2", "3", "4", "5"]
_RPE_RANGE: list[str] = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]


def _load_saved_steps() -> list[Step]:
    try:
        with open(_JSON_ROOT / "steps.json", "r") as f:
            raw_load = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
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
    
    saved_steps = _load_saved_steps()
    saved_steps.append(new_step)

    with open(_JSON_ROOT / "steps.json", "w") as f:
        json.dump([step.to_dict() for step in saved_steps], f, indent=4)

    return new_step

def cli_create_exercise() -> Exercise:
    """
    Create a new exercise via CLI.\n
    Automatically saves the exercise to the `exercises.json` file for future reuse.
    Also allows adding existing steps from `steps.json` to the exercise.
    """
    
    saved_steps = _load_saved_steps()
        
    exercise_name = text("Enter exercise name:").ask()
    exercise_desc = text("Enter exercise description (optional):").ask()
    step_type = select("Select exercise type:", choices=_SESSION_TYPES).ask()
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
            saved_steps = _load_saved_steps()
        
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
        type=step_type,
        steps=exercise_steps
    )
    
    new_exercise_dict = new_exercise.to_dict()
    
    with open(_JSON_ROOT / "exercises.json", "r") as f:
        existing_exercises = json.load(f)
        existing_exercises.append(new_exercise_dict)
    
    with open(_JSON_ROOT / "exercises.json", "w") as f:
        json.dump(existing_exercises, f, indent=4)

    return new_exercise

NewExercise = cli_create_exercise()

print(NewExercise)