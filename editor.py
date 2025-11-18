import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import json, subprocess, platform, sys
import os




# Get the directory where the executable/script is located
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    BASE_DIR = os.path.dirname(sys.executable)
else:
    # Running as script
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Set games directory relative to executable
GAMES_DIR = os.path.join(BASE_DIR, "..", "data")
os.makedirs(GAMES_DIR, exist_ok=True)

WORLD_FILE = "../data/world.json"
ITEMS_FILE = "../data/items.json"
PICTURES_FILE = "../data/pictures.json"
ENEMIES_FILE = "../data/enemies.json"
WEAPONS_FILE = "../data/weapons.json"
PLAYER_FILE = "../data/player.json"
LOADGAME_FILE = "../data/loadgame.json"
ENGINE_EXE = "textgame.exe" if platform.system() == "Windows" else "./textgame"

# Ensure world file exists
if not os.path.exists(WORLD_FILE):
    with open(WORLD_FILE, "w") as f:
        json.dump({"startRoom": "", "rooms": []}, f, indent=2)

# Ensure items file exists
if not os.path.exists(ITEMS_FILE):
    with open(ITEMS_FILE, "w") as f:
        json.dump({"items": []}, f, indent=2)

#Ensure pictures file exists
if not os.path.exists(PICTURES_FILE):
    with open(PICTURES_FILE, "w") as f:
        json.dump({"pictures": []}, f, indent=2)

def load_world():
    with open(WORLD_FILE, "r") as f:
        return json.load(f)

def save_world(world_data):
    with open(WORLD_FILE, "w") as f:
        json.dump(world_data, f, indent=2)

def load_items():
    with open(ITEMS_FILE, "r") as f:
        return json.load(f)

def save_items(items_data):
    with open(ITEMS_FILE, "w") as f:
        json.dump(items_data, f, indent=2)

def load_enemies():
    with open(ENEMIES_FILE, "r") as f:
        return json.load(f)

def save_enemies(enemies_data):
    with open(ENEMIES_FILE, "w") as f:
        json.dump(enemies_data, f, indent=2)

def load_weapons():
    with open(WEAPONS_FILE, "r") as f:
        return json.load(f)

def save_weapons(weapons_data):
    with open(WEAPONS_FILE, "w") as f:
        json.dump(weapons_data, f, indent=2)

def load_pictures():
    with open(PICTURES_FILE, "r") as f:
        return json.load(f)
    
def save_pictures(pictures_data):
    with open(PICTURES_FILE, "w") as f:
        json.dump(pictures_data, f, indent=2)

def save_player(player_data):
    with open(PLAYER_FILE, "w") as f:
        json.dump(player_data, f, indent=2)

def load_player():
    with open(PLAYER_FILE, "r") as f:
        return json.load(f)
    

def add_items_to_items_json(item_names):
    """Add items to items.json if they don't already exist"""
    if not item_names:
        return
    
    items_data = load_items()
    existing_ids = {item["id"] for item in items_data["items"]}
    
    for item_name in item_names:
        if item_name and item_name not in existing_ids:
            # Create a basic item structure
            new_item = {
                "id": item_name,
                "name": item_name.replace("_", " ").title(),
                "desc": f"A {item_name.replace('_', ' ').lower()}.",
                "portable": True
            }
            items_data["items"].append(new_item)
    
    save_items(items_data)

def refresh_start_room_dropdown():
    world_data = load_world()
    rooms = [r["id"] for r in world_data["rooms"]]
    start_room_var.set(world_data.get("startRoom", ""))
    dropdown["menu"].delete(0, "end")
    for r in rooms:
        dropdown["menu"].add_command(label=r, command=tk._setit(start_room_var, r))

def set_start_room():
    world_data = load_world()
    world_data["startRoom"] = start_room_var.get()
    save_world(world_data)
    messagebox.showinfo("Updated", f"Start room set to {start_room_var.get()}")

def add_room():
    room_id = entry_room_id.get().strip()
    room_name = entry_room_name.get().strip()
    room_desc = entry_room_desc.get("1.0", tk.END).strip()
    exits_text = entry_exits.get().strip()   # e.g. north:foyer,east:cellar
    items_text = entry_items.get().strip()   # e.g. key,lantern
   

    if not room_id or not room_name:
        messagebox.showwarning("Missing Data", "Room ID and Name are required.")
        return

    exits = {}
    if exits_text:
        for pair in exits_text.split(","):
            try:
                direction, dest = pair.split(":")
                exits[direction.strip()] = dest.strip()
            except ValueError:
                pass

    items = [i.strip() for i in items_text.split(",")] if items_text else []

    world_data = load_world()

    # New room template with empty locks, requirements, triggers
    new_room = {
        "id": room_id,
        "name": room_name,
        "desc": room_desc,
        "exits": exits,
        "items": items,
        "weapons": [],
        "locks": [],
        "triggers": []
    }

    world_data["rooms"].append(new_room)
    save_world(world_data)
    
    # Also save items to items.json
    add_items_to_items_json(items)

    messagebox.showinfo("Success", f"Room '{room_name}' added! Items also saved to items.json.")
    entry_room_id.delete(0, tk.END)
    entry_room_name.delete(0, tk.END)
    entry_room_desc.delete("1.0", tk.END)
    entry_exits.delete(0, tk.END)
    entry_items.delete(0, tk.END)

    refresh_start_room_dropdown()

def add_item():
    item_id = simpledialog.askstring("Item ID", "Enter item ID:")
    if not item_id: return
    room_id = simpledialog.askstring("Room ID", "Enter room ID to place item in:")
    if not room_id: return 
    item_name = simpledialog.askstring("Item Name", "Enter item name:")
    if not item_name: return
    item_desc = simpledialog.askstring("Item Description", "Enter item description:")

    items_data = load_items()
    
        
    world_data = load_world()
    for room in world_data["rooms"]:
        if room["id"] == room_id:
            room["items"].append(item_id)
            items_data["items"].append({
                "id": item_id,
                "name": item_name,
                "desc": item_desc or f"A {item_name}.",
                "portable": True
            })
            save_world(world_data)
            break
    save_items(items_data)
    messagebox.showinfo("Added", f"Item {item_name} added.")

def add_item_desc():
    item_id = simpledialog.askstring("Item ID", "Enter item ID to add description:")
    if not item_id: return
    desc = simpledialog.askstring("Description", "Enter item description:")
    if not desc: return

    items_data = load_items()
    for item in items_data["items"]:
        if item["id"] == item_id:
            item["desc"] = desc
            save_items(items_data)
            messagebox.showinfo("Updated", f"Description updated for item {item_id}.")
            return
    messagebox.showwarning("Not Found", f"No item with id {item_id}")

def add_art():
    item_id = simpledialog.askstring("Item ID", "Enter item ID to add picture:")
    if not item_id: return
    path = simpledialog.askstring("Picture", "Enter ASCII art for picture:")
    if not path: return

    pictures_data = load_pictures()
    for pic in pictures_data["pictures"]:
        if pic["id"] == item_id:
            save_pictures(pictures_data)
            messagebox.showinfo("Updated", f"Picture added for item {item_id}.")
            return
    
    # If not found, add new entry
    pictures_data["pictures"].append({"id": item_id, "path": path})
    save_pictures(pictures_data)
    messagebox.showinfo("Added", f"Picture path added for item {item_id}.")

def add_enemy():
    enemy_id = simpledialog.askstring("Enemy ID", "Enter enemy ID (Must match desired room id):")
    if not enemy_id: return
    enemy_name = simpledialog.askstring("Enemy Name", "Enter enemy name:")
    if not enemy_name: return
    enemy_desc = simpledialog.askstring("Enemy Description", "Enter enemy description:")
    if not enemy_desc: return
    enemy_health = simpledialog.askinteger("Enemy Health", "Enter enemy health (integer):", minvalue=1)
    if not enemy_health: return
    enemy_damage = simpledialog.askinteger("Enemy Damage", "Enter enemy damage (integer):", minvalue=1)
    if not enemy_damage: return 


    enemies_data = load_enemies()
    enemies_data["enemies"].append({
        "id": enemy_id,
        "name": enemy_name,
        "desc": enemy_desc,
        "health": enemy_health,
        "damage": enemy_damage
    })
    save_enemies(enemies_data)
    messagebox.showinfo("Added", f"Enemy {enemy_name} added.")

def add_weapon():
    if not current_game_dir:
        messagebox.showwarning("No Game", "Please create or load a game first.")
        return
    
    weapon_id = simpledialog.askstring("Weapon ID", "Enter weapon ID (e.g., 'sword', 'axe'):")
    if not weapon_id: return
    
    weapon_name = simpledialog.askstring("Weapon Name", "Enter weapon name(Most simple to make same as ID and avoid spaces): ")
    if not weapon_name: return
    
    weapon_desc = simpledialog.askstring("Weapon Description", "Enter weapon description:")
    if not weapon_desc: return
    
    weapon_damage = simpledialog.askinteger("Weapon Damage", "Enter weapon damage (integer):", minvalue=1)
    if not weapon_damage: return

    # Always add to weapons.json first
    weapons_data = load_weapons()
    weapons_data["weapons"].append({
        "id": weapon_id,
        "name": weapon_name,
        "desc": weapon_desc,
        "damage": weapon_damage
    })
    save_weapons(weapons_data)
    
    # Ask if they want to place it in a room
    place_in_room = messagebox.askyesno("Place in Room?", 
                                        f"Weapon '{weapon_name}' added to weapons.json.\n\n"
                                        "Do you want to place it in a room?")
    
    if place_in_room:
        room_id = simpledialog.askstring("Room ID", "Enter room ID to place weapon in:")
        if room_id:
            world_data = load_world()
            room_found = False
            
            for room in world_data["rooms"]:
                if room["id"] == room_id:
                    if "weapons" not in room:
                        room["weapons"] = []
                    # Store by weapon_id (not room_id, not weapon_name)
                    room["weapons"].append(weapon_id)
                    save_world(world_data)
                    room_found = True
                    messagebox.showinfo("Success", f"Weapon '{weapon_name}' placed in room '{room_id}'.")
                    break
            
            if not room_found:
                messagebox.showwarning("Room Not Found", f"Room '{room_id}' not found. Weapon is in weapons.json but not placed in any room.")
    else:
        messagebox.showinfo("Added", f"Weapon '{weapon_name}' added to weapons.json.")

def add_lock():
    room_id = simpledialog.askstring("Room ID", "Enter room ID to add lock:")
    if not room_id: return
    exit_dir = simpledialog.askstring("Exit", "Which exit is locked? (e.g., north)")
    requires = simpledialog.askstring("Requires", "What item is required?")
    message = simpledialog.askstring("Message", "What message to show?")
    if not exit_dir or not requires: return

    world_data = load_world()
    for room in world_data["rooms"]:
        if room["id"] == room_id:
            room["locks"].append({
                "exit": exit_dir,
                "requires": requires,
                "message": message or ""
            })
            save_world(world_data)
            
            # Also add the required item to items.json
            add_items_to_items_json([requires])
            
            messagebox.showinfo("Added", f"Lock added to {room_id}. Required item added to items.json.")
            return
    messagebox.showwarning("Not Found", f"No room with id {room_id}")



def add_trigger():
    room_id = simpledialog.askstring("Room ID", "Enter room ID to add trigger:")
    if not room_id: return
    trigger_on = simpledialog.askstring("Trigger On", "What action triggers this? (e.g., use key on north)")

    world_data = load_world()
    for room in world_data["rooms"]:
        if room["id"] == room_id:
            effects = []
            while True:
                effect_type = simpledialog.askstring("Effect Type", "Effect type? (unlock/say) [Cancel to stop]")
                if not effect_type: break
                effect = {"type": effect_type}
                if effect_type == "unlock":
                    effect["exit"] = simpledialog.askstring("Unlock Exit", "Which exit to unlock?")
                elif effect_type == "say":
                    effect["text"] = simpledialog.askstring("Say Text", "What text to say?")
                effects.append(effect)

            if trigger_on and effects:
                room["triggers"].append({"on": trigger_on, "effects": effects})
                save_world(world_data)
                messagebox.showinfo("Added", f"Trigger added to {room_id}.")
            return
    messagebox.showwarning("Not Found", f"No room with id {room_id}")

def edit_player():
    """Edit player stats"""
    player_data = load_player()
    
    if "players" not in player_data or len(player_data["players"]) == 0:
        messagebox.showwarning("No Player", "No player found in player.json")
        return
    
    player = player_data["players"][0]  # Get first player
    
    # Ask for new values with current values as defaults
    new_name = simpledialog.askstring("Player Name", "Enter player name:", initialvalue=player.get("name", "Player"))
    if new_name is None: return  # User cancelled
    
    #new_desc = simpledialog.askstring("Player Description", "Enter player description:", initialvalue=player.get("desc", "It's you!"))
    #if new_desc is None: return
    
    new_health = simpledialog.askinteger("Player Health", "Enter player health:", initialvalue=player.get("health", 100), minvalue=1)
    if new_health is None: return
    
    new_damage = simpledialog.askinteger("Player Damage", "Enter player damage:", initialvalue=player.get("damage", 5), minvalue=0)
    if new_damage is None: return
    
    # Update player data
    player["name"] = new_name
    #player["desc"] = new_desc
    player["health"] = new_health
    player["damage"] = new_damage
    
    save_player(player_data)
    messagebox.showinfo("Updated", f"Player stats updated:\nHealth: {new_health}\nDamage: {new_damage}")

def delete_room():
    """Delete a room by ID"""
    room_id = simpledialog.askstring("Delete Room", "Enter room ID to delete:")
    if not room_id:
        return
    
    world_data = load_world()
    
    # Find and remove the room
    room_found = False
    for i, room in enumerate(world_data["rooms"]):
        if room["id"] == room_id:
            # Confirm deletion
            confirm = messagebox.askyesno(
                "Confirm Deletion", 
                f"Are you sure you want to delete room '{room['name']}' ({room_id})?\n\n"
                "Warning: This will break any exits pointing to this room!"
            )
            if confirm:
                world_data["rooms"].pop(i)
                save_world(world_data)
                
                # If this was the start room, clear it
                if world_data.get("startRoom") == room_id:
                    world_data["startRoom"] = ""
                    save_world(world_data)
                    messagebox.showwarning("Start Room Cleared", 
                                        "This was the start room. Please set a new start room.")
                
                refresh_start_room_dropdown()
                messagebox.showinfo("Deleted", f"Room '{room_id}' has been deleted.")
            room_found = True
            break
    
    if not room_found:
        messagebox.showwarning("Not Found", f"No room with ID '{room_id}' found.")

def update_file_paths():
    """Update global file path variables"""
    global WORLD_FILE, ITEMS_FILE, PICTURES_FILE, ENEMIES_FILE, WEAPONS_FILE, PLAYER_FILE
    
    if current_game_dir:
        WORLD_FILE = f"{current_game_dir}/world.json"
        ITEMS_FILE = f"{current_game_dir}/items.json"
        PICTURES_FILE = f"{current_game_dir}/pictures.json"
        ENEMIES_FILE = f"{current_game_dir}/enemies.json"
        WEAPONS_FILE = f"{current_game_dir}/weapons.json"
        PLAYER_FILE = f"{current_game_dir}/player.json"

        game_folder_name = os.path.basename(os.path.normpath(current_game_dir))

        with open(LOADGAME_FILE, "w", encoding="utf-8") as f:
            json.dump(game_folder_name, f, indent=2)
        

def update_title():
    """Update window title with current game name"""
    if current_game_dir:
        game_name = os.path.basename(current_game_dir)
        root.title(f"Text Game World Editor - {game_name}")
    else:
        root.title("Text Game World Editor - No Game Loaded")


def new_game():
    """Create a new game with empty JSON files"""
    global current_game_dir
    
    # Ask user to select/create a folder
    folder_path = filedialog.askdirectory(
        title="Select or Create a Folder for Your New Game",
        initialdir="textgame/data"
    )
    
    if not folder_path:
        return  # User cancelled
    
    # Check if folder already has game files
    if os.path.exists(os.path.join(folder_path, "world.json")):
        overwrite = messagebox.askyesno(
            "Folder Not Empty",
            "This folder already contains game files. Overwrite them?"
        )
        if not overwrite:
            return
    
    current_game_dir = folder_path
    
    # Create empty JSON files
    with open(f"{folder_path}/world.json", "w") as f:
        json.dump({"startRoom": "", "rooms": []}, f, indent=2)
    
    with open(f"{folder_path}/items.json", "w") as f:
        json.dump({"items": []}, f, indent=2)
    
    with open(f"{folder_path}/enemies.json", "w") as f:
        json.dump({"enemies": []}, f, indent=2)
    
    with open(f"{folder_path}/weapons.json", "w") as f:
        json.dump({"weapons": []}, f, indent=2)
    
    with open(f"{folder_path}/player.json", "w") as f:
        json.dump({
            "players": [{
                "id": "player",
                "name": "Player",
                "desc": "It's you!",
                "health": 100,
                "damage": 5
            }]
        }, f, indent=2)
    
    with open(f"{folder_path}/pictures.json", "w") as f:
        json.dump({"pictures": []}, f, indent=2)
    
    update_file_paths()
    refresh_start_room_dropdown()
    
    game_name = os.path.basename(folder_path)
    messagebox.showinfo("Success", f"New game '{game_name}' created!")
    update_title()


def load_game():
    """Load an existing game from a folder"""
    global current_game_dir
    
    # Ask user to select a folder
    folder_path = filedialog.askdirectory(
        title="Select Game Folder (containing JSON files)",
        initialdir="textgame/data"
    )
    
    if not folder_path:
        return  # User cancelled
    
    # Check if the folder contains the required JSON files
    required_files = ["world.json", "items.json", "enemies.json", "weapons.json", "player.json"]
    missing_files = []
    
    for file in required_files:
        if not os.path.exists(os.path.join(folder_path, file)):
            missing_files.append(file)
    
    if missing_files:
        messagebox.showerror(
            "Invalid Game Folder", 
            f"The selected folder is missing required files:\n\n" + 
            "\n".join(missing_files) +
            "\n\nPlease select a valid game folder."
        )
        return
    
    # Load the game
    current_game_dir = folder_path
    update_file_paths()
    
    # Verify files can be loaded
    try:
        refresh_start_room_dropdown()
        game_name = os.path.basename(folder_path)
        messagebox.showinfo("Success", f"Game '{game_name}' loaded successfully!")
        update_title()
    except Exception as e:
        messagebox.showerror("Load Error", f"Error loading game files:\n{str(e)}")
        current_game_dir = None


import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog, Canvas, Scrollbar
import json
import os

def visualize_world():
    """Create a visual representation of the world map"""
    if not current_game_dir:
        messagebox.showwarning("No Game", "Please create or load a game first.")
        return
    
    try:
        world_data = load_world()
    except:
        messagebox.showerror("Error", "Could not load world data.")
        return
    
    if not world_data.get("rooms"):
        messagebox.showinfo("Empty World", "No rooms to visualize. Create some rooms first!")
        return
    
    # Create visualization window
    viz_window = tk.Toplevel(root)
    viz_window.title("World Map Visualization")
    viz_window.geometry("900x700")
    
    # Create canvas with scrollbars
    frame = tk.Frame(viz_window)
    frame.pack(fill=tk.BOTH, expand=True)
    
    canvas = Canvas(frame, bg="white", scrollregion=(0, 0, 2000, 2000))
    
    h_scrollbar = Scrollbar(frame, orient=tk.HORIZONTAL, command=canvas.xview)
    h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
    
    v_scrollbar = Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
    v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    canvas.config(xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)
    
    # Layout algorithm - simple grid-based with auto-positioning
    positions = auto_layout_rooms(world_data["rooms"])
    
    # Draw connections (exits) first so they appear behind rooms
    for room in world_data["rooms"]:
        room_id = room["id"]
        if room_id not in positions:
            continue
        
        x1, y1 = positions[room_id]
        
        for direction, target_id in room.get("exits", {}).items():
            if target_id in positions:
                x2, y2 = positions[target_id]
                
                # Draw arrow
                canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST, fill="gray", width=2)
                
                # Draw direction label
                mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
                canvas.create_text(mid_x, mid_y, text=direction, fill="blue", font=("Arial", 9))
    
    # Draw rooms
    start_room = world_data.get("startRoom", "")
    
    for room in world_data["rooms"]:
        room_id = room["id"]
        if room_id not in positions:
            continue
        
        x, y = positions[room_id]
        
        # Room color based on properties
        color = "lightgreen" if room_id == start_room else "lightblue"
        
        # Check for special features
        has_enemy = any(enemy["id"] == room_id for enemy in load_enemies().get("enemies", []))
        has_items = len(room.get("items", [])) > 0
        has_weapons = len(room.get("weapons", [])) > 0
        has_locks = len(room.get("locks", [])) > 0
        
        if has_enemy:
            color = "lightcoral"
        elif has_locks:
            color = "lightyellow"
        
        # Draw room box
        rect = canvas.create_rectangle(x-60, y-40, x+60, y+40, fill=color, outline="black", width=2)
        
        # Room name
        canvas.create_text(x, y-20, text=room["name"], font=("Arial", 10, "bold"), width=110)
        
        # Room ID (smaller)
        canvas.create_text(x, y, text=f"({room_id})", font=("Arial", 8), fill="gray")
        
        # Icons for features
        icon_y = y + 15
        icons = []
        if has_enemy:
            icons.append("⚔️")
        if has_items:
            icons.append("📦")
        if has_weapons:
            icons.append("🗡️")
        if has_locks:
            icons.append("🔒")
        
        if icons:
            canvas.create_text(x, icon_y, text=" ".join(icons), font=("Arial", 12))
        
        # Make rooms clickable
        def on_room_click(event, r=room):
            show_room_details(r)
        
        canvas.tag_bind(rect, "<Button-1>", on_room_click)
    
    # Add legend
    legend_x, legend_y = 20, 20
    canvas.create_rectangle(legend_x, legend_y, legend_x + 200, legend_y + 180, fill="white", outline="black")
    canvas.create_text(legend_x + 100, legend_y + 15, text="Legend", font=("Arial", 12, "bold"))
    
    legend_items = [
        ("🟢 Start Room", "lightgreen"),
        ("🔵 Normal Room", "lightblue"),
        ("🔴 Enemy Room", "lightcoral"),
        ("🟡 Locked Room", "lightyellow"),
        ("⚔️ Has Enemy", "white"),
        ("📦 Has Items", "white"),
        ("🗡️ Has Weapons", "white"),
        ("🔒 Has Locks", "white"),
    ]
    
    for i, (text, color) in enumerate(legend_items):
        y = legend_y + 35 + (i * 18)
        if color != "white":
            canvas.create_rectangle(legend_x + 10, y - 6, legend_x + 30, y + 6, fill=color, outline="black")
        canvas.create_text(legend_x + 40, y, text=text, anchor="w", font=("Arial", 9))

def auto_layout_rooms(rooms):
    """Automatically position rooms in a grid layout based on connections"""
    if not rooms:
        return {}
    
    positions = {}
    placed = set()
    
    # Start with the first room at center
    start_room = rooms[0]["id"]
    positions[start_room] = (1000, 1000)  # Center of canvas
    placed.add(start_room)
    
    # Direction offsets
    direction_offsets = {
        "north": (0, -150),
        "south": (0, 150),
        "east": (150, 0),
        "west": (-150, 0),
        "northeast": (150, -150),
        "northwest": (-150, -150),
        "southeast": (150, 150),
        "southwest": (-150, 150),
        "up": (0, -100),
        "down": (0, 100),
    }
    
    # Keep placing rooms until all are placed
    max_iterations = 100
    iteration = 0
    
    while len(placed) < len(rooms) and iteration < max_iterations:
        iteration += 1
        
        for room in rooms:
            if room["id"] in placed:
                # Try to place connected rooms
                current_pos = positions[room["id"]]
                
                for direction, target_id in room.get("exits", {}).items():
                    if target_id not in placed:
                        # Calculate position based on direction
                        offset = direction_offsets.get(direction.lower(), (150, 0))
                        new_x = current_pos[0] + offset[0]
                        new_y = current_pos[1] + offset[1]
                        
                        # Check if position is already taken
                        pos_taken = False
                        for existing_pos in positions.values():
                            if abs(existing_pos[0] - new_x) < 50 and abs(existing_pos[1] - new_y) < 50:
                                pos_taken = True
                                break
                        
                        if not pos_taken:
                            positions[target_id] = (new_x, new_y)
                            placed.add(target_id)
    
    # Place any remaining unconnected rooms in a grid
    unplaced = [r["id"] for r in rooms if r["id"] not in placed]
    grid_x, grid_y = 1000, 200
    
    for i, room_id in enumerate(unplaced):
        positions[room_id] = (grid_x + (i % 5) * 150, grid_y + (i // 5) * 150)
    
    return positions

def show_room_details(room):
    """Show detailed information about a room in a popup"""
    details = f"Room: {room['name']}\n"
    details += f"ID: {room['id']}\n"
    details += f"Description: {room['desc']}\n\n"
    
    if room.get("exits"):
        details += "Exits:\n"
        for direction, target in room["exits"].items():
            details += f"  {direction} → {target}\n"
        details += "\n"
    
    if room.get("items"):
        details += f"Items: {', '.join(room['items'])}\n"
    
    if room.get("weapons"):
        details += f"Weapons: {', '.join(room['weapons'])}\n"
    
    if room.get("locks"):
        details += "Locks:\n"
        for lock in room["locks"]:
            details += f"  {lock['exit']} requires {lock['requires']}\n"
    
    messagebox.showinfo(f"Room: {room['name']}", details)







# --- Tkinter UI ---
root = tk.Tk()
root.title("Text Game World Editor")

# Create menu bar
menubar = tk.Menu(root)
root.config(menu=menubar)

# File menu
file_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New Game", command=new_game)
file_menu.add_command(label="Load Game", command=load_game)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

# Start Room Section
frame_start = tk.LabelFrame(root, text="Start Room", padx=10, pady=10)
frame_start.pack(padx=10, pady=5, fill="x")

start_room_var = tk.StringVar(root)
dropdown = tk.OptionMenu(frame_start, start_room_var, "")
dropdown.pack(side="left", padx=5)
btn_set_start = tk.Button(frame_start, text="Set Start Room", command=set_start_room)
btn_set_start.pack(side="left", padx=5)

# --- Room Section ---
frame_room = tk.LabelFrame(root, text="Add Room", padx=10, pady=10)
frame_room.pack(padx=10, pady=5, fill="x")

tk.Label(frame_room, text="Room ID:").grid(row=0, column=0, sticky="w")
entry_room_id = tk.Entry(frame_room, width=30)
entry_room_id.grid(row=0, column=1)

tk.Label(frame_room, text="Room Name:").grid(row=1, column=0, sticky="w")
entry_room_name = tk.Entry(frame_room, width=30)
entry_room_name.grid(row=1, column=1)

tk.Label(frame_room, text="Description:").grid(row=2, column=0, sticky="nw")
entry_room_desc = tk.Text(frame_room, width=40, height=3)
entry_room_desc.grid(row=2, column=1)

tk.Label(frame_room, text="Exits (dir:roomID,...):").grid(row=3, column=0, sticky="w")
entry_exits = tk.Entry(frame_room, width=40)
entry_exits.grid(row=3, column=1)

tk.Label(frame_room, text="Items (comma list):").grid(row=4, column=0, sticky="w")
entry_items = tk.Entry(frame_room, width=40)
entry_items.grid(row=4, column=1)

btn_add_room = tk.Button(frame_room, text="Add Room", command=add_room)
btn_add_room.grid(row=5, column=1, sticky="e", pady=5)

# --- Extra Editors ---
frame_extras = tk.LabelFrame(root, text="Advanced Editors", padx=10, pady=10)
frame_extras.pack(padx=10, pady=5, fill="x")

tk.Button(frame_extras, text="Add Lock", command=add_lock).pack(side="left", padx=5)
#tk.Button(frame_extras, text="Add Requirement", command=add_requirement).pack(side="left", padx=5)
tk.Button(frame_extras, text="Add Trigger", command=add_trigger).pack(side="left", padx=5)
tk.Button(frame_extras, text="Add Item Description", command=add_item_desc).pack(side="left", padx=5)
tk.Button(frame_extras, text="Add Enemy", command=add_enemy).pack(side="left", padx=5)
tk.Button(frame_extras, text="Add Item", command=add_item).pack(side="left", padx=5)
tk.Button(frame_extras, text="Add Weapon", command=add_weapon).pack(side="left", padx=5)
tk.Button(frame_extras, text="Edit Player", command=edit_player).pack(side="left", padx=5)

#btn_play = tk.Button(root, text="Play Game", command=play_game, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
#btn_play.pack(pady=10)

#root.mainloop()


# -- Undo Actions Section --
frame_undo = tk.LabelFrame(root, text="Undo Actions", padx=10, pady=10)
frame_undo.pack(padx=10, pady=5, fill="x")
tk.Button(frame_undo, text="Delete Room", command=delete_room).pack(side="left", padx=5)


frame_view = tk.LabelFrame(root, text="Visualization", padx=10, pady=10)
frame_view.pack(padx=10, pady=5, fill="x")

tk.Button(frame_view, text="View World Map", command=visualize_world, 
          bg="lightblue", font=("Arial", 11, "bold")).pack(pady=5)


# Initialize dropdown
refresh_start_room_dropdown()

root.mainloop()