import os
import json

NOTES_DIR = "notes"
EXAM_FOLDERS = {"Mid", "Final", "Assignment", "Presentation"}
FLAT_FOLDERS = {"Assignment", "Presentation"}
SKIP_EXTENSIONS = {".html", ".json"}

def process_folder(folder_path):
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

    print(f"Updated: {folder_path} → files: {files} | folders: {folders}")

    for folder in folders:
        process_folder(os.path.join(folder_path, folder))


def process_flat_folder(folder_path):
    files = sorted([
        f for f in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, f))
        and os.path.splitext(f)[1].lower() not in SKIP_EXTENSIONS
    ])

    with open(os.path.join(folder_path, "files.json"), "w") as f:
        json.dump(files, f, indent=2)

    print(f"Updated: {folder_path} → files: {files}")


for year in os.listdir(NOTES_DIR):
    year_path = os.path.join(NOTES_DIR, year)
    if not os.path.isdir(year_path): continue

    for semester in os.listdir(year_path):
        semester_path = os.path.join(year_path, semester)
        if not os.path.isdir(semester_path): continue

        for subject in os.listdir(semester_path):
            subject_path = os.path.join(semester_path, subject)
            if not os.path.isdir(subject_path): continue

            for exam in os.listdir(subject_path):
                exam_path = os.path.join(subject_path, exam)
                if not os.path.isdir(exam_path): continue
                if exam not in EXAM_FOLDERS: continue

                if exam in FLAT_FOLDERS:
                    process_flat_folder(exam_path)
                else:
                    process_folder(exam_path)