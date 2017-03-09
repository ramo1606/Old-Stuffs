#ifndef ACTORGRAPHIC_H
#define ACTORGRAPHIC_H

#include <allegro.h>
#include <string>
#include "mask.h"

namespace Advanced2D
{
    class Actor;

    /*Esta clase se encarga de manejar el aspecto grafico de un actor*/
    class ActorGraphic{
        public:
            /*Constructor*/
            ActorGraphic();
            /*Destructor*/
            virtual ~ActorGraphic();
            /**/
            virtual void init();
            /**/
            virtual void update();
            /**/
            virtual void draw(BITMAP *bmp, int x, int y);
            /**/
            virtual int getWidth();
            /**/
            virtual int getHeight();
            /*Retorna la mascara de colision*/
            virtual Mask* getMask();
            /**/
            virtual bool loadImage(std::string filename);
            /**/
            virtual bool getImageLoaded();
            /**/
            virtual BITMAP *getBitMap();
            /**/
            virtual bool *setBitMap(BITMAP *image);


        protected:
            bool imageLoaded;
            BITMAP *p_bmp;
    };
};
#endif

