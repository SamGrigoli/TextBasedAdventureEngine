#ifndef PLAYER_HPP
#define PLAYER_HPP

#include <string>
#include <vector>

struct PlayerDef {
    std::string id = "player";  // Add ID like enemies have
    std::string name = "Player";
    std::string desc = "It's you!";
    int health = 100;
    int damage = 5;
    std::vector<std::string> tags;  // Optional, for consistency
};

#endif