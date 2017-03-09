#ifndef BITMAP_H
#define BITMAP_H

#include <allegro.h>
#include "actorGraphic.h"

namespace Advanced2D
{
    class Bitmap : public ActorGraphic{
    public:
        Bitmap(Actor *aowner, BITMAP *bmp);
        void draw(BITMAP *bmp);
        int get_w();
        int get_h();

    protected:
    };
}; //namespace


#endif // BITMAP_H
