#include "Inventory.hpp"

bool Inventory::add(const std::string& id, int qty) {
    items[id] += qty;
    return true;
}

bool Inventory::remove(const std::string& id, int qty) {
    auto it = items.find(id);
    if (it == items.end() || it->second < qty) return false;
    it->second -= qty;
    if (it->second == 0) items.erase(it);
    return true;
}

bool Inventory::contains(const std::string& id) const {
    return items.find(id) != items.end();
}
