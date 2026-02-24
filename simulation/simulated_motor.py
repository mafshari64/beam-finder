# simulation/simulated_motor.py

from hardware.motor_interface import Motor


class SimulatedMotor(Motor):
    """
    It Implements a simulated SLOW motor for testing.
   
    *** SLOW: One reading per motor move.
    
    This class follows the motor interface and behaves like
    a basic motion stage. It does not simulate acceleration
    and just updates position directly.

    Units are in microns, matching the interface definition.
    """

    def __init__(
        self,
        initial_position: float = 0.0,
        default_velocity: float = 1000.0,
    ):
        self._position = initial_position
        self._velocity = default_velocity

    def move_relative(self, distance: float) -> None:
        """
        Move the motor by a relative distance (microns).
        """
        self._position += distance

    def move_absolute(self, location: float) -> None:
        """
        Move the motor to an absolute position (microns).
        """
        self._position = location

    def get_position(self) -> float:
        """
        Return current motor position (microns).
        """
        return self._position

    def set_velocity(self, velocity: float) -> None:
        """
        change motor velocity (microns per second).
        """
        self._velocity = velocity