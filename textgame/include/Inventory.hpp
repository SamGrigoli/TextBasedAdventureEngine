#pragma once
#include <unordered_map> //Like a hashmap. Needs a string key to access
#include <string>

//Defines the inventory system
class Inventory 
{
    public:
        //Adds one item to the inventory
        bool add(const std::string& id, int qty = 1);
        //Removes one item from the inventory
        bool remove(const std::string& id, int qty = 1);
        //Tells me how much of a specific item the inventory has
        int count(const std::string& id) const;
        //Returns true if the inventory contains that item
        bool contains(const std::string& id) const;
        //returns a copy of the inventory map
        std::unordered_map<std::string, int> snapshot() const {return items;}
    
    private: 
        //Data storage for the inventory
        std::unordered_map<std::string, int> items;

};