import os
import shutil
import zipfile

def create_distribution():
    dist_name = "TextGameCreator"
    
    # Create distribution folder
    if os.path.exists(dist_name):
        shutil.rmtree(dist_name)
    
    os.makedirs(f"{dist_name}/editor")
    os.makedirs(f"{dist_name}/engine")
    os.makedirs(f"{dist_name}/games")
    
    # Copy editor executable
    shutil.copy("dist/GameEditor.exe", f"{dist_name}/editor/")
    
    # Copy game engine
    shutil.copy("textgame.exe", f"{dist_name}/engine/")
    shutil.copy("play.bat", f"{dist_name}/engine/")
    
    # Copy README
    shutil.copy("README.txt", f"{dist_name}/")
    
    # Create zip
    shutil.make_archive(dist_name, 'zip', dist_name)
    
    print(f"Distribution package created: {dist_name}.zip")

if __name__ == "__main__":
    create_distribution()