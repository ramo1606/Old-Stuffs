#include "pixel.h"

namespace Advanced2D
{
    Pixel::Pixel(int col) : ActorGraphic(){
        color=col;
        // Se creara la mascara de un pixel a partir de un bitmap vacio
        BITMAP *tmp_bmp=create_bitmap(1,1);
        clear_to_color(tmp_bmp, 1); // cualquier color
        mask=new Mask;
        mask->create(tmp_bmp);
        destroy_bitmap(tmp_bmp);
    }

    Pixel::~Pixel(){
    }

    void Pixel::draw(BITMAP *bmp, int x, int y){
        putpixel(bmp, x, y, color);
    }

    int Pixel::get_w(){
        return 1;
    }

    int Pixel::get_h(){
        return 1;
    }

    Mask *Pixel::get_mask(){
        return mask;
    }
}; //namespace
