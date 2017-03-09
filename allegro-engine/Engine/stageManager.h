#ifndef STAGEMANAGER_H
#define STAGEMANAGER_H

#include <allegro.h>
#include "advanced2d.h"
#include "actorManager.h"

namespace Advanced2D
{
    class Engine;

    /*clase que maneja la escena, donde todos actores se dibujan*/
    class StageManager{

        public:
            /*Constructor*/
            StageManager(Engine *e, int w, int h);
            /*Destructor*/
            ~StageManager();
            /*width*/
            int w();
            /*height*/
            int h();
            /*Actualiza la escena*/
            void update();
            /*Dibuja la escena*/
            void draw();
        protected:
            Engine *engine; //referencia al juego
            BITMAP *buffer;
            int width, height;
    };
}; //namespace
#endif
