#include "bullet.h"

Advanced2D::Engine *g_engine;

namespace Advanced2D
{
    Bullet::Bullet(ControllableActor *owner_p){
        owner = owner_p;
        //alive = 1;
        reinit();
    }

    void Bullet::reinit(){
        /*setX(owner->getGraphX());
        setY(owner->getGraphY() - owner->getHeight()/2);
        vy = -6;*/
    }

    void Bullet::move(){
        /*setY(getY() + vy);
        if(getY()<0)
        {
            alive = 0;
        }
        if(!alive)
        {
            g_engine->actor_manager->del(this);
        }*/
    }

    void Bullet::hit(Actor *a, int damage)
    {
        /*g_engine->actor_manager->del(this);*/
    }
}; //namespace
