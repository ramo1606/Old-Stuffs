#ifndef TRANSSPRITE_H
#define TRANSSPRITE_H

#include "sprite.h"

namespace Advanced2D
{
    class TransSprite : public Sprite{
        public:
            TransSprite();
            ~TransSprite();
            void draw(BITMAP *bmp, int x, int y);

        protected:
        private:
    };
};
#endif // TRANSSPRITE_H
