#include "Engine.hpp"
#include <iostream>
#include <fstream>
#include <nlohmann/json.hpp> 

int main(int argc, char* argv[]) {
    std::string err;
    Engine engine;

    std::string LOAD_FILE = "data/loadgame.json";


    std::ifstream loadFile(LOAD_FILE);
    if (!loadFile.is_open()) {
        std::cerr << "Failed to open " << LOAD_FILE << "\n";
        return 1;
    }

    nlohmann::json j;
    loadFile >> j;
    loadFile.close();

    std::string folderName = j.get<std::string>();

    if (!engine.init("data/" + folderName + "/items.json", "data/" + folderName + "/world.json", "data/" + folderName + "/enemies.json", "data/" + folderName + "/player.json", "data/" + folderName + "/weapons.json", err)) {
        std::cerr << "Init failed: " << err << "\n";
        return 1;
    }
    engine.loop();
    return 0;
}
