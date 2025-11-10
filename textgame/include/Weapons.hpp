#pragma once //Basically ifndef, tells compiler to only include once per build
#include <string>
#include <vector>

//This struct will describe what each weapon is in the game
struct WeaponsDef 
{
    //id: For the engine to refrence the weapon
    //name: Weapon name. What the player sees
    //desc: The description of the weapon
    std::string id, name, desc;
    //damage: The damage dealt by the weapon
    int damage = 10; 
    std::vector<std::string> tags;

};