#include "star.h"

namespace Advanced2D
{
    Star::Star(){
        reinit();
    }

    void Star::reinit(){
        setX(rand()%SCREEN_W);
        setY(0.);
        vy=1+rand()%4;
    }

    void Star::move(){
        setY(getY() + vy);
        if (getY()>SCREEN_H){
            reinit();
        }
    }

    void Star::hit(Actor *a, int damage)
    {
        g_engine->actor_manager->del(this);
    }
};
