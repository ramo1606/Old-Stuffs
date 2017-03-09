#include "stageManager.h"

namespace Advanced2D
{
    StageManager::StageManager(Engine *e, int w, int h){
        engine=e;
        width=w;
        height=h;
        buffer=create_bitmap(SCREEN_W, SCREEN_H);
    }

    StageManager::~StageManager(){
        destroy_bitmap(buffer);
    }

    int StageManager::w(){
        return width;
    }

    int StageManager::h(){
        return height;
    }

    void StageManager::update(){
        draw();
    }

    void StageManager::draw(){
        Actor *tmp;
        engine->actor_manager->rewind();
        clear(buffer);
        while ((tmp=engine->actor_manager->next())!=NULL){
            tmp->draw(buffer);
        }
        // 14 pixels abajo para el marcador de fps
        blit(buffer, screen, 0,0,0,14,SCREEN_W, SCREEN_H);
    }
}; //namespace
