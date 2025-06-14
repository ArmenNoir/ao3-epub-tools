import os
import shutil
import pandas as pd
from datetime import datetime

def classify_and_transfer_files(
    csv_path: str,
    classify_by: str = "author",
    output_root: str = None,
    mode: str = "move"
):
    assert mode in ("move", "copy"), "mode must be 'move' or 'copy'"

    df = pd.read_csv(csv_path)

    # default output path
    if output_root is None:
        csv_dir = os.path.dirname(os.path.abspath(csv_path))
        output_root = os.path.join(csv_dir, f"sorted_by_{classify_by}")
    os.makedirs(output_root, exist_ok=True)

    processed_src_paths = set()

    for idx, row in df.iterrows():
        raw_path = str(row.get("path", "")).strip()
        src_path = os.path.normpath(raw_path)
        error_val = row.get("error", "")
        if pd.isna(error_val) or str(error_val).strip() == "":
            error = ""
        else:
            error = str(error_val).strip()
        subfolder = str(row.get(classify_by, "Unknown")).strip() or "Unknown"

        if error:
            print(f"[Skip] File has error please check manually: {src_path}")
            continue
        if not os.path.exists(src_path):
            print(f"[Skip] File not exist: {src_path}")
            continue
        if src_path in processed_src_paths:
            print(f"[Skip] Already processed: {src_path}")
            continue

        target_dir = os.path.join(output_root, subfolder)
        os.makedirs(target_dir, exist_ok=True)

        file_name = os.path.basename(src_path)
        base_name, ext = os.path.splitext(file_name)
        target_path = os.path.join(target_dir, file_name)

        # duplicate add _250101_1212
        if os.path.exists(target_path):
            timestamp = datetime.now().strftime("_%y%m%d_%H%M%S")
            target_path = os.path.join(target_dir, f"{base_name}{timestamp}{ext}")
            print(f"[Duplicated] {src_path} → {target_path}")
        try:
            if mode == "copy":
                shutil.copy2(src_path, target_path)
                print(f"[COPY] {src_path} → {target_path}")
            else:
                shutil.move(src_path, target_path)
                print(f"[MOVE] {src_path} → {target_path}")

            processed_src_paths.add(src_path)
        except Exception as e:
            print(f"[Error] {src_path}\n Reason: {e}")

if __name__ == "__main__":
    classify_and_transfer_files(csv_path='ao3_epub_metadata.csv',classify_by="author",output_root=None,mode="move")