from sklearn.model_selection import train_test_split
import os
import shutil

'''
Copy every image from data/raw/images/<region>/ into data/processed/{train,val,test}/<region>/, stratified per region at 70/15/15, reproducibly.
'''

SRC_DIR = "data/raw/images"
DST_DIR = "data/processed"

summary = {}   # region (n_train, n_val, n_test), for the verification table

for region in sorted(os.listdir(SRC_DIR)):
    region_path = os.path.join(SRC_DIR, region)
    if not os.path.isdir(region_path):      # skip stray files, only process folders
        continue

    #All .jpg files in this region 
    files = [f for f in os.listdir(region_path) if f.endswith(".jpg")]

    # Two-step split: 70% train, then halve the rest into 15% val / 15% test
    train, temp = train_test_split(files, train_size=0.70, random_state=42)
    val, test = train_test_split(temp, test_size=0.50, random_state=42)

    # Copy each split's files into data/processed/<split>/<region>/
    for split_name, split_files in [("train", train), ("val", val), ("test", test)]:
        dst_folder = os.path.join(DST_DIR, split_name, region)
        os.makedirs(dst_folder, exist_ok=True)     # create the destination folder

        for fname in split_files:
            src = os.path.join(region_path, fname)        # where the image is now
            dst = os.path.join(dst_folder, fname)         # where it's going
            shutil.copy2(src, dst)                        # copy2 keeps file metadata

    summary[region] = (len(train), len(val), len(test))

# %%
# 4. Verification table
print(f"{'Region':28s} {'train':>6} {'val':>5} {'test':>5} {'total':>6}")
t_tr = t_va = t_te = 0
for region, (n_tr, n_va, n_te) in summary.items():
    print(f"{region:28s} {n_tr:6d} {n_va:5d} {n_te:5d} {n_tr+n_va+n_te:6d}")
    t_tr += n_tr; t_va += n_va; t_te += n_te
print(f"{'TOTAL':28s} {t_tr:6d} {t_va:5d} {t_te:5d} {t_tr+t_va+t_te:6d}")