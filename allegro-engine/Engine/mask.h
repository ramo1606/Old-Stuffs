#include <allegro.h>

using namespace std;

#ifndef MASK
#define MASK

class Mask{
    public:
        /*Constructor*/
        Mask();
        /*Destructor*/
        ~Mask();
        /*Deteccion perfecta por pixel, retorna 1 si hay colicion y 0 en caso contrario*/
        static int check_ppcollision(Mask *m1, Mask *m2, int x1, int y1, int x2,
        int y2);
        /*Deteccion de colision bounding box, retorna 1 si hay colicion y 0 en caso contrario*/
        static int check_bbcollision(Mask *m1, Mask *m2, int x1, int y1, int x2,
        int y2);
        /*Crea una maskara a partir de un mapa de bits*/
        void create(BITMAP *bmp);
        /*Retorna bb_height*/
        int get_bb_height() { return bb_height; }
        /*Retorna bb_width*/
        int get_bb_width() { return bb_width; }
        /*Retorna max chunk*/
        int get_max_chunk() { return max_chunk; }
        /*Retorna num_y*/
        int get_num_y() { return num_y; }
        /*Retorna la mascara de bits*/
        unsigned long int get_sp_mask(int i, int j) { return sp_mask[i][j]; }

    protected:
        int bb_height;
        int bb_width;
        int max_chunk;
        int num_y;
        unsigned long int **sp_mask;
};
#endif
