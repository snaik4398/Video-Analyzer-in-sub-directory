Here’s a polished **GitHub-style `README.md`** for your repository, with clean formatting, usage examples, badges, and best practices for developers.

---

## 📘 `README.md` (GitHub Version)

```markdown
# 🎞️ Video Metadata Analyzer

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

This tool recursively scans folders containing video files, extracts metadata (duration and size), and outputs:
- A structured `.json` report.
- A clean, human-readable `.txt` summary.

Ideal for archiving, auditing, or organizing video collections with structured metadata.



## 📂 Project Structure


📁 your-repo/
├── Dir/
│   └── main.py             # Main Python script
├── requirements.txt        # Project dependencies
├── README.md               # This documentation file
└── <video-folders>/        # Your video directories go here


## 🚀 Features

- 🔍 Recursively scans video files in all subdirectories.
- 📏 Extracts video duration and size using `moviepy`.
- 📄 Exports a JSON report and a text summary.
- 🧠 Human-readable size and time formatting via `humanize`.
- ✅ Graceful handling of unreadable/corrupt files.


````

## ⚙️ Installation

### ✅ Recommended

Install all dependencies using the provided `requirements.txt`:

```bash
pip install -r requirements.txt
```

## 🧰 Manual Dependency Installation

If needed, install manually:

```bash
pip install moviepy
pip install humanize
```

> These are the only required libraries.

---

## 🖥️ Usage

### 🔧 Step-by-Step

1. Ensure your videos are stored under a directory, e.g., `C:/transfer/Videos`.
2. Run the script via terminal:

```bash
python Dir/main.py C:/transfer/Videos
```

### 📝 Output

The script will generate:

* `Videos.json`: Structured report with all metadata.
* `Videos.txt`: Formatted summary report.

---

## 📦 Output Format

### Example (TXT)

```
sample_folder
  videos
  File                                               | Duration       | Size
  intro.mp4                                          | 32.1 s         | 4.3 MB
  part1.mkv                                          | 210.7 s        | 28.5 MB

  Total Duration: 0h 4m 2s
  Total Size: 32.8 MB

Overall Duration: 0h 4m 2s
Overall Size: 32.8 MB
```

---

## 🔍 How It Works

### 1. `collect_video_data(root_path)`

* Scans all folders under the root.
* Uses `moviepy` to get:

  * `duration` (in seconds)
  * `size` (in bytes)
* Builds JSON data for each folder.

### 2. `write_text_files_from_json(json_path)`

* Reads JSON data.
* Formats a clean `.txt` report for human review.

---

## 📜 requirements.txt

```txt
moviepy
humanize
```

---

## 🖥️ Optional Setup Scripts

### 🐧 For Linux/macOS (`install.sh`)

```bash
#!/bin/bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 🪟 For Windows (`install.bat`)

```bat
@echo off
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
```

---

## 📄 License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

---

## 👨‍💻 Author

**Sanjay Naik**
Feel free to open issues or PRs for suggestions or improvements.

```