# hardware/motor_interface.py


class Motor:
    """
    abstract interfaces of the real motor controlling the motion stage, i.e. what a motor must do.

    The beam finding algorithm will only use these methods.
    A real hardware implementation or a simulated version must follow this same interface.
    """

    def move_relative(self, distance: float) -> None:
        """
        Move the motor by a relative distance (in microns), relative to its current location.
        Distance can be both positive or negative to move in either direction.
        """
        raise NotImplementedError

    def move_absolute(self, location: float) -> None:
        """
        Move the motor to an absolute {location} (in microns).
        """
        raise NotImplementedError

    def get_position(self) -> float:
        """
        Return the current position of the motor. (in microns).
        """
        raise NotImplementedError

    def set_velocity(self, velocity: float) -> None:
        """
        Change the velocity of the motor, in microns per second.
        """
        raise NotImplementedError
