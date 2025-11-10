#pragma once 
#include <string>
#include <vector>

struct EnemyDef 
{
    //id: For the engine to reference the enemy
    //name: Enemy name. What the player sees
    //desc: The description of the enemy
    std::string id, name, desc; 
    //health: The health points of the enemy
    int health;
    //damage: The damage dealt by the enemy
    int damage;
    //tags: List of enemy properties
    std::vector<std::string> tags;
};