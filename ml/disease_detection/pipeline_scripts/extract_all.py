import zipfile
import os
import time
from concurrent.futures import ThreadPoolExecutor

zip_path = r"C:\Users\ESWAR\Downloads\archive.zip"
out_dir = r"C:\Users\ESWAR\Downloads\plant_dataset"
os.makedirs(out_dir, exist_ok=True)

print("Starting extraction of all plant categories from archive.zip...")
t0 = time.time()

with zipfile.ZipFile(zip_path, "r") as z:
    all_members = [m for m in z.infolist() if not m.is_dir() and "___" in m.filename]

print(f"Total image files to extract: {len(all_members)}")

# Create target directories upfront
class_names = set(m.filename.split("/")[2] for m in all_members if m.filename.count("/") >= 3)
for c in class_names:
    os.makedirs(os.path.join(out_dir, c), exist_ok=True)

# Also create PlantVillage/train and PlantVillage/val structure if desired
for m in all_members:
    parts = m.filename.split("/")
    if len(parts) >= 3:
        cls_name = parts[2]
        fname = parts[-1]
        # Direct class path
        dest = os.path.join(out_dir, cls_name, fname)
        # Also maintain PlantVillage path if needed
        # We can extract directly to out_dir/cls_name/fname

def extract_member(member):
    parts = member.filename.split("/")
    cls_name = parts[2]
    fname = parts[-1]
    dest = os.path.join(out_dir, cls_name, fname)
    if not os.path.exists(dest):
        with zipfile.ZipFile(zip_path, "r") as z_thread:
            with z_thread.open(member) as src, open(dest, "wb") as dst:
                dst.write(src.read())

print("Extracting with ThreadPoolExecutor (16 workers)...")
with ThreadPoolExecutor(max_workers=16) as executor:
    list(executor.map(extract_member, all_members, chunksize=100))

dt = time.time() - t0
print(f"Extraction complete in {dt:.2f} seconds!")

# Verify counts
total_extracted = 0
found_classes = sorted([d for d in os.listdir(out_dir) if os.path.isdir(os.path.join(out_dir, d)) and "___" in d])
print(f"Found {len(found_classes)} class directories:")
for c in found_classes:
    c_path = os.path.join(out_dir, c)
    num_imgs = len(os.listdir(c_path))
    total_extracted += num_imgs

print(f"Total images extracted across {len(found_classes)} classes: {total_extracted}")

