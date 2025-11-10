#pragma once //Basically ifndef, tells compiler to only include once per build
#include <string>
#include <vector>

//This struct will describe what each item is in the game
struct ItemDef 
{
    //id: For the engine to refrence the item
    //name: Item name. What the player sees
    //desc: The description of the item
    std::string id, name, desc; 
    //portable: If the player can pick up the item or not
    bool portable = true;
    //tags: List of item properties
    std::vector<std::string> tags;
};