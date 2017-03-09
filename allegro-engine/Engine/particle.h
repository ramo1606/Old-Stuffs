#ifndef PARTICLE_H
#define PARTICLE_H

#include <allegro.h>
#include "actor.h"

namespace Advanced2D
{
    class Particle : public Actor
    {
        public:
            Particle();
            virtual ~Particle();
            void move();
            void hit(Actor *a, int damage);

        protected:
        private:
    };
};
#endif // PARTICLE_H
