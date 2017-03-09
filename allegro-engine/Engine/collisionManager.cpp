#include <list>
#include "actorManager.h"
#include "collisionManager.h"

namespace Advanced2D
{
    CollisionManager::CollisionManager(){

    }

    void CollisionManager::update(){
        std::list<Actor*>::iterator first;
        std::list<Actor*>::iterator last;
        first = g_engine->actor_manager->get_begin_iterator();
        last = g_engine->actor_manager->get_end_iterator();

        if((*first) != NULL && (*last) != NULL)
        {
            while(first != g_engine->actor_manager->get_end_iterator())
            {
                if((*first)->isAlive() && (*first)->getIsDetected())
                {
                    while((*first) != (*last))
                    {
                        if((*last)->isAlive() && (*last)->getIsDetected() && (*last) != (*first))
                        {
                            if(Mask::check_ppcollision((*first)->getGraphMask(), (*last)->getGraphMask(), (*first)->getX(), (*first)->getY(), (*last)->getX(), (*last)->getY()))
                            {
                                game_collision((*first), (*last));
                            }
                        }
                        last--;
                    }
                }
                first++;
            }
        }
    }
}; //namespace
