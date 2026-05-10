"""
The `AmundWorks` `UniOps` module for Control and Operations tasks.
`UniOps` is built for tasks related to mechatronics control and operation tasks.
"""

import time

class ContinuousPIDController:
    """
    A very crude first iteration of the Continuous PID Controller algorithms from AmundWorks.
    """
    def __init__(self, kp, ki, kd, setpoint=0):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint

        self.integral = 0
        self.prev_error = 0
        self.prev_time = time.time()

    def update(self, measured_value):
        now = time.time()
        dt = now - self.prev_time

        error = self.setpoint - measured_value

        P = self.kp * error
        
        self.integral += error * dt
        I = self.ki * self.integral

        derivative = (error - self.prev_error) / dt if dt > 0 else 0
        D = self.kd * derivative

        self.prev_error = error
        self.prev_time = now

        return P + I + D 