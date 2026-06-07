"""
**The** `OLYMPUS` **Console** \n

The **Olympus Interface** is a tool for elite athletes to log their training, recovery, and overall well-being in a structured way. 
It provides a comprehensive overview of daily activities, training sessions, and upcoming events, 
allowing athletes to track their progress and make informed decisions about their training and recovery strategies. 

---

The interface is designed to be user-friendly and efficient, enabling athletes to quickly log their data and access neccesary tools for optimal performace.

Docs and other resources can be found in the [Durendal GitHub](https://github.com/amundgaard09/durendal/)
"""

### ------------------------------------------------------------------ ###
#|#                                                                    #|#
#|# TODO:                                                              #|#
#|#                                                                    #|#
#|# 1. Data analysis and visualization tools (charts, etc.)            #|#
#|# 2. Notifications and reminders                                     #|#
#|# 3. Training phases (build, peak, taper, recovery)                  #|#
#|# 4. Weekly summary and reports (olympus performance index - OPI)    #|#
#|# 5. Auto-generate training blocks based on goals & upcoming events  #|#
#|# 6. Integration with wearable devices and fitness apps ?            #|#
#|# 7. User authentication and profile management                      #|#
#|# 8. Data export and import (CSV, JSON)                              #|#
#|#                                                                    #|#
### ------------------------------------------------------------------ ###
#|#                                                                    #|#
#|# NOTE: ACRONYMS                                                     #|#
#|#                                                                    #|#
#|# HR(Z) - Heart Rate (Zone)                                          #|#
#|# THRZ  - Target Heart Rate Zone                                     #|#
#|# RPE   - Rate of Perceived Exertion (scale of 1-10)                 #|#
#|# TRPE  - Target Rate of Perceived Exertion                          #|#
#|# OPI   - Olympus Performance Index (performance metric)             #|#
#|#                                                                    #|#
### ------------------------------------------------------------------ ###

from durapy.src.types.color_dtypes import color_text as color_text
from durapy.src.unipy.uniCLI.uniCLI import clear_terminal

#from src.modules.dtypes import (
#    Step,
#    Exercise,
#    Session,
#    DayPlan,
#    WeekPlan,
#    TrainingBlock,
#    Event,
#    SeasonPlan,
#    AthleteProfile,
#    StudentAthleteProfile,
#    SeasonPlan,
#)

from src.modules.builders import (
    cli_create_event,
    cli_create_session,
    cli_create_day_plan,
    cli_create_week_plan,
    cli_create_season_plan,
    cli_create_training_block,
    cli_create_athlete_profile,
    cli_create_student_athlete_profile,
    
    view_steps,
    view_exercises,
    view_sessions,
    view_day_plans,
    view_week_plan,   
    view_event, 
    view_season_plan,
    view_training_block,
    view_athlete_profile,
    view_student_athlete_profile,
)

import json, time, datetime, questionary

### ------------------------------------------------------------------ ###

def console():
    pass

if __name__ == "__main__":
    clear_terminal()
    cli_create_event() 