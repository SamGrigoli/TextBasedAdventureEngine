#include "Engine.hpp"
#include <string>
#include <vector>
#include <algorithm> 
#include "Parser.hpp"
#include <iostream>
#include <cstdlib>  
#include <ctime>  

bool Engine::init(const std::string& itemsPath, const std::string& worldPath, const std::string& enemiesPath, const std::string& playerPath, const std::string& weaponsPath, std::string& err) {
    if (!world.load(itemsPath, worldPath, enemiesPath, playerPath, weaponsPath, err)) return false;
    state = new GameState(world);
    state->setRoom(world.startRoom);

    srand(static_cast<unsigned int>(time(nullptr)));
    return true;
}

void Engine::loop() {
    std::cout << "Type 'help' for commands.\n";
    doLook();

   

    for (std::string line; std::cout << "\n> " && std::getline(std::cin, line); ) {
        Command cmd = parseCommand(line);
        if (cmd.verb.empty()) continue;

        if (cmd.verb == "quit" || cmd.verb=="exit") break;
        else if (cmd.verb == "help") {
            std::cout << "Commands: look, go <dir>, take <item>, drop <item>, use <item> [on <dir|item>], equip <weapon>, attack <enemy>, inventory, weapons, status, quit\n";
        } 
        else if (cmd.verb == "look") {
            doLook(); checkEnemyAttack();
        }
        else if (cmd.verb == "equip") {
            EquipWeapon(cmd.args);
            checkEnemyAttack();
        }
        else if (cmd.verb == "attack") {
            doAttack(cmd.args);
        }
        else if (cmd.verb == "weapons") {
            doWeaponsInventory();
            checkEnemyAttack();
        }
        else if (cmd.verb == "go" && !cmd.args.empty()) {
            doGo(cmd.args[0]);
            checkEnemyAttack();
        }
        else if (cmd.verb == "take" && !cmd.args.empty()) {
            doTake(cmd.args[0]);
            checkEnemyAttack();
        }
        else if (cmd.verb == "drop" && !cmd.args.empty()) {
            doDrop(cmd.args[0]);
            checkEnemyAttack();
        }
        else if (cmd.verb == "inventory") {
            doInventory();
            checkEnemyAttack();
        }
        else if (cmd.verb == "use") {
            doUse(cmd.args);
            checkEnemyAttack();
        }
        else if (cmd.verb == "status") {
            doStatus();
        }
        else std::cout << "I don't understand.";
    }
}



std::string Engine::isEnemyPresent() const {
Room* r = const_cast<Room*>(state->room());

// Check if there's an enemy with the same ID as the current room
const auto* room_enemy = world.getEnemy(r->id);
if (room_enemy) {
    return room_enemy-> name;
}

return "";
}

void Engine::checkEnemyAttack() {
    const Room* r = state->room();
    if (!r) return;
    
    const auto* enemy = world.getEnemy(r->id);
    if (!enemy) return;
    
    int currentHealth = state->getEnemyHealth(r->id, enemy->health);
    if (currentHealth <= 0) return;
    
    if (rand() % 100 < 30) {
        const auto* player = world.getPlayer("player");  
        if (!player) return;
        
        int playerHp = state->getPlayerHealth("player", player->health);
        std::cout << "\n*** " << enemy->name << " attacks you for " << enemy->damage << " damage! ***\n";
        state->damagePlayer("player", enemy->damage);  
        
        playerHp = state->getPlayerHealth("player", player->health);
        std::cout << "Your health: " << playerHp << "/" << player->health << "\n";
        
        if (state->isPlayerDead("player")) {
            std::cout << "\n=== YOU DIED ===\n";
            std::cout << "Game Over.\n";
            exit(0);
        }
    }
}



std::string Engine::doWeaponsInventory() const {
    auto snap = state->weapons().snapshot();
    if (snap.empty()) { std::cout << "You have no weapons.\n";  return ""; }
    
    std::cout << "You carry:\n";
    for (auto& kv : snap) {
        const auto* def = world.getWeapon(kv.first);
        std::cout << "- " << (def?def->name:kv.first) << " x" << kv.second << "\n";
    }
    
    return "";

}

void Engine::doLook() const {
    const Room* r = state->room();
    if (!r) { std::cout << "You are nowhere."; return; }
    std::cout << r->name << "\n" << r->desc << "\n";

    //Show enemy first
    std::string enemy = isEnemyPresent();

    if (!enemy.empty()) {
        // Get the full enemy definition to print description
        Room* r_mut = const_cast<Room*>(r);
        const auto* enemy = world.getEnemy(r_mut->id);
        if (enemy) {
            std::cout << "A " << enemy->name << " is here! " << enemy->desc << "\n";
        }
    }

    if (!r->items.empty()) {
        std::cout << "You see: ";
        for (size_t i=0;i<r->items.size();++i) {
            const auto* def = world.getItem(r->items[i]);
            std::cout << (def?def->name:r->items[i]);
            if (i+1<r->items.size()) std::cout << ", ";
        }
        std::cout << ".\n";
    }

    if (!r->weapons.empty()) {
        std::cout << "You see weapons: ";
        for (size_t i=0;i<r->weapons.size();++i) {
            const auto* def = world.getWeapon(r->weapons[i]);
            std::cout << (def?def->name:r->weapons[i]);
            if (i+1<r->weapons.size()) std::cout << ", ";
        }
        std::cout << ".\n";
    }
    if (!r->exits.empty()) {
        std::cout << "Exits: ";
        bool first=true;
        for (auto& kv : r->exits) {
            if (!first) std::cout << ", ";
            std::cout << kv.first;
            first=false;
        }
        std::cout << "\n";
    }

    
}

void Engine::EquipWeapon(const std::vector<std::string>& args) {
    if (args.empty()) { 
        std::cout << "Equip what?\n"; 
        return; 
    }

    // Build the weapon name from arguments 
    std::string weaponName;
    for (const auto& arg : args) {
        if (!weaponName.empty()) weaponName += " ";
        weaponName += arg;
    }

    // Convert to lowercase for comparison
    std::string weaponNameLower = weaponName;
    std::transform(weaponNameLower.begin(), weaponNameLower.end(), weaponNameLower.begin(), ::tolower);

    // Check if weapon exists in inventory
    auto snap = state->weapons().snapshot();
    bool weaponFound = false;
    std::string weaponId;

    for (auto& kv : snap) {
        const auto* def = world.getWeapon(kv.first);
        if (def) {
            std::string defNameLower = def->name;
            std::transform(defNameLower.begin(), defNameLower.end(), defNameLower.begin(), ::tolower);
            
            if (weaponNameLower == defNameLower) {
                weaponFound = true;
                weaponId = kv.first;
                weaponName = def->name;  
                break;
            }
        }
        
        // Also check by ID
        std::string idLower = kv.first;
        std::transform(idLower.begin(), idLower.end(), idLower.begin(), ::tolower);
        if (weaponNameLower == idLower) {
            weaponFound = true;
            weaponId = kv.first;
            if (def) weaponName = def->name;
            break;
        }
    }

    if (!weaponFound) {
        std::cout << "You don't have that weapon.\n";
        return;
    }

    // Equip the weapon
    state->equipWeapon(weaponId);
    std::cout << "You equip " << weaponName << " from your inventory.\n";
}

void Engine::doAttack(const std::vector<std::string>& args) {


    if (args.empty()) { std::cout << "Attack what?"; return; }

    std::string targetName;
    for (const auto& arg : args) {
        if (!targetName.empty()) targetName += " ";
        targetName += arg;
    }

    std::string enemy = isEnemyPresent();

    std::string targetLower = targetName;
    std::string enemyLower = enemy;
    std::transform(targetLower.begin(), targetLower.end(), targetLower.begin(), ::tolower);
    std::transform(enemyLower.begin(), enemyLower.end(), enemyLower.begin(), ::tolower);

    if (enemy.empty()) { std::cout << "There's no enemy here to attack.\n"; return; }

    if (targetLower != enemyLower) {
        std::cout << "There's no enemy here named that.\n";
        return;
    }

    // Get current health from state

    Room* r = const_cast<Room*>(state->room());
    auto room_enemy = world.getEnemy(r->id);
    int currentHealth = state->getEnemyHealth(r->id, room_enemy->health);
    
    if (currentHealth <= 0) {
        std::cout << room_enemy->name << " is already dead.\n";
        return;
    }

    // Get damage from equipped weapon
    int damageDealt = 5; // base damage
    std::string weaponUsed = "your fists";
    
    if (state->hasEquippedWeapon()) {
        const auto* weapon = world.getWeapon(state->getEquippedWeapon());
        if (weapon) {
            damageDealt = weapon->damage;  // USE EQUIPPED WEAPON'S DAMAGE
            weaponUsed = weapon->name;
        }
    }

    std::cout << "You attack " << room_enemy->name << " with " << weaponUsed << "!\n";
    state->damageEnemy(r->id, damageDealt);

    currentHealth = state->getEnemyHealth(r->id, room_enemy->health);
    
    if (currentHealth <= 0) {
        std::cout << room_enemy->name << " has been defeated!\n";
    } else {
        std::cout << room_enemy->name << " has " << currentHealth << " health remaining.\n";
    }

}

void Engine::doGo(const std::string& dir) {
    Room* r = const_cast<Room*>(state->room());
    if (!r) return;
    auto it = r->exits.find(dir);
    if (it == r->exits.end()) { std::cout << "No exit that way."; return; }

    std::string lockMsg;
    if (world.isExitLocked(*r, dir, lockMsg)) { std::cout << lockMsg << "\n"; return; }

    // requirement based on tags (need light etc)
    for (const auto& req : r->requirements) {
        if (req.enter == it->second) {
            // check if inventory has an item with that tag
            bool ok = false;
            for (auto& pair : state->inv().snapshot()) {
                const auto* def = world.getItem(pair.first);
                if (def) {
                    for (auto& t : def->tags) if (t == req.requiresTag) ok = true;
                }
            }
            if (!ok) { std::cout << req.message << "\n"; return; }
        }
    }

    state->setRoom(it->second);
    doLook();
}

void Engine::doTake(const std::string& what) {
    //Check if item
    Room* r = const_cast<Room*>(state->room());
    auto it = std::find(r->items.begin(), r->items.end(), what);
    if (it != r->items.end()) {
        const auto* def = world.getItem(what);
        if (def && !def->portable) { 
            std::cout << "You can't take that here."; 
            return; 
        }
        state->inv().add(what);
        r->items.erase(it);
        std::cout << "Taken.";
        return;
    }

    // Check if weapon by ID or name
    std::string whatLower = what;
    std::transform(whatLower.begin(), whatLower.end(), whatLower.begin(), ::tolower);
    
    // Loop through weapons actually in the room
    for (auto wit = r->weapons.begin(); wit != r->weapons.end(); ++wit) {
        std::string weaponId = *wit;
        const auto* weaponDef = world.getWeapon(*wit);
        
        // Check if matches by ID
        std::string idLower = *wit;
        std::transform(idLower.begin(), idLower.end(), idLower.begin(), ::tolower);
        
        if (idLower == whatLower) {
            state->weapons().add(weaponId);  // Add by actual ID
            r->weapons.erase(wit);
            std::cout << "You picked up the " << (weaponDef ? weaponDef->name : weaponId) << ".\n";
            return;
        }
        
        // Check if matches by name
        if (weaponDef) {
            std::string nameLower = weaponDef->name;
            std::transform(nameLower.begin(), nameLower.end(), nameLower.begin(), ::tolower);
            
            if (nameLower == whatLower) {
                state->weapons().add(*wit);  // Add by actual ID
                r->weapons.erase(wit);
                std::cout << "You picked up the " << weaponDef->name << ".\n";
                return;
            }
        }
    }

    
    std::cout << "No such weapon here.";
    
}

void Engine::doDrop(const std::string& what) {
    if (!state->inv().contains(what)) { std::cout << "You don't have that."; return; }
    state->inv().remove(what);
    Room* r = const_cast<Room*>(state->room());
    r->items.push_back(what);
    std::cout << "Dropped.";
}

void Engine::doInventory() const {
    auto snap = state->inv().snapshot();
    if (snap.empty()) { std::cout << "Inventory is empty."; return; }
    std::cout << "You carry:\n";
    for (auto& kv : snap) {
        const auto* def = world.getItem(kv.first);
        std::cout << "- " << (def?def->name:kv.first) << " x" << kv.second << "\n";
    }
}

void Engine::applyTriggers(Room& r, const std::string& cmd) {
    for (auto& t : r.triggers) {
        if (t.on == cmd) {
            for (auto& e : t.effects) {
                if (e.type == "unlock") world.unlockExit(r, e.exit);
                else if (e.type == "say") std::cout << e.text << "\n";
            }
        }
    }
}

void Engine::doUse(const std::vector<std::string>& args) {
    if (args.empty()) { std::cout << "Use what?"; return; }

    std::string itemToUse = args[0];

    if (!state->inv().contains(itemToUse)) { std::cout << "You don't have that."; return; }

    std::string phrase = "use " + itemToUse;

    if (args.size() >= 3 && args[1] == "on") phrase += " on " + args[2];

    Room* r = const_cast<Room*>(state->room());
    applyTriggers(*r, phrase);

    std::cout << "You use " << itemToUse << (args.size()>=3 ? " on "+args[2] : "") << ".\n";
}

void Engine::doStatus() {
    const auto* player = world.getPlayer("player");  
    if (!player) {
        std::cout << "Player data not found.\n";
        return;
    }
    std::string playerName = player->name;
    std::cout << playerName << "'s Status:\n";
    int playerHp = state->getPlayerHealth("player", player->health);
    std::cout << "Your health: " << playerHp << "/" << player->health << "\n";
    
    if (state->hasEquippedWeapon()) {
        const auto* weapon = world.getWeapon(state->getEquippedWeapon());
        if (weapon) {
            std::cout << "Equipped weapon: " << weapon->name << " (Damage: " << weapon->damage << ")\n";
        } else {
            std::cout << "Equipped weapon: Unknown\n";
        }
    } else {
        std::cout << "No weapon equipped.\n";
    }
}


