#include "transsprite.h"

namespace Advanced2D
{
    TransSprite::TransSprite() : Sprite()
    {
    }

    TransSprite::~TransSprite()
    {
        //dtor
    }

    void TransSprite::draw(BITMAP *bmp, int x, int y){
        if(imageLoaded)
        {
            set_alpha_blender();
            draw_trans_sprite(bmp, p_bmp, x, y);
        }
    }
};
