"""
The `OLYMPUS` Console \n
The Olympus Interface is a tool for elite athletes to log their training, recovery, and overall well-being in a structured way. 
It provides a comprehensive overview of daily activities, training sessions, and upcoming events, 
allowing athletes to track their progress and make informed decisions about their training and recovery strategies. 

The interface is designed to be user-friendly and efficient, enabling athletes to quickly log their data and access neccesary tools for optimal performace.
"""

### ------------------------------------------------------------------ ###

### TODO:

### 1. Data analysis and visualization
### 2. Notifications and reminders
### 3. Training phases (build, peak, taper, recovery)
### 4. Weekly summary and reports (olympus performance index - OPI)

### ------------------------------------------------------------------ ###

# THRZ - Target Heart Rate Zone
# TRPE - Target Rate of Perceived Exertion

### ------------------------------------------------------------------ ###

EVENTS = "src\\data\\json\\events.json"
SESSIONS = "src\\data\\json\\sessions.json"
SCHEDULE = "src\\data\\json\\schedule.json"

### ------------------------------------------------------------------ ### 

import json, time, datetime, questionary

from awpc.src.types.color_dtypes import xColorText as colorText
from awpc.src.unipy.uniCLI.uniCLI import clearTerminal
from Vulcan.olympus.src.core.modules.types import (
    Step,
    Exercise,
    Session,
    DayPlan,
    WeekPlan,
    Event,)

### ------------------------------------------------------------------ ###

def save_event(event: Event):
    events = load_events()
    events.append(event)

    with open(EVENTS, "w", encoding="utf-8") as f:
        json.dump([e.to_dict() for e in events], f, indent=4) 
def load_events() -> list[Event]:
    try:
        with open(EVENTS, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [Event.from_dict(e) for e in data]
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    
def save_session(session: Session):
    sessions = load_sessions()
    sessions.append(session)

    with open(SESSIONS, "w", encoding="utf-8") as f:
        json.dump(
            [s.to_dict() for s in sessions],
            f,
            indent=4
        )
def load_sessions() -> list[Session]:
    try:
        with open(SESSIONS, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [Session.from_dict(s) for s in data]
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def sort_events_by_date(events: list[Event]) -> list[Event]:
    def parse_date(event: Event):
        try:
            return datetime.datetime.strptime(event.date, "%d-%m-%Y")
        except ValueError:
            return datetime.datetime.max  # Place invalid dates at the end

    return sorted(events, key=parse_date)

def load_schedule() -> dict[str, list[str]] | None:
    schedule = {
        "monday": [],
        "tuesday": [],
        "wednesday": [],
        "thursday": [],
        "friday": [],
        "saturday": [],
        "sunday": [],
    }
    
    try:
        with open(SCHEDULE, "r", encoding="utf-8") as f:
            data = json.load(f)
            for day in schedule.keys():
                if day in data:
                    schedule[day] = data[day]
                    return schedule
    except (FileNotFoundError, json.JSONDecodeError):
        return None
def edit_schedule():
    clearTerminal()
    print(colorText("Schedule Editor", "cyan") + "\n")
    print("not implemented yet, returning to main screen...")
    time.sleep(2)
    mainscreen()
    
def writefile(filepath: str, content: str) -> None:
    with open(filepath, 'a') as f:
        f.write(content + "\n")

def get_current_datetime_str() -> str:
    datetime_now = datetime.datetime.now()
    return datetime_now.strftime("%Y-%m-%d %H:%M:%S")

def ask_int(prompt: str, min_val: int | None = None, max_val: int | None = None) -> int:
    while True:
        try:
            value = int(questionary.text(prompt).ask())
            if min_val is not None and value < min_val:
                raise ValueError
            if max_val is not None and value > max_val:
                raise ValueError
            return value
        except (TypeError, ValueError):
            print(colorText("Invalid input. Try again.", "red"))


def mainscreen():
    pass

if __name__ == "__main__":
    mainscreen() 