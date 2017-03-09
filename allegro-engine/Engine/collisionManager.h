#ifndef COLLISIONMANAGER_H
#define COLLISIONMANAGER_H

#include "mask.h"

namespace Advanced2D
{
    class CollisionManager{
        public:
            CollisionManager();

            typedef enum{
                BOUNDING_BOX,
                PP_COLLISION
            }collision_method_t;

            void update();

        protected:
    };
}; //namespace

#endif
