import os
import shutil
import zipfile
import tarfile
import platform

def create_windows_distribution():
    dist_name = "TextGameCreator-Windows"
    
    print("Creating Windows distribution...")
    
    # Create distribution folder
    if os.path.exists(dist_name):
        shutil.rmtree(dist_name)
    
    os.makedirs(f"{dist_name}/editor")
    os.makedirs(f"{dist_name}/engine")
    os.makedirs(f"{dist_name}/data")
    
    # Copy editor executable
    if os.path.exists("dist/GameEditor.exe"):
        shutil.copy("dist/GameEditor.exe", f"{dist_name}/editor/")
    else:
        print("Warning: GameEditor.exe not found in dist/")
    
    # Copy game engine
    if os.path.exists("textgame.exe"):
        shutil.copy("textgame.exe", f"{dist_name}/engine/")
    else:
        print("Warning: textgame.exe not found")
    
    if os.path.exists("play.bat"):
        shutil.copy("play.bat", f"{dist_name}/engine/")
    else:
        print("Warning: play.bat not found")
    
    # Copy data files
    if os.path.exists("textgame/data/"):
        shutil.copytree("textgame/data/", f"{dist_name}/data/", dirs_exist_ok=True)
    else:
        print("Warning: textgame/data/ not found")
    
    # Copy README
    if os.path.exists("README.txt"):
        shutil.copy("README.txt", f"{dist_name}/")
    
    # Create zip
    shutil.make_archive(dist_name, 'zip', dist_name)
    
    print(f"Windows distribution created: {dist_name}.zip")

def create_linux_distribution():
    dist_name = "TextGameCreator-Linux"
    
    print("Creating Linux distribution...")
    
    # Create distribution folder
    if os.path.exists(dist_name):
        shutil.rmtree(dist_name)
    
    os.makedirs(f"{dist_name}/editor")
    os.makedirs(f"{dist_name}/engine")
    os.makedirs(f"{dist_name}/data")
    
    # Copy editor Python script
    if os.path.exists("editor.py"):
        shutil.copy("editor.py", f"{dist_name}/editor/")
        print("Copied editor.py")
    else:
        print("Warning: editor.py not found")
    
    # Copy game engine (Linux binary)
    # On Windows, this won't exist - need to compile on Linux
    if os.path.exists("textgame") and not os.path.exists("textgame.exe"):
        # This is the Linux binary
        shutil.copy("textgame", f"{dist_name}/engine/")
        os.chmod(f"{dist_name}/engine/textgame", 0o755)
        print("Copied textgame (Linux binary)")
    else:
        print("Warning: Linux binary 'textgame' not found")
        print("  (This is normal if you're on Windows)")
        print("  To create Linux version: compile on Linux with 'make'")
        # Create a placeholder note
        with open(f"{dist_name}/engine/BUILD_INSTRUCTIONS.txt", "w") as f:
            f.write("To build the Linux game engine:\n")
            f.write("1. Transfer source files to Linux\n")
            f.write("2. Run: make clean && make\n")
            f.write("3. Copy the 'textgame' binary here\n")
    
    if os.path.exists("play.sh"):
        shutil.copy("play.sh", f"{dist_name}/engine/")
        os.chmod(f"{dist_name}/engine/play.sh", 0o755)
        print("✓ Copied play.sh")
    else:
        print("Warning: play.sh not found")
    
    # Copy data files
    if os.path.exists("textgame/data/"):
        shutil.copytree("textgame/data/", f"{dist_name}/data/", dirs_exist_ok=True)
        print("✓ Copied data files")
    else:
        print("Warning: textgame/data/ not found")
    
    # Copy README
    if os.path.exists("README.txt"):
        shutil.copy("README.txt", f"{dist_name}/")
    
    # Create tar.gz
    with tarfile.open(f"{dist_name}.tar.gz", "w:gz") as tar:
        tar.add(dist_name, arcname=os.path.basename(dist_name))
    
    print(f"✓ Linux distribution created: {dist_name}.tar.gz")

def create_distribution():
    """Create distribution packages for both Windows and Linux"""
    
    current_os = platform.system()
    
    print("=" * 60)
    print(f"Running on: {current_os}")
    print("=" * 60)
    
    # Ask what to build
    print("\nWhat would you like to build?")
    print("1. Windows only (requires: textgame.exe, GameEditor.exe)")
    print("2. Linux only (requires: textgame binary compiled on Linux)")
    print("3. Both")
    print("4. Windows + Linux template (recommended if on Windows)")
    
    choice = input("\nEnter choice (1-4, default=4): ").strip() or "4"
    
    print()
    
    if choice == "1":
        create_windows_distribution()
    elif choice == "2":
        create_linux_distribution()
    elif choice == "3":
        create_windows_distribution()
        print()
        create_linux_distribution()
    elif choice == "4":
        
        create_windows_distribution()
        print()
        create_linux_distribution()
    else:
        print("Invalid choice. Creating both...")
        create_windows_distribution()
        print()
        create_linux_distribution()
    
    print("\n" + "=" * 60)
    print("Packaging complete!")
    print("=" * 60)
    
    if current_os == "Windows" and choice in ["2", "3", "4"]:
        print("\nNote: To complete Linux version:")
        print("1. Transfer project to Linux machine")
        print("2. Run: make clean && make")
        print("3. Run: python3 package.py")
        print("   OR manually copy 'textgame' to Linux distribution")

if __name__ == "__main__":
    create_distribution()