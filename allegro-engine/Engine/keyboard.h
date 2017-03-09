#ifndef KEYBOARD_H
#define KEYBOARD_H

#include <allegro.h>
#include "peripheral.h"

class Keyboard : public Peripheral{
    public:
        Keyboard();
        state_t get_state(component_t comp);
        component_t get_change();
        std::string get_component_name(component_t comp);
        void reset();
    protected:
        int old_state[KEY_MAX];
};
#endif

