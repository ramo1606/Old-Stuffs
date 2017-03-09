#ifndef PARTICLEEMITTER_H
#define PARTICLEEMITTER_H

#include "particle.h"
#include "transsprite.h"

namespace Advanced2D
{
    class ParticleEmitter : public Actor
    {
        public:
            ParticleEmitter(std::string particle_p);
            virtual ~ParticleEmitter();
            void draw(BITMAP *bmp);
            void update();
            //void move();
            void add();

            void setMax(int num) { m_max = num; }
            void setAlphaRange(int min_p,int max_p);
            void setColorRange(int r1,int g1,int b1,int r2,int g2,int b2);
            void setSpread(int value) { spread = value; }
            void setLength(double value) { length = value; }
            void setScale(double value) { scale = value; }

        protected:
        private:
            typedef std::vector<Particle*>::iterator iter;
            std::vector<Particle*> particles;
            std::string particle;
            double length;
            int m_max;
            int alphaMin,alphaMax;
            int minR,minG,minB,maxR,maxG,maxB;
            int spread;
            double scale;
    };
};
#endif // PARTICLEEMITTER_H
