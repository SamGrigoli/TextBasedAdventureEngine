import os
import shutil
import zipfile
import platform

# Detect OS
if os.name == "nt":  # Windows
    EXE = ".exe"
    RM = "del /F"
else:  # macOS / Linux / BSD
    EXE = ""
    RM = "rm -f"

print("EXE =", EXE)
print("RM =", RM)

def create_distribution():
    dist_name = "TextGameCreator"
    
    # Create distribution folder
    if os.path.exists(dist_name):
        shutil.rmtree(dist_name)
    
    os.makedirs(f"{dist_name}/editor")
    os.makedirs(f"{dist_name}/engine")
    os.makedirs(f"{dist_name}/data")
    
    # Copy editor executable
    shutil.copy(f"dist/GameEditor{EXE}", f"{dist_name}/editor/")
    
    # Copy game engine
    shutil.copy(f"textadventure{EXE}", f"{dist_name}/engine/")
    shutil.copy("play.bat", f"{dist_name}/engine/")

    # Copy data files
    shutil.copytree("textgame/data/", f"{dist_name}/data/", dirs_exist_ok=True)
    
    # Copy README
    shutil.copy("README.txt", f"{dist_name}/")
    
    # Create zip
    shutil.make_archive(dist_name, 'zip', dist_name)
    
    print(f"Distribution package created: {dist_name}.zip")

if __name__ == "__main__":
    create_distribution()