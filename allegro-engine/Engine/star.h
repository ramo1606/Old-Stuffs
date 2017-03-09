#ifndef STAR_H
#define STAR_H

#include <allegro.h>
//#include "actor.h"
#include "actorManager.h"

namespace Advanced2D
{
    class Star : public Actor{
        public:
            Star();
            void move();
            void hit(Actor *a, int damage);

        protected:
            void reinit();
            int vy;
    };
}; //namespace
#endif // STAR_H
