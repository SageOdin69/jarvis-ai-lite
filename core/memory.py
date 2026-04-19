"""import json
import os

MEMORY_FILE = "data/memory.json"

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)"""

"""import json
import os

MEMORY_FILE = "data/memory.json"

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)


def update_memory_from_text(memory, text):
    text = text.lower()

    # 🎯 simple rules (safe start)
    if "my name is" in text:
        name = text.split("my name is")[-1].strip()
        memory["user_name"] = name

    elif "i like" in text:
        memory.setdefault("likes", []).append(text)

    elif "i am working on" in text:
        memory.setdefault("projects", []).append(text)

    elif "my goal is" in text:
        memory.setdefault("goals", []).append(text)

    return memory"""

import json
import os

MEMORY_FILE = "data/memory.json"


def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {
            "user_name": "Bibhu",
            "likes": [],
            "goals": [],
            "projects": []
        }

    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {
            "user_name": "Bibhu",
            "likes": [],
            "goals": [],
            "projects": []
        }


def save_memory(memory):
    os.makedirs("data", exist_ok=True)
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=4, ensure_ascii=False)

def extract_name(text):
    lower = text.lower().strip()

    if "my name is" in lower:
        start = lower.find("my name is") + len("my name is")
        name = text[start:].strip()
        return name if name else None

    return None

def normalize_spelling(text):
    words = text.split()

    # if user spells letters like B I B H U
    if all(len(w) == 1 for w in words):
        return "".join(words).upper()

    return text.upper()


def update_memory_from_text(memory, text):
    lower = text.lower().strip()

    if lower.startswith("my name is "):
        memory["user_name"] = text[11:].strip()

    elif lower.startswith("i like "):
        item = text[7:].strip()
        memory.setdefault("likes", [])
        if item and item not in memory["likes"]:
            memory["likes"].append(item)

    elif lower.startswith("my goal is "):
        goal = text[11:].strip()
        memory.setdefault("goals", [])
        if goal and goal not in memory["goals"]:
            memory["goals"].append(goal)

    elif lower.startswith("i am working on "):
        project = text[16:].strip()
        memory.setdefault("projects", [])
        if project and project not in memory["projects"]:
            memory["projects"].append(project)

    return memory