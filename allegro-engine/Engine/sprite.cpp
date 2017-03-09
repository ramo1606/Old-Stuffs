#include "sprite.h"

namespace Advanced2D
{
    Sprite::Sprite() : ActorGraphic(){
        curFrame = 0;
        totalFrames = 1;
        animDir = 1;
        animColumns = 1;
        frameCount = 0;
        frameDelay = 10;
        animStartx = 0;
        animStarty = 0;
        faceAngle = 0;
        moveAngle = 0;
        width = 1;
        height = 1;
        scaling = 1.;
        rotation = 0;
    }

    Sprite::~Sprite(){
        for (masks_iter=masks.begin(); masks_iter!=masks.end(); masks_iter++){
            delete (*masks_iter);
        }
    }

    void Sprite::init()
    {
        curFrame = 0;
        frameCount = 0;
    }

    void Sprite::update(ControllableObject::action_t action){
        switch (action){
            case DOWN:
                //curFrame = 0;
                break;
            case UP:
                //curFrame = 2;
                break;
            case LEFT:
                //curFrame = 1;
                break;
            case RIGHT:
                //curFrame = 1;
                break;
        }
    }

    void Sprite::update(){
        if(++frameCount > frameDelay)
        {
            frameCount = 0;
            curFrame += animDir;
            if(curFrame < 0)
            {
                curFrame = totalFrames - 1;
            }
            if(curFrame > totalFrames - 1)
            {
                curFrame = 0;
            }
        }
    }

    void Sprite::draw(BITMAP *bmp, int x, int y){
        if(imageLoaded)
        {
            drawFrame(bmp, x, y);
        }
    }

    void Sprite::drawFrame(BITMAP *bmp, int x, int y)
    {
        int framex = animStartx + (curFrame % animColumns) * width;
        int framey = animStarty + (curFrame / animColumns) * height;

        masked_blit(p_bmp, bmp, framex, framey, x, y, getWidth(), getHeight());
    }


    BITMAP *Sprite::grabframe(BITMAP *source, int width, int height, int startx, int starty, int columns, int frame)
    {
        BITMAP *temp = create_bitmap(width,height);

        int x = startx + (frame % columns) * width;
        int y = starty + (frame / columns) * height;

        blit(source,temp,x,y,0,0,width,height);

        return temp;
    }

    bool Sprite::loadMasks(void)
    {
        bool result = false;
        if(imageLoaded)
        {
            for(int init = 0; init < totalFrames; ++init)
            {
                BITMAP *temp = grabframe(p_bmp, getWidth(), getHeight(), animStartx, animStarty, animColumns, curFrame);
                Mask *mask = new Mask;
                mask->create(temp);
                masks.push_back(mask);
                delete temp;
            }
            result = true;
        }
        return result;
    }

    int Sprite::getWidth(){
        return width;
    }

    int Sprite::getHeight(){
        return height;
    }

    void Sprite::setWidth(int value)
    {
        this->width = value;
    }

    void Sprite::setHeight(int value)
    {
        this->height = value;
    }

    void Sprite::setSize(int width, int height)
    {
        this->width = width;
        this->height = height;
    }

    int Sprite::getColumns()
    {
        return animColumns;
    }
    void Sprite::setColumns(int value)
    {
        animColumns = value;
    }

    Mask *Sprite::getMask(){
        return masks[curFrame];
    }

    int Sprite::getFrameDelay()
    {
        return frameDelay;
    }

    void Sprite::setFrameDelay(int value)
    {
        frameDelay = value;
    }

    int Sprite::getCurrentFrame()
    {
        return curFrame;
    }

    void Sprite::setCurrentFrame(int value)
    {
        curFrame = value;
    }

    int Sprite::getTotalFrames()
    {
        return totalFrames;
    }

    void Sprite::setTotalFrames(int value)
    {
        totalFrames = value;
    }

    int Sprite::getAnimationDirection()
    {
        return animDir;
    }

    void Sprite::setAnimationDirection(int value)
    {
        animDir = value;
    }

    double Sprite::getRotation()
    {
        return rotation;
    }

    void Sprite::setRotation(double value)
    {
        rotation = value;
    }

    double Sprite::getScale()
    {
        return scaling;
    }

    void Sprite::setScale(double value)
    {
        scaling = value;
    }
}; //namespace
