from openai import OpenAI
from processing.list import COMMAND_INFO
import config, json

ROLE_FUNCTION = "function"
ROLE_USER = "user"
ROLE_ASSISTANT = "assistant"
ROLE_SYSTEM = "system"


class GPTAgent:
    def __init__(self, role, context, chain_length=0):
        self.context = context
        self.chain_length = chain_length
        self.role = role

        self.chain = []

    def add_to_chain(self, role, message):
        self.chain.append({"role": role, "content": message})
        if len(self.chain) > self.chain_length:
            # Remove first (oldest) element
            self.chain.pop(0)

    def ask(self, client, question):
        completion = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": ROLE_SYSTEM, "content": self.context},
                *self.chain,
                {"role": ROLE_USER, "content": question},
            ],
        )

        self.add_to_chain(ROLE_USER, question)

        response = completion.choices[0].message.content

        self.add_to_chain(self.role, response)

        # print(completion)
        return response


class GPTManager:
    def __init__(self, name):
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)

        self.command_agent = GPTAgent(
            ROLE_FUNCTION,
            f"""You are a technical interpreter, you must interpret the user's input and extract the command they may want to execute. 
                You are not to talk to the user, only to a computer. Your responses must be in JSON with the following format: 
                {{\"command\": \"command_id\", \"parameters\": {{\"parameter1\": \"value1\", \"parameter2\": \"value2\"}}}}
                Do not say anything but the generated JSON. The available commands are the following: 

                {COMMAND_INFO.values()}

                If no listed command is inferred from the user input, respond with {{\"command\": \"none\"}}.
                Please mind as the user may say the words from a command without wanting to execute it, so you must be careful to only execute the command if it is explicitly requested.
                The user said the following, please respond:
                """,
        )

        self.chat_agent = GPTAgent(
            ROLE_ASSISTANT,
            f"""You are an AI assistant called {name}. You must help the user with their tasks in the most efficient way possible, but you must be always polite and respectful. 
            You may always address the user by 'Sir'. You may mantain your replies as short as possible. If a command was executed, try not to bother the user with the command's context, just inform the result.
            Your responses are being translated to speech and transmitted to the user via a speaker, DO NOT use special formatting or special content such as code blocks, since those aren't effective via audio.
            Instead of showing code to the user, you may explain the code in a simple way. 
            At the end of your response, you must ask the user if they require anything else (Unless the user is saying goodbye).
            The user asked you the following, please respond: """,
            chain_length=5,
        )

    def ask(self, user_prompt):
        command_detection = self.command_agent.ask(self.client, user_prompt)

        try:
            command_response = json.loads(command_detection)
            print("Command agent response: ", command_response)
            command_id = command_response["command"]
            if command_id == "none":
                return self.chat_agent.ask(self.client, user_prompt)

            command = COMMAND_INFO[command_id]

            # If the command is valid, we execute it and return the response
            response = command.execute(command_response["parameters"])

            return self.chat_agent.ask(
                self.client,
                f"A command was executed as requested by the user. The command description is '{command.description}' and the response was '{response}'. Please inform the user accordingly.",
            )

        except:
            # If something throws an exception, we respond with the chat agent
            return self.chat_agent.ask(
                self.client,
                "The device couldn't execute the inferred command. " + user_prompt,
            )
