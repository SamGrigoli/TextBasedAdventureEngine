#pragma once
#include <unordered_map> 
#include <string>

class Health        
{
    public:
        //Sets the max health and current health to the same value
        void setMax(int v) { max = v; cur = v; }
        //Sets the current health to a specific value
        void setCur(int v) { cur = std::max(0, std::min(v, max)); }
        //Returns the current health value
        int getCur() const { return cur; }
        //Returns the max health value
        int getMax() const { return max; }
        //Returns true if current health is 0 or less
        bool isDead() const { return cur <= 0; }
        //Heals the entity by a specific amount
        void heal(int v) { setCur(cur + v); }
        //Damages the entity by a specific amount
        void damage(int v) { setCur(cur - v); }

    private:
        int max = 100; //Max health value
        int cur = 100; //Current health value
};