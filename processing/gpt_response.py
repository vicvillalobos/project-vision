def gpt_natural_response(text):
    # Generates a prompt for OpenAI GPT, in the case the text has no commands and is merely conversational.
    pass


def gpt_command_response(command, response):
    # Generates a prompt for OpenAI GPT, in the case the text is the result of a command.
    # The idea is that the AI generates a natural text including the response of the command.
    # Example:
    # Command = "Tell current time", Response = "12:34PM"
    # Prompt => "{Prefix} Your instruction is: {command}. Your parameter is: {response}."
    # Text => "The current time is 12:34PM sir."
    pass
