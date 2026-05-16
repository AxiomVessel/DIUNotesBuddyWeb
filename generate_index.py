import os
import json

NOTES_DIR = "notes"
EXAM_FOLDERS = {"Mid", "Final", "Assignment", "Presentation"}
FLAT_FOLDERS = {"Assignment", "Presentation"}
DEEP_FOLDERS = {"Mid", "Final"}
SKIP_EXTENSIONS = {".html", ".json"}

print("=== Starting Debug ===")
print(f"Current working directory: {os.getcwd()}")
print(f"Contents of root: {os.listdir('.')}")

if not os.path.exists(NOTES_DIR):
    print(f"ERROR: '{NOTES_DIR}' folder not found!")
    exit()

print(f"\nContents of {NOTES_DIR}/: {os.listdir(NOTES_DIR)}")


def process_flat_folder(folder_path):
    files = sorted([
        f for f in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, f))
        and os.path.splitext(f)[1].lower() not in SKIP_EXTENSIONS
    ])

    with open(os.path.join(folder_path, "files.json"), "w") as f:
        json.dump(files, f, indent=2)

    print(f"  ✅ Flat: {folder_path} → {files}")


def process_one_level_folder(folder_path):
    items = os.listdir(folder_path)

    files = sorted([
        f for f in items
        if os.path.isfile(os.path.join(folder_path, f))
        and os.path.splitext(f)[1].lower() not in SKIP_EXTENSIONS
    ])

    folders = sorted([
        f for f in items
        if os.path.isdir(os.path.join(folder_path, f))
    ])

    with open(os.path.join(folder_path, "files.json"), "w") as f:
        json.dump(files, f, indent=2)

    with open(os.path.join(folder_path, "folders.json"), "w") as f:
        json.dump(folders, f, indent=2)

    print(f"  ✅ OneLevel: {folder_path} → files: {files} | folders: {folders}")

    for folder in folders:
        process_flat_folder(os.path.join(folder_path, folder))


def process_deep_folder(folder_path):
    items = os.listdir(folder_path)

    files = sorted([
        f for f in items
        if os.path.isfile(os.path.join(folder_path, f))
        and os.path.splitext(f)[1].lower() not in SKIP_EXTENSIONS
    ])

    folders = sorted([
        f for f in items
        if os.path.isdir(os.path.join(folder_path, f))
    ])

    with open(os.path.join(folder_path, "files.json"), "w") as f:
        json.dump(files, f, indent=2)

    with open(os.path.join(folder_path, "folders.json"), "w") as f:
        json.dump(folders, f, indent=2)

    print(f"  ✅ Deep: {folder_path} → files: {files} | folders: {folders}")

    for folder in folders:
        process_deep_folder(os.path.join(folder_path, folder))


for year in os.listdir(NOTES_DIR):
    year_path = os.path.join(NOTES_DIR, year)
    if not os.path.isdir(year_path): continue
    print(f"\nYear: {year}")

    for semester in os.listdir(year_path):
        semester_path = os.path.join(year_path, semester)
        if not os.path.isdir(semester_path): continue
        print(f"  Semester: {semester}")

        # Handle QN directly under semester
        qn_path = os.path.join(semester_path, "QN")
        if os.path.isdir(qn_path):
            print(f"    Found QN directly under {semester}")
            process_one_level_folder(qn_path)

        for subject in os.listdir(semester_path):
            subject_path = os.path.join(semester_path, subject)
            if not os.path.isdir(subject_path): continue
            if subject == "QN": continue  # already handled above
            print(f"    Subject: {subject}")

            for exam in os.listdir(subject_path):
                exam_path = os.path.join(subject_path, exam)
                if not os.path.isdir(exam_path): continue
                print(f"      Exam found: '{exam}' — ", end="")

                if exam not in EXAM_FOLDERS:
                    print(f"SKIPPED (not in EXAM_FOLDERS)")
                    continue

                if exam in FLAT_FOLDERS:
                    print("processing as FLAT")
                    process_flat_folder(exam_path)
                elif exam in DEEP_FOLDERS:
                    print("processing as DEEP")
                    process_deep_folder(exam_path)

print("\n=== Done ===")