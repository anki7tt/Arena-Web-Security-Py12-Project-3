# Automated File Organizer

A Python command-line tool built to clean up unorganized folders (like Downloads or Desktop) by sorting files into categorized directories based on their extensions. It includes duplicate protection, preview mode, and activity logging.

---

## Features

- **Automatic Folder Creation**: Automatically creates target folders (`Images`, `Documents`, `Videos`, `Python Files`, `Others`) if they do not exist.
- **Categorization**:
  - `Images`: `.jpg`, `.png`, `.jpeg`
  - `Documents`: `.pdf`, `.docx`, `.txt`
  - `Videos`: `.mp4`, `.mkv`
  - `Python Files`: `.py`
  - `Others`: Any other file types (e.g., `.zip`, `.mp3`, `.csv`)
- **Safe Duplicate Handling**: If a file with the same name already exists in the destination folder, the tool renames the incoming file (e.g., `report_1.pdf`, `report_2.pdf`) instead of overwriting existing data.
- **Preview Mode (Bonus Challenge)**: Lets you inspect where files will go and what names they will take without making any changes on disk.
- **Activity Logging & Summary**: Records every moved file with a timestamp in `organizer_log.txt` and prints a final category breakdown report.
- **OOP Architecture**: Core logic is encapsulated inside the `FileOrganizer` class.

---

## Project Structure

```text
Project 3/
├── file_organizer.py      # Core FileOrganizer class and interactive CLI
├── main.py               # Main entry point
├── create_test_files.py  # Script to generate sample files for testing
├── test_organizer.py     # Automated unit test suite
└── README.md             # Project documentation
```

---

## How to Run

### 1. Requirements
- Python 3.8 or higher.
- Built entirely using standard library modules (`os`, `shutil`, `datetime`, `unittest`). No external dependencies or `pip install` required.

### 2. (Optional) Generate Test Files
To test the organizer on a dummy folder without risking personal files, run:
```bash
python create_test_files.py
```
This generates a folder named `test_downloads` filled with sample images, documents, videos, Python scripts, and miscellaneous files.

### 3. Run the Organizer
```bash
python main.py
```
*(or `python file_organizer.py`)*

1. Enter the folder path you want to organize (e.g., `test_downloads` or an absolute path like `C:/Users/User/Downloads`).
2. Select your desired option:
   - `1`: Preview mode (inspect without moving)
   - `2`: Organize files directly
   - `3`: Preview first, then confirm before moving
   - `4`: Cancel

### 4. Run Unit Tests
Run the automated test suite to verify file categorization, preview mode, duplicate protection, and logging:
```bash
python test_organizer.py
```

---

## Duplicate Protection Logic

When moving `notes.txt` into `Documents/`:
1. If `Documents/notes.txt` does not exist, the file is moved as `notes.txt`.
2. If `Documents/notes.txt` already exists, the tool checks `notes_1.txt`, `notes_2.txt`, etc., and saves the file under the first available filename.
3. Original files in the destination are never modified or overwritten.

---

## Log File Format

Each time files are organized, operations are appended to `organizer_log.txt` in the target folder:
```text
[2026-11-11 16:21:48] MOVED: C:/Users/Downloads/resume.pdf -> C:/Users/Downloads/Documents/resume.pdf
[2026-11-11 16:22:40] MOVED (RENAMED): C:/Users/Downloads/resume.pdf -> C:/Users/Downloads/Documents/resume_1.pdf
```

---

## Error Handling

- **Invalid folder paths**: Re-prompts the user if the entered directory does not exist or points to a single file.
- **Self-referential protection**: Ignores the log file (`organizer_log.txt`) and existing subdirectories during scanning.
- **Permission errors**: Catches and displays file-system exceptions during move and log write operations.
"# Arena-Web-Security-Py12-Project-3" 
