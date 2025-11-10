#pragma once
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>
#include "Item.hpp"
#include "Enemy.hpp"
#include "Weapons.hpp"
#include "Player.hpp"

//Locked door
struct ExitLock 
{
    std::string exit, requires, message;
};

//Blocked path. This checks for item tag/condition instead
struct Requirements 
{
    std::string enter, requiresTag, message;
};

struct Room
{
    //id: internal name
    //name: display name
    //desc: description shown to the player
    //exits: map of direction to room id - {"north" : "cave"}
    //items: list of item ids
    //weapons: list of weapon ids
    //locks: list of locked exits
    //requirements: rules to enter room
    std::string id, name, desc;
    std::unordered_map<std::string, std::string> exits;
    std::vector<std::string> items;
    std::vector<std::string> weapons;
    std::vector<ExitLock> locks;
    std::vector<std::string> enemies;
    std::vector<Requirements> requirements;

    //Triggers for using items on objects and doors
    struct TriggerEffect 
    {
        std::string type, exit, text;
    };

    struct Trigger 
    {
        std::string on; std::vector<TriggerEffect> effects;
    };

    std::vector<Trigger> triggers; 


    
};

class World 
    {
        public:
        
            //Reads in from json file
            bool load(const std::string& itemsPath, const std::string& worldPath, const std::string& enemiesPath, const std::string& playerPath, const std::string& weaponsPath, std::string& err);
            //Gets room id
            const Room* getRoom(const std::string& id) const;
            //Gets item def
            const ItemDef* getItem(const std::string& id) const;
            //Gets weapon def
            const WeaponsDef* getWeapon(const std::string& id) const;
            //Gets enemy def
            const EnemyDef* getEnemy(const std::string& id) const;
            //Checks if moving dir from room r is locked
            bool isExitLocked(const Room& r, const std::string& dir, std::string& msg) const;
            //opens locked exit
            void unlockExit(Room& r, const std::string& dir);
            const PlayerDef* getPlayer(const std::string& id) const;


            std::unordered_map<std::string, ItemDef> items;
            std::unordered_map<std::string, EnemyDef> enemies;
            std::unordered_map<std::string, Room> rooms;
            std::unordered_map<std::string, WeaponsDef> weapons;
            std::unordered_map<std::string, PlayerDef> players;
            std::string startRoom;
            

    };