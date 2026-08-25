import json
from openai import OpenAI
from pathlib import Path


client = OpenAI(
    api_key= )

SAVE_PATH = Path(
    r"C:\Users\박지예\OneDrive\바탕 화면\agent_notes.txt"
)

tools = [
    {
        "type": "web_search"
    },
    {
        "type": "function",
        "name": "save_to_notepad",
        "description": (
            "Save text to the user's notepad text file. "
            "Use this when the user asks to save, record, or memo something."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "The complete text that should be saved."
                }
            },
            "required": ["content"],
            "additionalProperties": False
        },
        "strict": True
    }
]


def save_to_notepad(content):
    with open(SAVE_PATH, "a", encoding="utf-8") as file:
        file.write(content)
        file.write("\n\n")

    return f"Successfully saved to {SAVE_PATH}"


def ask_agent(user_command, previous_response_id=None):
    response = client.responses.create(
        model="gpt-4o-mini",

        instructions="""
You are an AI agent helping a third-year cybersecurity student
at Ewha Womans University.

When necessary, search the web yourself before answering.

Prioritize information from:
- Ewha Career Development Center
- Ewha Office of International Affairs
- Ewha College of Artificial Intelligence
- Ewha Department of Cyber Security
- Ewha Department of Computer Science and Engineering

Find internships, competitions, educational programs,
research opportunities, conferences, and other useful activities.

Check whether the information is still current.
Never invent deadlines or qualifications.
Always include the source link.
If the user requests a maximum number, follow that limit.
Answer in the same language as the user's command. please give the information that is available now as well. and simple answer plz.
""",

        input=user_command,
        tools=tools,
        previous_response_id=previous_response_id
    )
    
    while True:
        tool_outputs = []

        for item in response.output:
            if item.type != "function_call":
                continue

            if item.name == "save_to_notepad":
                arguments = json.loads(item.arguments)
                result = save_to_notepad(arguments["content"])

                tool_outputs.append(
                    {
                        "type": "function_call_output",
                        "call_id": item.call_id,
                        "output": result
                    }
                )

        if not tool_outputs:
            return response.output_text, response.id

        response = client.responses.create(
            model="gpt-5.6-luna",
            instructions="""
Tell the user whether the requested action was completed.
Answer in the same language as the user.
""",
            input=tool_outputs,
            tools=tools,
            previous_response_id=response.id
        )




def run_agent():
    print("Ewha Activity AI Agent")
    print("Type 'exit' to finish.\n")

    previous_response_id = None

    while True:
        user_command = input("You: ")

        if user_command.lower() == "exit":
            print("Agent terminated.")
            break

        try:
            answer, previous_response_id = ask_agent(
                user_command,
                previous_response_id
            )

            print("\nAgent:")
            print(answer)
            print()

        except Exception as error:
            print("\nError:", error)
            print()


run_agent()