#다운로드폴더에서 uuid (드림핵폴더죽이기) 폴더 삭제하고파서 새 폴더에 다 집어넣기 
#클라우드 AI 모델이 로컬 Python 도구를 선택해서 사용하는 소형 파일 정리 에이전트

import os
import json
import shutil
import zipfile
import re #uuid관련
from pathlib import Path
from openai import OpenAI
from send2trash import send2trash


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY") #터미널에 setx로 값넣어
)

TARGET_FOLDER = Path(
    r"C:\Users\박지예\Downloads"
)

tools = [
    {
        "type": "function",
        "name": "find_dreamhack_items",
        "description": ("Find folders and ZIP files in Downloads "
            "whose names have UUID format."),
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False
        }
    },
    {
        "type":"function",
        "name":"delete_dreamhack_items",
        "description":(
            "Move confirmed UUID-named DreamHack items "
            "to the Windows Recycle Bin."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "item_names": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                }
            },
            "required": ["item_names"],
            "additionalProperties": False
        }
    }
]
 
UUID_PATTERN = re.compile(
    r"^[0-9a-fA-F]{8}-"
    r"[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{12}$"
)

BACKUP_FOLDER = TARGET_FOLDER / "DreamHack_삭제대기"
LOG_FILE = BACKUP_FOLDER / "move_log.json"


def is_uuid_name(item): #uuid 판별하는 함수
    # ZIP 파일이면 확장자를 제외한 이름을 검사
    name = item.stem if item.is_file() else item.name

    return bool(UUID_PATTERN.fullmatch(name))

def find_dreamhack_items():
    candidates = []

    for item in TARGET_FOLDER.iterdir():
        if not is_uuid_name(item):
            continue

        # 폴더 또는 ZIP 파일만 포함
        if item.is_dir():
            candidates.append({
                "name": item.name,
                "type": "압축 해제 폴더"
            })

        elif item.is_file() and item.suffix.lower() == ".zip":
            candidates.append({
                "name": item.name,
                "type": "ZIP 압축파일"
            })

    return json.dumps(
        candidates,
        ensure_ascii=False,
        indent=2
    )

def move_dreamhack_items(item_names):
    BACKUP_FOLDER.mkdir(exist_ok=True)

    moved = []

    for item_name in item_names:
        source = TARGET_FOLDER / item_name
        destination = BACKUP_FOLDER / item_name

        if not source.exists():
            continue

        if not is_uuid_name(source):
            continue

        if destination.exists():
            continue

        shutil.move(str(source), str(destination))

        moved.append({
            "original": str(source),
            "moved_to": str(destination)
        })

    with open(LOG_FILE, "w", encoding="utf-8") as file:
        json.dump(
            moved,
            file,
            ensure_ascii=False,
            indent=2
        )

    return json.dumps({
        "moved": [item["original"] for item in moved],
        "message": "삭제대기 폴더로 이동했습니다."
    }, ensure_ascii=False)


def ask_agent(user_command, previous_response_id=None):
    response = client.responses.create(
        model="gpt-4o-mini",

        instructions="""
You are a DreamHack cleanup agent.

Use find_dreamhack_items to find UUID-named folders and
UUID-named ZIP files in the Downloads folder.

Treat these items as DreamHack file candidates based only
on their UUID-formatted names. Do not inspect their contents.

First show all candidates to the user. Do not delete them
during classification.

Only use delete_dreamhack_items after the user explicitly
confirms that the displayed candidates should be deleted.

When deletion succeeds, explain that the items were moved
to the Windows Recycle Bin.
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
            if item.name == "find_dreamhack_items":
                result = find_dreamhack_items()
            elif item.name == "delete_dreamhack_items":
                arguments = json.loads(item.arguments)

                result = move_dreamhack_items(
                    arguments["item_names"]
                )
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
        user_command=input("\nYou: ")

        if user_command.lower()=="exit": break

        answer,previous_response_id=ask_agent(
            user_command,
            previous_response_id
        )
        print("\nAgent:")
        print(answer)
        print()


run_agent()



