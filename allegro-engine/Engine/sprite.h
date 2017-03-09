#ifndef SPRITE_H
#define SPRITE_H

#include <allegro.h>
#include <vector>

#include "actor.h"
#include "controllableObject.h"
#include "collisionManager.h"
#include "actorGraphic.h"

namespace Advanced2D
{
    class Sprite : public ActorGraphic{
        public:

            typedef enum{
                DOWN,
                UP,
                LEFT,
                RIGHT
            }action_t;

            Sprite();
            ~Sprite();
            void init();
            void draw(BITMAP *bmp, int x, int y);
            void drawFrame(BITMAP *bmp, int x, int y);
            BITMAP *grabframe(BITMAP *source, int width, int height, int startx, int starty, int columns, int frame);
            /*Hace update si hay alguna accion*/
            void update(ControllableObject::action_t action);
            /*update standar*/
            void update();
            //void addFrame(BITMAP *bmp, int cx, int cy, int ticks);
            bool loadMasks(void);
            Mask *getMask();

            //image size
            void setSize(int width, int height);
            int getWidth();
            void setWidth(int value);
            int getHeight();
            void setHeight(int value);
            int getColumns();
            void setColumns(int value);

            int getFrameDelay();
            void setFrameDelay(int value);

            int getCurrentFrame();
            void setCurrentFrame(int value);

            int getTotalFrames();
            void setTotalFrames(int value);

            int getAnimationDirection();
            void setAnimationDirection(int value);

            double getRotation();
            void setRotation(double value);
            double getScale();
            void setScale(double value);

        protected:
            int width, height;
            int curFrame,totalFrames,animDir;
            int animColumns;
            int frameCount,frameDelay;
            int animStartx, animStarty;
            int faceAngle, moveAngle;
            double rotation, scaling;

            std::vector<Mask*> masks;
            std::vector<Mask*>::iterator masks_iter;
            //int actual_tick, actual_frame;
    };
};
#endif // SPRITE_H
