# This is an example of a procedure.

from procedureapi import Procedure
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)

HYSTERESIS = 1.0

class Thermostat(Procedure):
    """Every procedure subclasses ProcedureAPI.
    The API is then accessible in self.api"""

    def __init__(self): self.api = None

    def init(self):
        """Any global initialization happens here."""
        self.is_on = False # State is preserved between invocations.

    def run(self):
        """The execution starts from the run method."""
        self.api.add_schedule(delay=60) # We reschedule ourselves in 60 seconds.
        temp = self.read_temp()
        self.api.log_info("Read temperature: %r" % temp)
        self.api.write_output('temp', temp)
        threshold = self.api.read_value('set temperature')
        self.is_on = temp < threshold + HYSTERESIS if self.is_on else temp < threshold - HYSTERESIS
        self.api.write_output('is_on', self.is_on)
        self.set_heating()

    def read_temp(self):
        """Here we read the temperature, e.g. via a network call or GPIO"""
        pass

    def set_heating(self):
        """Here we switch heater on/off according to self.is_on, e.g. via GPIO"""
        GPIO.output(12, self.is_on)
