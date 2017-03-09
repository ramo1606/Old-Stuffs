#include "particle.h"

namespace Advanced2D
{
        Particle::Particle()
    {
        //ctor
    }

    Particle::~Particle()
    {
        //dtor
    }

    void Particle::move()
    {
        setX(getPosition().getX() + getVelocity().getX());
        setY(getPosition().getY() + getVelocity().getY());
    }

    void Particle::hit(Actor *a, int damage)
    {
    }
};
