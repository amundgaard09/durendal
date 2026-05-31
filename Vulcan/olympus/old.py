"""
The `OLYMPUS` Console \n
The Olympus Interface is a tool for elite athletes to log their training, recovery, and overall well-being in a structured way. 
It provides a comprehensive overview of daily activities, training sessions, and upcoming events, 
allowing athletes to track their progress and make informed decisions about their training and recovery strategies. 

The interface is designed to be user-friendly and efficient, enabling athletes to quickly log their data and access neccesary tools for optimal performace.
"""

### ------------------------------------------------------------------ ###

### TODO:

### 1. Softcode schedule (session classes) and user entry of completed workouts in morning/evening log
### 2. Data analysis and visualization
### 3. Notifications and reminders
### 4. Event calendar and phases (build, peak, taper, recovery)
### 5. Weekly summary and reports (olympus performance index - OPI)

### ------------------------------------------------------------------ ###

# THRZ - Target Heart Rate Zone
# TRPE - Target Rate of Perceived Exertion

### ------------------------------------------------------------------ ###

SCHEDULEPATH, SESSIONFILE, SLEEP_SCORES, GOALS, LOGFILE, LOGPATH, EVENTFILE, SCHEDULE = (None for _ in range(8))

import sys, json, time, datetime, questionary
from awpc.src.types.color_dtypes import x_color_text as color_text
from awpc.src.unipy.uniCLI.uniCLI import clearTerminal as clearterminal

from vulcan.olympus.src import (
    Step,
    Exercise,
    Session,
    DayPlan,
    WeekPlan,
    Event,
)

def save_event(event: Event):
    events = load_events()
    events.append(event)

    with open(EVENTFILE, "w", encoding="utf-8") as f:
        json.dump([e.to_dict() for e in events], f, indent=4) 
def load_events() -> list[Event]:
    try:
        with open(EVENTFILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [Event.from_dict(e) for e in data]
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    
def save_session(session: Session):
    sessions = load_sessions()
    sessions.append(session)

    with open(SESSIONFILE, "w", encoding="utf-8") as f:
        json.dump(
            [s.to_dict() for s in sessions],
            f,
            indent=4
        )
def load_sessions() -> list[Session]:
    try:
        with open(SESSIONFILE, "r", encoding="utf-8") as f:
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
        with open(SCHEDULEPATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            for day in schedule.keys():
                if day in data:
                    schedule[day] = data[day]
                    return schedule
    except (FileNotFoundError, json.JSONDecodeError):
        return None
def edit_schedule():
    clearterminal()
    print(color_text("Schedule Editor", "cyan") + "\n")
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
            print(color_text("Invalid input. Try again.", "red"))

morninglogged: bool = False
eveninglogged: bool = False

def mainscreen():
    clearterminal()
    global morninglogged, eveninglogged
    datetime_now = datetime.datetime.now()
    datetime_str = get_current_datetime_str()
    date_str = datetime_now.strftime("%Y-%m-%d")
    
    try:
        with open(LOGPATH, "r") as f:
            lines = f.readlines()
            if lines:
                morninglogged, eveninglogged = False, False
                for line in lines: 
                    if line.startswith(f"M|{date_str}"):
                        morninglogged = True
                    if line.startswith(f"E|{date_str}"):
                        eveninglogged = True
       
    except FileNotFoundError:
        print("\n Log text file not found!")
    
    print(f"Olympus Interface - {datetime_str}" + "\n")
    print(color_text("Today's Schedule:", "green") + "\n")
    counter = 1
    
    for workout in SCHEDULE[datetime_now.strftime("%A").lower()]:
        print(color_text(f"{counter}. {workout}", "green"))
        counter += 1
    
    print("\n")
    morningcompletionstr = "COMPLETED" if morninglogged else "NOT COMPLETED"
    eveningcompletionstr = "COMPLETED" if eveninglogged else "NOT COMPLETED"

    selection: str = questionary.select(
        "Select an option:",
        choices = [
            f"Morning Log - {date_str} - {morningcompletionstr}",
            f"Evening Log - {date_str} - {eveningcompletionstr}",
            f"Weekly OPI Report - N.I.",
            f"Schedule Overview - N.I.",
            f"Events / Races - I.C.",
            f"Sessions",
            f"Race Calendar - I.C.",
            f"PR Tracker - I.C.",
            "Exit"
        ]).ask()
    
    match selection:
        case selection if selection.startswith("Morning Log"):
            morning_log()
        case selection if selection.startswith("Evening Log"):
            evening_log()
        case selection if selection.startswith("Weekly OPI Report"):
            weekly_opi_report()
        case selection if selection.startswith("Schedule Overview"):
            scheduleoverview() 
        case selection if selection.startswith("Events"):
            racecalendar()
        case selection if selection.startswith("Sessions"):
            sessionsoverview()
        case selection if selection.startswith("Race Calendar"):
            racecalendar()
        case selection if selection.startswith("PR Tracker"):
            pr_tracker()
        case "Exit":
            print(color_text("Exiting Olympus Interface. Goodbye!", "red"))
            sys.exit()
    
def morning_log():
    datetime_now = datetime.datetime.now()
    date_str = datetime_now.strftime("%Y-%m-%d %H:%M:%S")
    print(color_text(f"Morning Log - {date_str}", "cyan"))
    print("no functionality yet, returning to main screen...")
    time.sleep(2)
    mainscreen()
def evening_log():
    datetime_now = datetime.datetime.now()
    date_str = datetime_now.strftime("%Y-%m-%d %H:%M:%S")
    print(color_text(f"Evening Log - {date_str}", "cyan"))
    try:
        with open(LOGPATH, "r") as f:
            lines = f.readlines()
            if lines:
                for line in lines: 
                    if line.startswith(f"E|{date_str[:10]}"):  # Check for today's date in the log
                        print(color_text("Today's Log:", "yellow") + "\n")
                        log_details = line.strip().split("|")
                        print(f"Date: {log_details[1]}")
                        print(f"Completed Workouts: {log_details[2]}")
                        print(f"Daily Completion Score: {log_details[3]}")
                        print(f"Overall Day Score: {log_details[4]}")
                        print(f"Step Goal Met: {'Yes' if log_details[5] == 'True' else 'No'}")
                        print(f"Injury/Discomfort: {'Yes' if log_details[6] == 'True' else 'No'}")
                        print(f"Sleep Quality: {log_details[7]}")
                        print(f"Nutrition Rating: {log_details[8]}/10")
                        print(f"Mental Health Rating: {log_details[9]}/10")
                        print(f"Strength Feeling Rating: {log_details[10]}/10")
                        confirmed = questionary.confirm("Return?").ask()
                        if confirmed:
                            mainscreen()
            else:
                print("No logs found.")
    except FileNotFoundError:
        print("ERROR! Log file not found. No upcoming events to display.")
    
    
    counter = 1
    for workout in SCHEDULE[datetime_now.strftime("%A").lower()]:
        print(color_text(f"{counter}. Planned Workout: {workout}", "green"))
        counter += 1
    
    checklist = questionary.checkbox(
        "Select completed workouts:",
        choices=[workout for workout in SCHEDULE[datetime_now.strftime("%A").lower()]]
    )
    completed_workouts = checklist.ask()
    daily_completion_score = (len(completed_workouts) / len(SCHEDULE[datetime_now.strftime("%A").lower()])) * 100
    print(color_text(f"Daily Completion Score: {daily_completion_score:.2f}%", "green" if daily_completion_score >= 85 else "yellow" if daily_completion_score >= 50 else "red"))

    stepgoalbool = questionary.confirm("Did you meet your step goal today?").ask()
    injurybool = questionary.confirm("Did you experience any injuries or discomfort today?").ask()
    sleepquality = questionary.select(
        "How was your sleep quality?",
        choices=[
            "Excellent",
            "Good",
            "Fair",
            "Poor"
        ]
    ).ask()
    nutriscale: int = questionary.select(
        "Rate your nutrition today:",
        choices=[str(i) for i in range(1, 11)]
    ).ask()
    mentalscale: int = questionary.select(
        "Rate your mental health:",
        choices=[str(i) for i in range(1, 11)]
        ).ask()
    strenghtscale: int = questionary.select(
        "On a scale of 1-10, how strong did you feel today?",
        choices=[str(i) for i in range(1, 11)]
    ).ask()
    
    # 0 - 100 daily rating based on completion, step goal, injury, sleep, nutrition, mental health and strength
    dayscore: int = (stepgoalbool * 10 
    + (not injurybool) * 10 
    + (SLEEP_SCORES[sleepquality]) 
    + int(nutriscale) 
    + int(mentalscale) 
    + int(strenghtscale) 
    + round((daily_completion_score / 10)))
    print(color_text(f"Overall Day Score: {dayscore}/100", "green" if dayscore >= 85 else "yellow" if dayscore >= 50 else "red"))
    
    understood = questionary.confirm("Complete").ask()
    
    if understood:
        daystr = f"E|{date_str}|{', '.join(completed_workouts)}|{daily_completion_score:.2f}%|{dayscore}|{stepgoalbool}|{injurybool}|{sleepquality}|{nutriscale}|{mentalscale}|{strenghtscale}"
        writefile(LOGPATH, daystr)
        mainscreen()

def weekly_opi_report():
    clearterminal()
    print(color_text("Weekly OPI Report", "cyan") + "\n")
    print("not implemented yet, returning to main screen...")
    time.sleep(2)
    mainscreen()

def scheduleoverview():
    clearterminal()
    print(color_text("Schedule Overview", "cyan") + "\n")
    
    schedule = load_schedule()
    if schedule is None:
        print(color_text("Schedule is empty! \n", "red"))
        
    else:
        for day, workouts in schedule.items():
            print(color_text(f"{day.capitalize()}: {', '.join(workouts) if workouts else 'No workouts scheduled'}", "green"))
    
        print("\n")

    selection: str = questionary.select(
        "Select an option:",
        choices = [
            f"Edit Schedule",           
            f"Return",
        ]).ask()
    
    match selection:
        case selection if selection.startswith("Edit Schedule"):
            edit_schedule()
        case selection if selection.startswith("Return"):
            mainscreen()

def exercisebuilder():
    clearterminal()
    print(color_text("Exercise Builder", "cyan") + "\n")
    
    steps: list[Step] = []
    exercisename = questionary.text("Exercise Name:").ask()
    
    addsteps = questionary.confirm("Add steps to this exercise?").ask()
    newstep: Step
    firststepadded: bool = False
    
    while addsteps:
        stepadded = False
        clearterminal()
        print(color_text(f"Exercise Builder - {exercisename}", "cyan") + "\n")
        print(color_text(f"Added steps: {[step.name for step in steps]}", "green") + "\n")
        
        if not firststepadded: # Prevents copy option on first step before any steps exist
            copystep = False
        else: 
            copystep = questionary.confirm("Copy a previous step?").ask()
        
        if copystep:
            copystepname = questionary.select(
                "Select a step to copy:",
                choices=[step.name for step in steps]        ).ask()
        else:
            copystepname = None
            
        if copystepname:
            selected_step = next((s for s in steps if s.name == copystepname), None)
            if selected_step:
                stepworkout = selected_step.workout
                stepduration = selected_step.duration
                stepthrz = selected_step.thrz
                steptrpe = selected_step.trpe
                
                copiedstep = Step(
                    name=selected_step.name, 
                    workout=stepworkout,
                    duration=stepduration,
                    thrz=stepthrz,
                    trpe=steptrpe
                )
                
                steps.append(copiedstep)
                stepadded = True
            else:
                print(color_text("Selected step not found. Creating new step.", "yellow"))
        if stepadded:
            print(color_text(f"Step '{copystepname}' copied successfully!", "green"))
            time.sleep(2)
            continue
        else:
            stepname = questionary.text("Step Name:").ask()
            stepworkout = questionary.text("Step Workout Description:").ask()
            stepduration = ask_int("Step Duration (minutes):", 0)
            stepthrz = ask_int("Target HR Zone (1-5):", 1, 5)
            steptrpe = ask_int("Target RPE (1-10):", 1, 10)

            newstep = Step(
                name=stepname,
                workout=stepworkout,
                duration=stepduration,
                thrz=stepthrz,
                trpe=steptrpe
            )
        
            steps.append(newstep)
        
        addsteps = questionary.confirm("Add another step?").ask()
    
    newexercise = Exercise(
        name=exercisename,
        steps=steps
    )

    return newexercise
def sessionbuilder():
    clearterminal()
    print(color_text("Session Builder", "cyan") + "\n")
    print(color_text("New session:", "green") + "\n")
    
    exercises: list[Exercise] = []
    sessionname = questionary.text("Session Name:").ask()
    seshtype = questionary.select("Session Type:", choices=[GOALS[idx].capitalize() for idx, _ in enumerate(GOALS)]).ask()
    duration: int = 0  
    
    addexercises = questionary.confirm("Add exercises to this session?").ask()
    
    while addexercises:
        newexercise = exercisebuilder()
        exercises.append(newexercise)
        addexercises = questionary.confirm("Add another exercise?").ask()

    newsession = Session(
        name=sessionname,
        seshtype=seshtype,
        exercises=exercises,
    )
    
    save_session(newsession)
    print(color_text(f"Session '{newsession.name}' saved!", "green"))
    time.sleep(1)
    sessionsoverview()
def sessionviewer():
    clearterminal()
    print(color_text("Session Viewer", "cyan") + "\n")
    sessions = load_sessions()
    
    if not sessions:
        action = questionary.confirm(color_text("No sessions found. Build a new one?", "yellow")).ask()
        if action:
            sessionbuilder()
        else:
            mainscreen()
        return

    for session in sessions:
        print(color_text(f"Session: {session.name}", "green"))
        for exercise in session.exercises:
            print(color_text(f"  Exercise: {exercise.name}", "yellow"))
    print("\n")
    
    returnconfirmed = questionary.confirm("Return?").ask()
    if returnconfirmed:
        sessionsoverview()    
def sessionsoverview():
    clearterminal()
    print(color_text("Sessions Overview", "cyan") + "\n")
    selection: str = questionary.select(
        "Select an option:",
        choices = [
            "View Sessions",
            "Build Session", 
            "Edit Session",
            "Build Exercise",           
            "Return",
        ]).ask()
    match selection:
        case "View Sessions":
            sessionviewer()
        case "Build Session":
            sessionbuilder()
        case "Edit Session":
            sessioneditor()
        case "Build Exercise":
            exercisebuilder()
        case "Return":
            mainscreen()
def sessioneditor():
    clearterminal()
    print(color_text("Session Editor", "cyan") + "\n")
    print("not implemented yet, returning to main screen...")
    time.sleep(2)
    mainscreen()

def add_event():
    clearterminal()
    print(color_text("Add Event", "cyan") + "\n")
    name: str = questionary.text("Event Name:").ask()
    date: str = questionary.text("Event Date (DD-MM-YYYY):").ask()
    type: str = questionary.select("Event Type: ", choices=["Cycling", "Running", "Swimming", "Triathlon", "XC Ski", ]).ask()
    
    if type == "Triathlon":
        print(color_text("\n Enter distances for each discipline in kilometers.", "yellow") + "\n")
        swimdistance: float = questionary.text("Swim Distance:").ask()
        bikedistance: float = questionary.text("Bike Distance:").ask()
        rundistance: float = questionary.text("Run Distance:").ask()
        distance: list[float] = [swimdistance, bikedistance, rundistance]
        
    else:
        distance: float = questionary.text("Event Distance (Kilometers):").ask()
        
    rawlocation: str = questionary.text("Location (City - Country) :").ask()
    location: list = rawlocation.strip().split(" - ")
    priority: str = questionary.select("Priority", choices=["Primary", "Secondary", "Tertiary", "Supporting"]).ask()
    notes: str = questionary.text("Notes (Optional):").ask()
    
    new_event = Event(
        name=name,
        date=date,
        type=type,
        distance=distance,
        location=location,
        priority=priority,
        notes=notes if notes else None
    )
    
    save_event(new_event)
    print(color_text("Event successfully saved!", "green"))
    time.sleep(2)
    mainscreen()
    
def racecalendar():
    clearterminal()
        
    print(color_text("Race Calendar", "cyan") + "\n")
    print("Upcoming Events:" + "\n")
    
    events = sort_events_by_date(load_events())
    if not events:
        print(color_text("No upcoming events found. Add an event to get started!", "yellow") + "\n")
    else:
        for event in events:
            print("------------------------------")
            print(f"{event.name} - {event.date} - {event.type} - Priority:" + color_text(" "+event.priority, "red" if event.priority == "Primary" else "yellow" if event.priority == "Secondary" else "green" if event.priority == "Tertiary" else "cyan"))
            if isinstance(event.distance, list):
                print(color_text(f">>> Distances (km): Swim: {event.distance[0]}, Bike: {event.distance[1]}, Run: {event.distance[2]}", "yellow"))
            else:
                print(color_text(f">>> Distance (km): {event.distance}", "yellow"))
            print(color_text(f">>> Location: {', '.join(event.location) if event.location else 'N/A'}", "yellow"))
            if event.notes:
                print(color_text(f">>> Notes: {event.notes}", "yellow"))
        print("------------------------------")
    selection: str = questionary.select(
        "Select an option:",
        choices = [
            f"Add Event",           
            f"Return",
        ]).ask()
    match selection:
        case selection if selection.startswith("Add Event"):
            clearterminal()
            add_event()
        case selection if selection.startswith("Return"):
            mainscreen()

def pr_tracker():
    clearterminal()
    print(color_text("PR Tracker", "cyan") + "\n")
    choice = questionary.select(
        "Select an option:",
        choices=[
            "View PRs",
            "Add PR",
            "Return"
        ]
    ).ask()
    match choice:
        case "View PRs":
            clearterminal()
            print(color_text("PRs Overview", "cyan") + "\n")
            print("No functionality yet, returning to main screen...")
            time.sleep(2)
            mainscreen()
        case "Add PR":
            clearterminal()
            print(color_text("Add PR", "cyan") + "\n")
            print("No functionality yet, returning to main screen...")
            time.sleep(2)
            mainscreen()
        case "Return":
            mainscreen()

if __name__ == "__main__":
    mainscreen() 