#ifndef BULLET_H
#define BULLET_H

#include <allegro.h>
#include "actor.h"
#include "controllableActor.h"

namespace Advanced2D
{
    class Bullet : public Actor{
        public:
            Bullet(ControllableActor *owner_p);
            void move();
            void hit(Actor *a, int damage);

        protected:
            void reinit();
            ControllableActor *owner;
    };
}; //namespace
#endif // BULLET_H
