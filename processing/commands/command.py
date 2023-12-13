class DeviceCommand:
    # Generic Command class to be executed on this device. Each command will extend this class,
    # have an id, name, description, and parameters. The command will be executed by calling the execute() method.

    def __init__(self, id, name, description, parameters):
        self.id = id
        self.name = name
        self.description = description
        self.parameters = parameters

    def validate_parameters(self, parameters):
        # Validates that the given parameters fulfill the requirements of this command.
        # Basically we check that the parameters given here are a dict with the same keys as the parameters of this object.

        # First check that the parameters are a dict
        if not isinstance(parameters, dict):
            raise Exception(
                f"Parameters for command '{self.id}' must be a dict, not a {type(parameters)}"
            )

        # Then check that the parameters have the same keys as this object's parameters
        for key in self.parameters:
            if key not in parameters:
                raise Exception(
                    f"Missing parameter '{key}' in parameters for command '{self.id}'"
                )

        return True

    def execute(self, parameters):
        # Executes the command with the given parameters.
        # This method should be overridden by each command.
        self.validate_parameters(parameters)
        pass

    def __str__(self):
        return f"Command {self.id}: {self.name}\n{self.description}\nParameters: {self.parameters}\n\n"

    def __repr__(self):
        return self.__str__()
