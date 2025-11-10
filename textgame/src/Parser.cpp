// Parser.cpp
#include "Parser.hpp"
#include <sstream>
#include <algorithm>
#include <cctype>

static std::string lower(std::string s){
    std::transform(s.begin(), s.end(), s.begin(),
                   [](unsigned char c){ return std::tolower(c); });
    return s;
}

Command parseCommand(const std::string& line) {
    std::istringstream iss(line);
    std::vector<std::string> tokens;
    for (std::string t; iss >> t; ) tokens.push_back(lower(t));
    if (tokens.empty()) return {"",{}};

    // shorthands
    if (tokens.size()==1) {
        if (tokens[0] == "n") return {"go", {"north"}};
        if (tokens[0] == "s") return {"go", {"south"}};
        if (tokens[0] == "e") return {"go", {"east"}};
        if (tokens[0] == "w") return {"go", {"west"}};
        if (tokens[0] == "i" || tokens[0]=="inv") return {"inventory",{}};
        if (tokens[0] == "look" || tokens[0]=="l") return {"look",{}};
    }

    Command c; c.verb = tokens.front();
    tokens.erase(tokens.begin());
    c.args = std::move(tokens);
    return c;
}
