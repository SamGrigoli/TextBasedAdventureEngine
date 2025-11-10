#pragma once
#include <string>
#include "Inventory.hpp"
#include "World.hpp"
#include "WeaponsInventory.hpp"

class GameState {
    public:
        std::unordered_map<std::string, int> enemyHealth;
        std::unordered_map<std::string, int> playerHealth;  
        
        explicit GameState(World& w) : world(w) {}
        
        void setRoom(const std::string& id) { currentRoom = id; }
        std::string equippedWeapon; 
        const Room* room() const { return world.getRoom(currentRoom); }
        Inventory& inv() { return inventory; }
        const Inventory& inv() const { return inventory; }
        const WeaponsInventory& weapons() const { return weaponsInventory; }
        WeaponsInventory& weapons() { return weaponsInventory; }

        // Enemy health
        int getEnemyHealth(const std::string& roomId, int defaultHealth) {
            if (enemyHealth.find(roomId) == enemyHealth.end()) {
                enemyHealth[roomId] = defaultHealth;
            }
            return enemyHealth[roomId];
        }
        
        void damageEnemy(const std::string& roomId, int damage) {
            enemyHealth[roomId] -= damage;
        }
        
        bool isEnemyDead(const std::string& roomId) {
            return enemyHealth.find(roomId) != enemyHealth.end() && 
                enemyHealth[roomId] <= 0;
        }

        // Player health 
        int getPlayerHealth(const std::string& playerId, int defaultHealth) {
            if (playerHealth.find(playerId) == playerHealth.end()) {
                playerHealth[playerId] = defaultHealth;
            }
            return playerHealth[playerId];
        }
        
        void damagePlayer(const std::string& playerId, int damage) {
            playerHealth[playerId] -= damage;
        }
        
        void healPlayer(const std::string& playerId, int amount) {
            playerHealth[playerId] += amount;
        }
        
        bool isPlayerDead(const std::string& playerId) {
            return playerHealth.find(playerId) != playerHealth.end() && 
                playerHealth[playerId] <= 0;
        }

        void equipWeapon(const std::string& weaponId) {
            equippedWeapon = weaponId;
        }
        
        std::string getEquippedWeapon() const {
            return equippedWeapon;
        }
        
        bool hasEquippedWeapon() const {
            return !equippedWeapon.empty();
        }

    private:
        World& world;
        std::string currentRoom;
        Inventory inventory;
        WeaponsInventory weaponsInventory;
};