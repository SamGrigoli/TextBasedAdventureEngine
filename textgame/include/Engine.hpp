#pragma once
#include <string>
#include "World.hpp"
#include "GameState.hpp"
#include "Health.hpp"


class Engine 
{
    public:
        bool init(const std::string& itemsPath, const std::string& worldPath, const std::string& enemiesPath, const std::string& playerPath,const std::string& weaponsPath, std::string& err);
        void loop();
    private:
        void doLook() const;
        void doGo(const std::string& dir);
        void doTake(const std::string& what);
        void doDrop(const std::string& what);
        void doUse(const std::vector<std::string>& args);
        void doInventory() const;
        void applyTriggers(Room& r, const std::string& normalizedCommand);
        std::string isEnemyPresent() const;
        void doAttack(const std::vector<std::string>& args);
        std::string doWeaponsInventory() const;
        void EquipWeapon(const std::vector<std::string>& args);
        void checkEnemyAttack();
        void doStatus();

        World world;
        GameState* state = nullptr;

};