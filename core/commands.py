import os
import webbrowser
import urllib.parse
import re
from datetime import datetime

from core.storage import get_drive_usage, get_largest_subfolders
from core.cleanup import analyze_drive, analyze_folder


def execute_command(text):
    text = text.lower().strip()

    # ---------- Open Apps ----------
    if "open notepad" in text:
        os.system("notepad")
        return "Opening Notepad."

    if "open calculator" in text:
        os.system("calc")
        return "Opening Calculator."

    if "open cmd" in text or "open command prompt" in text:
        os.system("start cmd")
        return "Opening Command Prompt."

    # ---------- Websites ----------
    if "open youtube" in text:
        webbrowser.open("https://youtube.com")
        return "Opening YouTube."

    if "open google" in text:
        webbrowser.open("https://google.com")
        return "Opening Google."

    if "open gmail" in text:
        webbrowser.open("https://mail.google.com")
        return "Opening Gmail."

    # ---------- Search ----------
    if text.startswith("search "):
        query = text.replace("search ", "", 1).strip()
        if query:
            url = "https://www.google.com/search?q=" + urllib.parse.quote(query)
            webbrowser.open(url)
            return f"Searching for {query}"

    # ---------- Time / Date ----------
    if "time" in text:
        return f"The time is {datetime.now().strftime('%I:%M %p')}"

    if "date" in text:
        return f"Today is {datetime.now().strftime('%d %B %Y')}"

    # ---------- System ----------
    if "shutdown pc" in text:
        return "Shutdown command detected. Please confirm manually."

    if "restart pc" in text:
        return "Restart command detected. Please confirm manually."

    # ---------- Cleanup Advisor FIRST ----------
    cleanup_words = [
        "analyze",
        "cleanup",
        "clean up",
        "what can i delete",
        "inspect",
        "report"
    ]
    if "inspect users" in text and "drive" in text:
        match = re.search(r"\b([cdefghijklmnopqrstuvwxyz])\b", text)

        if match:
            drive = match.group(1).upper()
            return analyze_folder(
                f"{drive}:\\Users",
                f"Users folder on {drive} drive."
            )

    if any(word in text for word in cleanup_words) and "drive" in text:
        match = re.search(r"\b([cdefghijklmnopqrstuvwxyz])\b", text)

        if match:
            drive_letter = match.group(1).upper()
            return analyze_drive(drive_letter)

    # ---------- Drive Commands ----------
    drive_letters = re.findall(r"\b([cdefghijklmnopqrstuvwxyz])\b", text)

    if drive_letters and "drive" in text:

        # remove duplicates
        seen = []
        for d in drive_letters:
            if d.upper() not in seen:
                seen.append(d.upper())

        scan_words = [
            "biggest",
            "taking",
            "eating",
            "full",
            "space",
            "storage",
            "folders",
            "scan"
        ]

        # Scan only first drive
        if any(word in text for word in scan_words):
            drive_letter = seen[0]

            path = f"{drive_letter}:\\"
            folders, error = get_largest_subfolders(path, top_n=10)

            if error:
                return f"I could not scan {drive_letter} drive."

            reply = [f"Biggest space users on {drive_letter} drive."]

            for item in folders:
                reply.append(f"{item['name']} {item['size']}")

            return " | ".join(reply)

        # Normal drive info
        replies = []

        for drive_letter in seen:
            try:
                info = get_drive_usage(drive_letter)

                replies.append(
                    f"{drive_letter} drive: "
                    f"{info['free']} free of {info['total']}"
                )
            except:
                replies.append(f"{drive_letter} drive unavailable")

        return " | ".join(replies)

    return None