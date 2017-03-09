#ifndef PIXEL_H
#define PIXEL_H

#include <allegro.h>
#include "actorGraphic.h"
#include "mask.h"

namespace Advanced2D
{
    class Pixel : public ActorGraphic{
        public:
            Pixel(int col);
            ~Pixel();

            void draw(BITMAP *bmp, int x, int y);
            int get_w();
            int get_h();
            Mask *get_mask();

        protected:
            int color;
            Mask *mask;
    };
}; //namespace
#endif // PIXEL_H
