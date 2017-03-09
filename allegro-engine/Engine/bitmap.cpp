#include "bitmap.h"

namespace Advanced2D
{
    Bitmap::Bitmap(Actor *aowner) : ActorGraphic(aowner){
    }

    void Bitmap::draw(BITMAP *bmp){
        draw_sprite(bmp, bitmap, getX(), getY());
    }

    int Bitmap::getWidth(){
        return p_bmp->w;
    }

    int Bitmap::getHeight(){
        return p_bmp->h;
    }
}; //namespace

