#include "particleemitter.h"

namespace Advanced2D
{
    ParticleEmitter::ParticleEmitter(std::string particle_p) : Actor()
    {
        //initialize particles to defaults
        particle = particle_p;
        m_max = 100;
        length = 100;
        alphaMin = 254;    alphaMax = 255;
        minR = 0; maxR = 255;
        minG = 0; maxG = 255;
        minB = 0; maxB = 255;
        spread = 50;
        scale = 1.0f;
    }

    ParticleEmitter::~ParticleEmitter()
    {
        //destroy particles
        for (iter i = particles.begin(); i != particles.end(); ++i)
        {
            delete *i;
        }
        particles.clear();
    }

    void ParticleEmitter::add()
    {
        static double PI_DIV_180 = 3.1415926535 / 180.0f;
        double vx,vy;

        //create a new particle
        Particle *particle_a = new Particle();
        TransSprite *p = new TransSprite();
        p->loadImage(particle);
        p->setSize(p->getWidth(), p->getHeight());
        particle_a->setPosition(getPosition().getX(), getPosition().getY());
        vx = (double)(rand()%30 - 15)/10.0f;
		vy = (double)(rand()%30 - 15)/10.0f;
        particle_a->setVelocity(vx, vy);
        particle_a->setActorGraphic(p);

        //add some randomness to the spread
        double variation = (rand() % spread - spread/2) / 100.0f;

        //set linear velocity
        //double dir = this->getDirection() - 90.0;
        //vx = cos( dir * PI_DIV_180) + variation;
        //vy = sin( dir * PI_DIV_180) + variation;
        //particle_a->setVelocity(vx * this->getVelocity().getX(),vy * this->getVelocity().getY());

        //set random color based on ranges
        int r = rand()%(maxR-minR)+minR;
        int g = rand()%(maxG-minG)+minG;
        int b = rand()%(maxB-minB)+minB;
        int a = rand()%(alphaMax-alphaMin)+alphaMin;

        //set the scale
        p->setScale( scale );

        //add particle to the emitter
        particles.push_back(particle_a);
    }

    void ParticleEmitter::draw(BITMAP *bmp)
    {
        //draw particles
        for (iter i = particles.begin(); i != particles.end(); ++i)
        {
            (*i)->draw(bmp);
        }
    }

    void ParticleEmitter::update()
    {
        //do we need to add a new particle?
        if ((int)particles.size() < m_max)
        {
            //trivial but necessary slowdown
            //if (timer.stopwatch(1))
            add();
        }

        for (iter i = particles.begin(); i != particles.end(); ++i)
        {
            //update particle's position
            //(*i)->setX(getX() + getVelocity().getX());
            //(*i)->setY(getY() + getVelocity().getY());
            //(*i)->setEmitterPosition(getPosition().getX(), getPosition().getY());
            (*i)->update();

            //is particle beyond the emitter's range?
            if ( (*i)->getPosition().Distance(this->getPosition()) > length)
            {
                //reset particle to the origin
                (*i)->setX(getPosition().getX());
                (*i)->setY(getPosition().getY());
            }
        }
    }

    void ParticleEmitter::setAlphaRange(int min_p,int max_p)
    {
        alphaMin=min_p;
        alphaMax=max_p;
    }

    void ParticleEmitter::setColorRange(int r1,int g1,int b1,int r2,int g2,int b2)
    {
        minR = r1; maxR = r2;
        minG = g1; maxG = g2;
        minB = b1; maxB = b2;
    }
}
