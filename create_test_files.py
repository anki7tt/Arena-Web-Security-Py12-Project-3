import os


def generate_test_files(target_dir="test_downloads"):
    os.makedirs(target_dir, exist_ok=True)

    test_files = [
        "landscape.jpg",
        "profile.png",
        "avatar.jpeg",
        "resume.pdf",
        "project_report.docx",
        "meeting_notes.txt",
        "vacation_clip.mp4",
        "tutorial.mkv",
        "automation_script.py",
        "data_backup.zip",
        "theme_song.mp3",
        "records.csv",
        "notes_without_extension"
    ]

    for fname in test_files:
        file_path = os.path.join(target_dir, fname)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"Sample content for {fname}\n")

    print(f"Created {len(test_files)} test files in '{target_dir}'.")


if __name__ == "__main__":
    generate_test_files()
