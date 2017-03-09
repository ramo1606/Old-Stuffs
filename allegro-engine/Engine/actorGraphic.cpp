#include "actorGraphic.h"
#include "actor.h"

namespace Advanced2D
{
    ActorGraphic::ActorGraphic(){
        imageLoaded = false;
        p_bmp = NULL;
    }

    ActorGraphic::~ActorGraphic(){
        if(p_bmp != NULL)
        {
            destroy_bitmap(p_bmp);
        }
    }

    void ActorGraphic::update(){
    }

    void ActorGraphic::init(){
    }

    void ActorGraphic::draw(BITMAP *bmp, int x, int y){
    }

    int ActorGraphic::getWidth(){
        if(imageLoaded && p_bmp != NULL)
        {
            return p_bmp->w;
        }else
        {
            return -1;
        }
    }

    int ActorGraphic::getHeight(){
        if(imageLoaded && p_bmp != NULL)
        {
            return p_bmp->h;
        }else
        {
            return -1;
        }
    }

    Mask* ActorGraphic::getMask(){
    }

    bool ActorGraphic::loadImage(std::string filename)
    {
        if(imageLoaded && p_bmp != NULL)
        {
            delete p_bmp;
        }
        char *name = (char *)filename.c_str();
        p_bmp = load_bitmap(name, NULL);
        if(p_bmp != NULL)
        {
            imageLoaded = true;
        }else
        {
            imageLoaded =false;
        }
        return imageLoaded;
    }

    bool ActorGraphic::getImageLoaded()
    {
        return imageLoaded;
    }

    BITMAP *ActorGraphic::getBitMap()
    {
        return p_bmp;
    }

    bool *ActorGraphic::setBitMap(BITMAP *image)
    {
        if(p_bmp != NULL)
        {
            destroy_bitmap(p_bmp);
        }
        p_bmp = image;
    }

}; //namespace
