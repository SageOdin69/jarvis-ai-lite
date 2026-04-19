"""from core.brain import ask_ai
from core.voice import speak

def run_assistant():
    speak("Local Jarvis is ready.")

    messages = []

    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue

        if user_input.lower() in {"exit", "quit", "stop"}:
            speak("Goodbye.")
            break

        messages.append({"role": "user", "content": user_input})
        reply = ask_ai(messages)
        messages.append({"role": "assistant", "content": reply})
        speak(reply)"""
        
"""from core.brain import ask_ai
from core.voice import speak
from core.memory import load_memory, save_memory, update_memory_from_text
from core.listen import listen
import time

def run_assistant():
    speak("Local Jarvis is ready.")

    memory = load_memory()
    messages = []

    while True:
        user_input = listen()
        
        memory = update_memory_from_text(memory, user_input)
        save_memory(memory)

        if not user_input:
            continue

        if user_input.lower() in {"exit", "quit", "stop"}:
            speak("Goodbye.")
            break

        print("DEBUG: Got input")  # debug

        messages.append({"role": "user", "content": user_input})

        print("DEBUG: Calling AI...")  # debug
        #reply = ask_ai(messages)
        full_context = f""""""
        You are Jarvis, a friendly, witty, slightly teasing AI assistant.

        Personality:
        - Talk like a smart friend, not a robot
        - Be a little playful and teasing sometimes
        - Keep responses short and natural
        - Avoid being overly formal or technical
        - Do NOT say "I am a language model"

        Memory usage rules:
        - You KNOW the user's details but DO NOT mention them unless relevant
        - Only talk about user's goals if the question is related
        - Do NOT randomly bring up job, goals, or projects
        - Be subtle, not overeager

        Facts:
        - You run locally
        - You don’t have real-world experiences
        - Occasionally tease the user lightly, but never insult

        User info (use only when needed):
        Name: {memory.get("user_name")}
        Goals: {memory.get("goals")}
        Projects: {memory.get("projects")}
        """""""

        reply = ask_ai(
            [{"role": "system", "content": full_context}] + messages
        )
        print("DEBUG: AI replied")  # debug
        messages.append({"role": "assistant", "content": reply})

        print("DEBUG: Speaking now...")  # debug
        time.sleep(0.3)
        speak(reply)"""

import time
from core.brain import ask_ai
from core.voice import speak
from core.memory import load_memory, save_memory, update_memory_from_text, extract_name
from core.listen import listen
from core.commands import execute_command
from core.memory import extract_name,normalize_spelling


def run_assistant():
    speak("Local Jarvis is ready.")

    memory = load_memory()
    messages = []

    while True:
        user_input = listen()

        if not user_input:
            continue

        """if user_input.lower() in {"exit", "quit", "stop"}:
            speak("Goodbye.")
            break"""
        if any(x in user_input.lower() for x in [
            "what is my name",
            "what's my name",
            "tell my name",
            "my name"
        ]):
            name = memory.get("user_name", "I don't know yet")

            # clean formatting
            clean_name = name.replace("-", "").replace(" ", "")

            speak(f"Your name is {clean_name}")
            continue
        
        if any(x in user_input.lower() for x in [
            "exit", "quit", "stop", "bye", "goodbye", "shut down"
        ]):
            speak("Alright, shutting down.")
            break

        # First, try to extract a name and confirm it before saving
        name_candidate = extract_name(user_input)
        if name_candidate:
            speak(f"I heard {name_candidate}. Is that correct?")

            confirmation = listen()

            if confirmation and "yes" in confirmation.lower():
                clean_name = normalize_spelling(name_candidate)
                clean_name = clean_name.replace("-", "").replace(" ", "").upper()
                memory["user_name"] = clean_name
                save_memory(memory)
                speak(f"Got it. I’ll call you {clean_name}.")
            else:
                speak("Hmm… let's try again later.")

            continue

        if name_candidate:
            speak(f"Did you say your name is {name_candidate}?")
            confirmation = listen()

            if confirmation and "yes" in confirmation.lower():
                memory["user_name"] = name_candidate
                save_memory(memory)
                speak("Got it. I’ll remember that.")
            else:
                speak("Alright, tell me your name again clearly.")
            continue

        # Save other useful facts normally
        memory = update_memory_from_text(memory, user_input)
        save_memory(memory)

        command_response = execute_command(user_input)
        if command_response:
            speak(command_response)
            continue

        full_context = f"""
        You are Jarvis, a friendly, witty, slightly teasing AI assistant.

        Personality:
        - Talk like a smart friend, not a robot
        - Be a little playful and teasing sometimes
        - Keep responses short and natural
        - Avoid being overly formal or technical
        - Do NOT say "I am a language model"

        Memory rules:
        - You know the user's details
        - Only mention them if they are relevant
        - Do not randomly bring up goals, projects, or personal info
        - When answering questions about user's name, ALWAYS return it EXACTLY as stored.
        - Do NOT modify, shorten, or reformat the name.
        - If name is stored as "BIBHU", return exactly "BIBHU".

        Facts:
        - You run locally on a computer
        - You do not have real-world experiences

        User info:
        Name: {memory.get("user_name")}
        Likes: {memory.get("likes")}
        Goals: {memory.get("goals")}
        Projects: {memory.get("projects")}
        """

        messages.append({"role": "user", "content": user_input})

        print("DEBUG: Got input")
        print("DEBUG: Calling AI...")
        if "what is my name" in user_input.lower():
            speak(f"Your name is {memory.get('user_name')}")
            continue
        reply = ask_ai([{"role": "system", "content": full_context}] + messages)
        print("DEBUG: AI replied")
        print("DEBUG: Speaking now...")

        messages.append({"role": "assistant", "content": reply})

        time.sleep(0.2)
        speak(reply)