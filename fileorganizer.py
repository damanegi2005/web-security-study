import os
import json
import shutil
from pathlib import Path
from openai import OpenAI


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

TARGET_FOLDER = Path(
    r"C:\Users\박지예\OneDrive\사진\문서"
)

tools = [
    {
        "type": "function",
        "name": "list_files",
        "description": "Get all file names in the target folder.",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "type": "function",
        "name": "move_useless_files",
        "description": (
            "Move files classified as useless "
            "into the 비유용 folder."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "file_names": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                }
            },
            "required": ["file_names"]
        }
    }
]


def list_files():
    file_names=[]

    for file in TARGET_FOLDER.iterdir():
        if file.is_file():
            file_names.append(file.name)
    return json.dumps(file_names,ensure_ascii=False)


def move_useless_files(file_names):
    useless_folder=TARGET_FOLDER / "비유용"
    useless_folder.mkdir(exist_ok=True)

    for file_name in file_names:
        original_file=TARGET_FOLDER / file_name
        new_location=useless_folder / file_name

        shutil.move(
            str(original_file),str(new_location)
        )
    return "비유용 파일 이동 완료"

def move_file(file_name, category):
    # 이동할 파일의 원래 경로를 만든다.
    # category 이름으로 목적지 폴더 경로를 만든다.
    # 목적지 폴더가 없으면 생성한다.
    # shutil.move()로 파일을 이동한다.
    # 실행 결과를 문자열로 반환한다.
    pass

def ask_agent(user_command, previous_response_id=None):
    response = client.responses.create(
        model="gpt-4o-mini",

        instructions="""
You are a simple file classification agent.

First, use list_files to inspect the target folder.

Classify the files into only two categories:
유용 and 비유용.

When showing the result, use this format:

[유용]
- file name
- file name

[비유용]
- file name
- file name

Do not move any files while classifying them.

Only use move_useless_files after the user
explicitly asks you to move the useless files.
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

            if item.name == "list_files":
                result=list_files()

            elif item.name == "move_useless_files":
                arguments = json.loads(item.arguments)

                result = move_useless_files(
                    arguments["file_names"])
                
            else:
                continue

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
            model="gpt-4o-mini",
            input=tool_outputs,
            tools=tools,
            previous_response_id=response.id
        )


def run_agent():
    print("file organization agent")
    print("종료하려면 exit 누르렴렴렴켘")

    previous_response_id = None

    while True:
        user_command=input("You: ")

        if user_command.lower()=="exit": break

        answer,previous_response_id=ask_agent(
            user_command,
            previous_response_id
        )
        print("\nAgent:")
        print(answer)
        print()


run_agent()



