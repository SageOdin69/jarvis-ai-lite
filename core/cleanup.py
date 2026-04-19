import subprocess
from pathlib import Path


def human(size):
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} PB"


def powershell_folder_disk_size(path_text):
    ps = rf"""
$path = "{path_text}"
$sum = 0

Get-ChildItem $path -Recurse -Force -ErrorAction SilentlyContinue |
Where-Object {{ -not $_.PSIsContainer }} |
ForEach-Object {{
    try {{
        $sum += $_.Length
    }} catch {{}}
}}

Write-Output $sum
"""

    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",
            timeout=180
        )

        return int(result.stdout.strip() or 0)

    except:
        return 0


def analyze_drive(drive_letter):
    drive = drive_letter.upper()
    root = Path(f"{drive}:\\")

    if not root.exists():
        return f"{drive} drive not found."

    items = []

    try:
        for item in root.iterdir():
            try:
                if item.is_symlink():
                    continue

                size = powershell_folder_disk_size(str(item))
                items.append((item.name, size))

            except:
                pass
    except:
        return f"Could not analyze {drive} drive."

    items.sort(key=lambda x: x[1], reverse=True)
    top = items[:10]

    report = [f"{drive} drive analysis (size on disk mode)."]

    total = 0

    for name, size in top:
        total += size
        report.append(f"{name}: {human(size)}")

    report.append(f"Top shown total: {human(total)}")
    report.append("No files deleted. Review manually.")

    return " | ".join(report)


def analyze_folder(path_text, title="Folder analysis"):
    path = Path(path_text)

    if not path.exists():
        return "Folder not found."

    items = []

    try:
        for item in path.iterdir():
            try:
                size = powershell_folder_disk_size(str(item))
                items.append((item.name, size))
            except:
                pass
    except:
        return "Could not inspect folder."

    items.sort(key=lambda x: x[1], reverse=True)
    top = items[:10]

    report = [title]

    for name, size in top:
        report.append(f"{name}: {human(size)}")

    return " | ".join(report)