from processing.commands.command import DeviceCommand
from datetime import datetime


class TellTimeCommand(DeviceCommand):
    def __init__(self):
        super().__init__(
            "tell_time", "Tell Time", "Tells the user the current time.", []
        )

    def execute(self, parameters):
        super().execute(parameters)

        return datetime.now().strftime("%I:%M%p")
