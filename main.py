import os
import json
import sys
from pathlib import Path
from moviepy.editor import VideoFileClip
import humanize
import re

root_dir = sys.argv[1]
VIDEO_EXTENSIONS = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv']

def sort_key_by_filename(video):
    match = re.match(r"(\d+)", video["file"])
    return int(match.group(1)) if match else float('inf')

def get_video_info(file_path):
    print(f"  → Extracting info from: {file_path}")
    try:
        clip = VideoFileClip(str(file_path))
        duration = clip.duration
        size = os.path.getsize(file_path)
        clip.close()
        print(f"    ✓ Success: duration={round(duration,2)}s, size={humanize.naturalsize(size)}")
        return round(duration, 2), size
    except Exception as e:
        print(f"    ✗ Error reading file: {file_path} → {e}")
        return None, 0

def collect_video_data(root_path):
    root_path = Path(root_path)
    all_data = {}

    print(f"🔍 Scanning top-level directory: {root_path}")

    for folder in root_path.iterdir():
        if folder.is_dir():
            print(f"\n📁 Processing folder: {folder.name}")
            folder_data = {
                "videos": [],
                "total_duration": 0.0,
                "total_size": 0
            }

            for subdir, _, files in os.walk(folder):
                for file in files:
                    file_path = Path(subdir) / file
                    if file_path.suffix.lower() in VIDEO_EXTENSIONS:
                        duration, size = get_video_info(file_path)
                        if duration is not None:
                            rel_path = str(file_path.relative_to(folder))
                            folder_data["videos"].append({
                                "file": rel_path,
                                "duration": duration,
                                "size": size
                            })
                            folder_data["total_duration"] += duration
                            folder_data["total_size"] += size

            if folder_data["videos"]:
                # Sort videos numerically by filename
                folder_data["videos"].sort(key=sort_key_by_filename)
                all_data[folder.name] = folder_data
                print(f"  → Found {len(folder_data['videos'])} video(s)")
            else:
                print(f"  ⚠ No video files found in {folder.name}")

    folder_name = Path(root_dir).name
    json_filename = f"{folder_name}.json"
    json_path = root_path / json_filename

    # Wrap in outer folder name
    wrapped_data = {folder_name: all_data}

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(wrapped_data, f, indent=2)

    print(f"\n📄 JSON data saved to {json_path}")
    return wrapped_data

def write_text_files_from_jsonOld(json_path):
    print(f"\n📄 Reading JSON: {json_path}")
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    base_path = Path(json_path).parent
    folder_name = list(data.keys())[0]  # The outer key
    all_folders = data[folder_name]

    lines = [f"{folder_name} : {{"]

    for folder, folder_data in all_folders.items():
        lines.append(f'\n  "{folder}": {{')
        lines.append(f'    "videos": [')

        for idx, video in enumerate(folder_data["videos"]):
            size_readable = humanize.naturalsize(video["size"])
            lines.append(f'      {{')
            lines.append(f'        "file": "{video["file"]}",')
            lines.append(f'        "duration": {video["duration"]},')
            lines.append(f'        "size": {video["size"]}  // {size_readable}')
            lines.append(f'      }}{"," if idx < len(folder_data["videos"]) - 1 else ""}')

        lines.append(f'    ],')

        total_seconds = int(folder_data["total_duration"])
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        total_size = humanize.naturalsize(folder_data["total_size"])

        lines.append(f'    "total_duration": "{hours}h {minutes}m {seconds}s",')
        lines.append(f'    "total_size": "{total_size}"')
        lines.append(f'  }}{"," if folder != list(all_folders.keys())[-1] else ""}')

    lines.append("}")

    output_file = base_path / f"{folder_name}.txt"
    with open(output_file, "w", encoding="utf-8") as out:
        out.write("\n".join(lines))

    print(f"  ✓ File created: {output_file}")



def write_text_files_from_json(json_path):
    print(f"\n📄 Reading JSON: {json_path}")
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    base_path = Path(json_path).parent
    folder_name = list(data.keys())[0]
    all_folders = data[folder_name]

    lines = []
    overall_seconds = 0
    overall_bytes = 0

    for section_name, folder_data in all_folders.items():
        lines.append(f"{section_name}")
        lines.append("  videos")
        lines.append("  {:<50} | {:<9} | {}".format("File", "Duration", "Size"))

        for video in folder_data["videos"]:
            size_human = humanize.naturalsize(video["size"])
            lines.append("  {:<80} | {:<15} | {}".format(
                video["file"], f"{video['duration']} s", size_human
            ))

            

        total_sec = int(folder_data["total_duration"])
        h = total_sec // 3600
        m = (total_sec % 3600) // 60
        s = total_sec % 60
        total_size_human = humanize.naturalsize(folder_data["total_size"])

        lines.append("")
        lines.append(f"  Total Duration: {h}h {m}m {s}s")
        lines.append(f"  Total Size: {total_size_human}")
        lines.append("")

        overall_seconds += total_sec
        overall_bytes += folder_data["total_size"]

    h = overall_seconds // 3600
    m = (overall_seconds % 3600) // 60
    s = overall_seconds % 60
    total_size_human = humanize.naturalsize(overall_bytes)

    lines.append("Overall Duration: {}h {}m {}s".format(h, m, s))
    lines.append(f"Overall Size: {total_size_human}")

    output_file = base_path / f"{folder_name}.txt"
    with open(output_file, "w", encoding="utf-8") as out:
        out.write("\n".join(lines))

    print(f"  ✓ File created: {output_file}")


# 🏁 Run the script
video_data = collect_video_data(root_dir)
folder_name = Path(root_dir).name
json_filename = f"{folder_name}.json"
json_path = Path(root_dir) / json_filename
write_text_files_from_json(json_path)
