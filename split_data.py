import os
import random
import shutil

random.seed(42)

IMG_DIR = "data/images"
LBL_DIR = "data/labels"

IMG_TRAIN = "data/images/train"
IMG_VAL = "data/images/val"
LBL_TRAIN = "data/labels/train"
LBL_VAL = "data/labels/val"

os.makedirs(IMG_TRAIN, exist_ok=True)
os.makedirs(IMG_VAL, exist_ok=True)
os.makedirs(LBL_TRAIN, exist_ok=True)
os.makedirs(LBL_VAL, exist_ok=True)

images = [f for f in os.listdir(IMG_DIR) if f.endswith(".jpg")]
random.shuffle(images)

split = int(0.8 * len(images))
train_imgs = images[:split]
val_imgs = images[split:]

def move(files, img_dst, lbl_dst):
    for img in files:
        lbl = img.replace(".jpg", ".txt")
        shutil.move(os.path.join(IMG_DIR, img), os.path.join(img_dst, img))
        shutil.move(os.path.join(LBL_DIR, lbl), os.path.join(lbl_dst, lbl))

move(train_imgs, IMG_TRAIN, LBL_TRAIN)
move(val_imgs, IMG_VAL, LBL_VAL)

print("✅ Dataset split complete")
