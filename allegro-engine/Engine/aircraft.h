#ifndef AIRCRAFT_H
#define AIRCRAFT_H

#include <allegro.h>
#include "advanced2d.h"
#include "controllableActor.h"

namespace Advanced2D
{
    class Actor;

    class AirCraft : public ControllableActor{
        public:
            AirCraft();

            typedef enum{
                DOWN,
                UP,
                LEFT,
                RIGHT,
                SHOOT
            }action_t;

            void update();
            void doAction(ControllableObject::action_t act, int magnitude);
            void move();
            void hit(Actor *a, int damage);
            ControllableObject::action_t getCurrentAction();

        protected:
            void shootBullet();
            ControllableObject::action_t current_action;
    };
}; //namespace
#endif // AIRCRAFT_H
