import os, shutil
src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
out = "/output/entry.png"
try:
    os.makedirs("/output", exist_ok=True)
    shutil.copyfile(src, out)
except OSError:
    os.makedirs("output", exist_ok=True)
    shutil.copyfile(src, "output/entry.png")
