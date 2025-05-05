# The class CarSimulator is a simple 2D vehicle simulator.
# The vehicle states are:
# - x: is the position on the x axis on a xy plane
# - y: is the position on the y axis on a xy plane
# - v is the vehicle speed in the direction of travel of the vehicle
# - theta: is the angle wrt the x axis (0 rad means the vehicle
#   is parallel to the x axis, in the positive direction;
#   pi/2 rad means the vehicle is parallel
#   to the y axis, in the positive direction)
# - NOTE: all units are SI: meters (m) for distances, seconds (s) for
#   time, radians (rad) for angles...
#
# (1)
# Write the method "simulatorStep", which should update
# the vehicle states, given 3 inputs:
#  - a: commanded vehicle acceleration
#  - wheel_angle: steering angle, measured at the wheels;
#    0 rad means that the wheels are "straight" wrt the vehicle.
#    A positive value means that the vehicle is turning counterclockwise
#  - dt: duration of time after which we want to provide
#    a state update (time step)
#
# (2)
# Complete the function "main". This function should run the following simulation:
# - The vehicle starts at 0 m/s
# - The vehicle drives on a straight line and accelerates from 0 m/s to 10 m/s
#   at a constant rate of 0.4 m/s^2, then it proceeds at constant speed.
# - Once reached the speed of 10 m/s, the vehicle drives in a clockwise circle of
#   roughly 100 m radius
# - the simulation ends at 100 s
#
# (3)
# - plot the vehicle's trajectory on the xy plane
# - plot the longitudinal and lateral accelerations over time

import math
import numpy as np
import matplotlib.pyplot as plt

class CarSimulator():
    def __init__(self, wheelbase, v0, theta0):
        # INPUTS:
        # the wheel base is the distance between the front and the rear wheels
        self.wheelbase = wheelbase
        self.x = 0
        self.y = 0
        self.v = v0
        self.theta = theta0

    def simulatorStep(self, a, wheel_angle, dt):
        self.v += a * dt
        self.theta += (self.v * math.tan(wheel_angle) / self.wheelbase) * dt
        self.x += self.v * math.cos(self.theta) * dt
        self.y += self.v * math.sin(self.theta) * dt


def main():
     wheelbase = 4  # arbitrary 4m wheelbase
     v0 = 0
     theta0 = 0
     simulator = CarSimulator(wheelbase, v0, theta0)
     dt = 0.1  # arbitrarily set the time step to 0.1 s

     simulation_time = 100
     num_simulation_steps = int(simulation_time / dt)

     time_points = np.zeros(num_simulation_steps)
     x_points = np.zeros(num_simulation_steps)
     y_points = np.zeros(num_simulation_steps)
     v_points = np.zeros(num_simulation_steps)
     a_long_points = np.zeros(num_simulation_steps)
     a_lat_points = np.zeros(num_simulation_steps)

     target_speed = 10
     acceleration = 0.4
     target_radius = 100

     for i in range(num_simulation_steps):
        time = i * dt
        time_points[i] = time
        
        # Determine acceleration command
        if simulator.v < target_speed:
            a_cmd = acceleration
        else:
            a_cmd = 0
        
        # Determine steering angle
        # When at target speed, drive in a circle of radius 100m
        if simulator.v >= target_speed:
            # For clockwise circle: wheel_angle = -arctan(wheelbase/radius)
            wheel_angle = -math.atan(simulator.wheelbase / target_radius)
        else:
            wheel_angle = 0  # straight
        
        # Store current state
        x_points[i] = simulator.x
        y_points[i] = simulator.y
        v_points[i] = simulator.v
        
        # Calculate longitudinal and lateral accelerations
        a_long = a_cmd
        
        # Lateral acceleration for circular motion = v²/r
        if wheel_angle != 0 and simulator.v > 0:
            # Radius of curvature = wheelbase / tan(wheel_angle)
            curve_radius = abs(simulator.wheelbase / math.tan(wheel_angle))
            a_lat = (simulator.v ** 2) / curve_radius
            if wheel_angle < 0:
                a_lat = -a_lat  # Direction depends on turn direction
        else:
            a_lat = 0
            
        a_long_points[i] = a_long
        a_lat_points[i] = a_lat

        # Update vehicle state
        simulator.simulatorStep(a_cmd, wheel_angle, dt)
        
     # Plot the trajectory
     plt.figure(figsize=(10, 8))

     plt.subplot(2, 1, 1)
     plt.plot(x_points, y_points)
     plt.title('Vehicle Trajectory')
     plt.xlabel('X Position (m)')
     plt.ylabel('Y Position (m)')
     plt.grid(True)
     plt.axis('equal')
    
     plt.subplot(2, 1, 2)
     plt.plot(time_points, a_long_points, label='Longitudinal Acceleration')
     plt.plot(time_points, a_lat_points, label='Lateral Acceleration')
     plt.title('Vehicle Accelerations')
     plt.xlabel('Time (s)')
     plt.ylabel('Acceleration (m/s²)')
     plt.legend()
     plt.grid(True)
    
     plt.tight_layout()
     plt.show()
            
            
if __name__ == "__main__":
    main()