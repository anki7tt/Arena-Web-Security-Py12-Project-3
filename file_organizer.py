import os
import shutil
from datetime import datetime


class FileOrganizer:
    CATEGORIES = {
        'Images': ['.jpg', '.png', '.jpeg'],
        'Documents': ['.pdf', '.docx', '.txt'],
        'Videos': ['.mp4', '.mkv'],
        'Python Files': ['.py']
    }

    def __init__(self, target_dir, log_filename="organizer_log.txt"):
        self.target_dir = os.path.abspath(target_dir)
        self.log_path = os.path.join(self.target_dir, log_filename)
        self.counts = {category: 0 for category in self.CATEGORIES}
        self.counts['Others'] = 0
        self.history = []

    def get_category(self, filename):
        ext = os.path.splitext(filename)[1].lower()
        for category, extensions in self.CATEGORIES.items():
            if ext in extensions:
                return category
        return 'Others'

    def get_unique_filename(self, dest_dir, filename):
        base_name, ext = os.path.splitext(filename)
        target_path = os.path.join(dest_dir, filename)

        if not os.path.exists(target_path):
            return filename

        counter = 1
        while True:
            new_filename = f"{base_name}_{counter}{ext}"
            new_path = os.path.join(dest_dir, new_filename)
            if not os.path.exists(new_path):
                return new_filename
            counter += 1

    def log_entry(self, action, source, destination):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] {action}: {source} -> {destination}\n"
        try:
            with open(self.log_path, "a", encoding="utf-8") as f:
                f.write(entry)
        except OSError as e:
            print(f"Failed to write to log file: {e}")

    def scan_files(self):
        if not os.path.exists(self.target_dir):
            raise FileNotFoundError(f"Directory not found: {self.target_dir}")

        if not os.path.isdir(self.target_dir):
            raise NotADirectoryError(f"Path is not a directory: {self.target_dir}")

        files = []
        for item in os.listdir(self.target_dir):
            item_path = os.path.join(self.target_dir, item)
            if os.path.isfile(item_path):
                if item == os.path.basename(self.log_path):
                    continue
                files.append(item)
        return files

    def organize(self, preview=False):
        files_to_organize = self.scan_files()

        for category in self.counts:
            self.counts[category] = 0
        self.history = []

        if not files_to_organize:
            return self.history

        for filename in files_to_organize:
            source_path = os.path.join(self.target_dir, filename)
            category = self.get_category(filename)
            dest_dir = os.path.join(self.target_dir, category)

            unique_name = self.get_unique_filename(dest_dir, filename)
            dest_path = os.path.join(dest_dir, unique_name)

            is_renamed = unique_name != filename

            if preview:
                action = "PREVIEW (RENAMED)" if is_renamed else "PREVIEW"
                self.history.append({
                    "action": action,
                    "filename": filename,
                    "target_name": unique_name,
                    "category": category,
                    "from": source_path,
                    "to": dest_path
                })
                self.counts[category] += 1
            else:
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir, exist_ok=True)

                shutil.move(source_path, dest_path)
                action = "MOVED (RENAMED)" if is_renamed else "MOVED"
                self.history.append({
                    "action": action,
                    "filename": filename,
                    "target_name": unique_name,
                    "category": category,
                    "from": source_path,
                    "to": dest_path
                })
                self.counts[category] += 1
                self.log_entry(action, source_path, dest_path)

        return self.history

    def get_summary(self):
        total_files = sum(self.counts.values())
        return {
            "target_dir": self.target_dir,
            "total_files": total_files,
            "category_counts": dict(self.counts),
            "log_path": self.log_path
        }


def print_summary(summary, preview=False):
    mode_text = "PREVIEW SUMMARY" if preview else "ORGANIZATION SUMMARY"
    print("\n" + "=" * 50)
    print(f" {mode_text} ")
    print("=" * 50)
    print(f"Folder: {summary['target_dir']}")
    print("-" * 50)
    for category, count in summary['category_counts'].items():
        print(f"  {category:<15}: {count} file(s)")
    print("-" * 50)
    print(f"Total Files Processed: {summary['total_files']}")
    if not preview and summary['total_files'] > 0:
        print(f"Log saved to: {summary['log_path']}")
    print("=" * 50 + "\n")


def main():
    print("=" * 50)
    print("         AUTOMATED FILE ORGANIZER TOOL")
    print("=" * 50)

    while True:
        folder_input = input("\nEnter the folder path to organize (or 'q' to quit): ").strip()
        if folder_input.lower() == 'q':
            print("Exiting application.")
            return

        target_dir = os.path.abspath(folder_input)
        if not os.path.exists(target_dir):
            print(f"Error: The path '{target_dir}' does not exist. Please try again.")
            continue
        if not os.path.isdir(target_dir):
            print(f"Error: '{target_dir}' is a file, not a folder. Please enter a folder path.")
            continue
        break

    organizer = FileOrganizer(target_dir)

    try:
        files = organizer.scan_files()
    except Exception as e:
        print(f"Error reading directory: {e}")
        return

    if not files:
        print(f"\nNo loose files found in '{target_dir}' to organize.")
        return

    print(f"\nFound {len(files)} file(s) ready to be organized.")
    print("\nChoose an option:")
    print("1. Preview mode (see planned moves without moving anything)")
    print("2. Organize files directly")
    print("3. Preview first, then confirm")
    print("4. Cancel")

    choice = input("\nEnter choice (1-4): ").strip()

    if choice == '1':
        results = organizer.organize(preview=True)
        print("\n--- PREVIEW OF FILE MOVEMENTS ---")
        for item in results:
            note = f" (will be renamed to {item['target_name']})" if item['target_name'] != item['filename'] else ""
            print(f"[{item['category']}] {item['filename']} -> {item['category']}/{item['target_name']}{note}")
        print_summary(organizer.get_summary(), preview=True)

    elif choice == '2':
        results = organizer.organize(preview=False)
        print("\n--- MOVING FILES ---")
        for item in results:
            print(f"[{item['action']}] {item['filename']} -> {item['category']}/{item['target_name']}")
        print_summary(organizer.get_summary(), preview=False)

    elif choice == '3':
        results = organizer.organize(preview=True)
        print("\n--- PREVIEW OF FILE MOVEMENTS ---")
        for item in results:
            note = f" (rename: {item['target_name']})" if item['target_name'] != item['filename'] else ""
            print(f"[{item['category']}] {item['filename']} -> {item['category']}/{item['target_name']}{note}")
        print_summary(organizer.get_summary(), preview=True)

        confirm = input("Do you want to proceed with organizing these files? (y/n): ").strip().lower()
        if confirm == 'y':
            results = organizer.organize(preview=False)
            print("\n--- MOVING FILES ---")
            for item in results:
                print(f"[{item['action']}] {item['filename']} -> {item['category']}/{item['target_name']}")
            print_summary(organizer.get_summary(), preview=False)
        else:
            print("Operation cancelled. No files were moved.")

    else:
        print("Operation cancelled.")


if __name__ == "__main__":
    main()
