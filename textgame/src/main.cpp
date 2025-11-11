#include "Engine.hpp"
#include <iostream>
#include <string>
#include <filesystem>

int main(int argc, char* argv[]) {
    std::string err;
    Engine engine;
    std::string gamePath;
    
    // Check if game path provided as argument
    if (argc > 1) {
        gamePath = std::string(argv[1]) + "/";
    } else {
        // Ask user for game folder
        std::cout << "Enter game folder path (or just folder name if in ../data/): ";
        std::string input;
        std::getline(std::cin, input);
        
        // Check if it's a full path or just a folder name
        if (std::filesystem::exists(input)) {
            gamePath = input + "/";
        } else if (std::filesystem::exists("../data/" + input)) {
            gamePath = "../data/" + input + "/";
        } else {
            std::cerr << "Game folder not found: " << input << "\n";
            return 1;
        }
    }
    
    if (!engine.init(gamePath + "items.json", 
                     gamePath + "world.json", 
                     gamePath + "enemies.json", 
                     gamePath + "player.json", 
                     gamePath + "weapons.json", 
                     err)) {
        std::cerr << "Init failed: " << err << "\n";
        std::cerr << "Make sure all JSON files exist in: " << gamePath << "\n";
        return 1;
    }
    
    engine.loop();
    return 0;
}