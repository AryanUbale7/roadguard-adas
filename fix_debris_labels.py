import os

for folder in ["data/labels/train", "data/labels/val"]:
    for f in os.listdir(folder):
        if not f.endswith(".txt"):
            continue
        path = os.path.join(folder, f)
        lines = []
        with open(path) as file:
            for line in file:
                parts = line.strip().split()
                parts[0] = "2"
                lines.append(" ".join(parts))
        with open(path, "w") as file:
            file.write("\n".join(lines))

print("✅ Debris class IDs fixed to 2")
