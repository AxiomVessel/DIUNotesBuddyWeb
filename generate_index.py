import os
import json

NOTES_DIR = "notes"
EXAM_FOLDERS = {"Mid", "Final"}
SKIP_EXTENSIONS = {".html", ".json"}

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

                # List only actual note files
                files = sorted([
                    f for f in os.listdir(exam_path)
                    if os.path.isfile(os.path.join(exam_path, f))
                    and os.path.splitext(f)[1].lower() not in SKIP_EXTENSIONS
                ])

                # Write files.json
                json_path = os.path.join(exam_path, "files.json")
                with open(json_path, "w") as f:
                    json.dump(files, f, indent=2)

                print(f"Updated: {json_path} → {files}")