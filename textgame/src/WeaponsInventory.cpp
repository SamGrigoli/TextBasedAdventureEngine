#include "WeaponsInventory.hpp"

bool WeaponsInventory::add(const std::string& id, int qty) {
    weapons[id] += qty;
    return true;
}

bool WeaponsInventory::remove(const std::string& id, int qty) {
    auto it = weapons.find(id);
    if (it == weapons.end() || it->second < qty) return false;
    it->second -= qty;
    if (it->second == 0) weapons.erase(it);
    return true;
}

bool WeaponsInventory::contains(const std::string& id) const {
    return weapons.find(id) != weapons.end();
}