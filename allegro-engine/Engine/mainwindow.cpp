#include "mainwindow.h"

//Advanced2D::Engine *g_engine;
//bool gameover;

int mainwindow(void){
    //TestFrameWork game;
    g_engine = new Advanced2D::Engine;
    srand(time(NULL));
    if(!game_preload())
    {
        EasyMessage msg(EasyCentered, "Error in game preload!!", "Error", "OK");
        return 1;
    }

    if(!g_engine->init(g_engine->getScreenWidth(), g_engine->getScreenHeight(), g_engine->getColorDepth(),
    g_engine->getFullscreen()))
    {
        EasyMessage msg(EasyCentered, "Error initializing the engine!!", "Error", "OK");
        return 1;
    }

    while(!gameover)
    {
        g_engine->update();
    }

    g_engine->close();
    delete g_engine;

    return 0;
}
