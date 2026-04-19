import os
import shutil
from pathlib import Path


def human_readable_size(num_bytes):
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if num_bytes < 1024:
            return f"{num_bytes:.2f} {unit}"
        num_bytes /= 1024
    return f"{num_bytes:.2f} PB"


def get_drive_usage(drive_letter):
    drive = f"{drive_letter.upper()}:\\"

    usage = shutil.disk_usage(drive)

    total = human_readable_size(usage.total)
    used = human_readable_size(usage.used)
    free = human_readable_size(usage.free)

    percent_used = (usage.used / usage.total) * 100

    return {
        "drive": drive_letter.upper(),
        "total": total,
        "used": used,
        "free": free,
        "percent_used": round(percent_used, 2)
    }


def folder_size(path):
    total = 0

    for root, dirs, files in os.walk(path):
        for file in files:
            try:
                fp = os.path.join(root, file)
                total += os.path.getsize(fp)
            except:
                pass

    return total


def get_largest_subfolders(path, top_n=10):
    items = []

    try:
        for item in Path(path).iterdir():
            try:
                if item.is_dir():
                    size = folder_size(item)
                else:
                    size = item.stat().st_size

                items.append((item.name, size))
            except:
                pass

        items.sort(key=lambda x: x[1], reverse=True)

        result = []
        for name, size in items[:top_n]:
            result.append({
                "name": name,
                "size": human_readable_size(size)
            })

        return result, None

    except Exception as e:
        return [], str(e)