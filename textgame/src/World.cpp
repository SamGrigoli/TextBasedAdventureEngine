// World.cpp
#include "World.hpp"
#include "Enemy.hpp"
#include "Weapons.hpp"
#include <fstream>
#include <nlohmann/json.hpp>
#include <iostream>
using nlohmann::json;

static std::vector<std::string> toVec(const json& j) {
    std::vector<std::string> v;
    for (auto& x : j) v.push_back(x.get<std::string>());
    return v;
}

bool World::load(const std::string& itemsPath, const std::string& worldPath, const std::string& enemiesPath, const std::string& playerPath, const std::string& weaponsPath, std::string& err) {
    try {
        std::ifstream fi(itemsPath), fw(worldPath), fe(enemiesPath), fp(playerPath), fc(weaponsPath);
        if (!fi || !fw || !fe || !fp || !fc) { err = "Cannot open data files"; return false; }

        json ji; fi >> ji;
        for (auto& it : ji["items"]) {
            ItemDef d;
            d.id = it["id"]; d.name = it["name"]; d.desc = it["desc"];
            if (it.contains("portable")) d.portable = it["portable"];
            if (it.contains("tags")) for (auto& t : it["tags"]) d.tags.push_back(t.get<std::string>());
            items[d.id] = std::move(d);
        }
        json jc; fc >> jc;
        for (auto& iw : jc["weapons"]) {
            WeaponsDef w;
            w.id = iw["id"]; w.name = iw["name"]; w.desc = iw["desc"]; w.damage = iw["damage"];
            //if (iw.contains("damage")) w.damage = iw["damage"];
            if (iw.contains("tags")) for (auto& t : iw["tags"]) w.tags.push_back(t.get<std::string>());
            weapons[w.id] = std::move(w);
        }

        json jw; fw >> jw;
        startRoom = jw["startRoom"];
        for (auto& jr : jw["rooms"]) {
            Room r;
            r.id = jr["id"]; r.name = jr["name"]; r.desc = jr["desc"];
            for (auto& [k,v] : jr["exits"].items()) r.exits[k] = v.get<std::string>();

            if (jr.contains("items")) r.items = toVec(jr["items"]);
            if (jr.contains("weapons")) r.weapons = toVec(jr["weapons"]);
            if (jr.contains("locks")) for (auto& l : jr["locks"]) {
                r.locks.push_back({l["exit"], l["requires"], l["message"]});
            }
            if (jr.contains("requirements")) for (auto& rq : jr["requirements"]) {
                r.requirements.push_back({rq["enter"], rq["requiresTag"], rq["message"]});
            }
            if (jr.contains("triggers")) for (auto& t : jr["triggers"]) {
                Room::Trigger trig; trig.on = t["on"];
                for (auto& e : t["effects"]) {
                    Room::TriggerEffect eff; eff.type = e["type"];
                    if (e.contains("exit")) eff.exit = e["exit"];
                    if (e.contains("text")) eff.text = e["text"];
                    trig.effects.push_back(std::move(eff));
                }
                r.triggers.push_back(std::move(trig));
            }
            rooms[r.id] = std::move(r);
        }

        json je; fe >> je;
        for (auto& en : je["enemies"]) {
            EnemyDef e;
            e.id = en["id"]; 
            e.name = en["name"]; 
            e.desc = en["desc"];
            
            // Optional fields with defaults
            if (en.contains("health")) e.health = en["health"];
            if (en.contains("damage")) e.damage = en["damage"];
            if (en.contains("tags")) {
                for (auto& t : en["tags"]) {
                    e.tags.push_back(t.get<std::string>());
                }
            }
            
            enemies[e.id] = std::move(e);
        }

    json jp; 
    fp >> jp;
    for (auto& pl : jp["players"]) {  
        PlayerDef p;
        p.id = pl["id"];
        p.name = pl["name"];
        p.desc = pl["desc"];
        
        // Optional fields with defaults
        if (pl.contains("health")) p.health = pl["health"];
        if (pl.contains("damage")) p.damage = pl["damage"];
        
        players[p.id] = std::move(p);
    }
        

        return true;
    } catch (std::exception& ex) { err = ex.what(); return false; }
}

const Room* World::getRoom(const std::string& id) const {
    auto it = rooms.find(id); return it==rooms.end()?nullptr:&it->second;
}
const ItemDef* World::getItem(const std::string& id) const {
    auto it = items.find(id); return it==items.end()?nullptr:&it->second;
}
const WeaponsDef* World::getWeapon(const std::string& id) const {
    auto it = weapons.find(id); return it==weapons.end()?nullptr:&it->second;
}

const EnemyDef* World::getEnemy(const std::string& id) const {
    auto it = enemies.find(id); return it==enemies.end()?nullptr:&it->second;
}

const PlayerDef* World::getPlayer(const std::string& id) const {
    auto it = players.find(id);
    return it == players.end() ? nullptr : &it->second;
}
bool World::isExitLocked(const Room& r, const std::string& dir, std::string& msg) const {
    for (auto& l : r.locks) if (l.exit==dir) { msg = l.message; return true; }
    return false;
}
void World::unlockExit(Room& r, const std::string& dir) {
    r.locks.erase(std::remove_if(r.locks.begin(), r.locks.end(),
                 [&](const ExitLock& l){ return l.exit==dir; }), r.locks.end());
}
