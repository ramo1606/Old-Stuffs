#ifndef GAME_H
#define GAME_H

#include <allegro.h>
#include <string>
#include <iostream>
#include "lib/inc/fmod.h"
#include "easymessage.h"

namespace Advanced2D
{
    class Actor;
}

#define VERSION_MAJOR 1
#define VERSION_MINOR 0
#define REVISION 0

//external variables and functions
extern bool gameover;
extern bool game_preload();
extern bool game_init();
extern void game_update();
extern void game_render();
extern void game_end();

extern void game_collision(Advanced2D::Actor*, Advanced2D::Actor*);

/*La calse game contiene toda la indormacion del juego y
 *delega tareas a los managers.
 */
 namespace Advanced2D
{
    class ActorManager;
    class StageManager;
    class CollisionManager;
    class ControlManager;
    class AudioManager;

    class Engine{
        public:
            typedef enum
            {
                ALLY,
                ENEMY
            }team_t;

            /*constructor*/
            Engine();

            /*Destructor*/
            virtual ~Engine();

            /*Inicializador de la clase, inicia el modo grafico, crea los manejadores e inicia el juego*/
            virtual int init(int width, int height, int colordepth, int fullscreen);
            void close();
            void update();
            void message(std::string message, std::string title = "ADVANCED 2D");
            void fatalerror(std::string msg, std::string title = "FATAL ERROR");
            void shutdown();

            //accessor/mutator functions expose the private variables
            bool isPaused() { return p_pause_mode; }
            void setPaused(bool value) { p_pause_mode = value; }
            std::string getAppTitle() { return p_apptitle; }
            void setAppTitle(std::string value) { p_apptitle = value; }
            int getVersionMajor() { return p_versionMajor; }
            int getVersionMinor() { return p_versionMinor; }
            int getRevision() { return p_revision; }
            std::string getVersionText();
            int getScreenWidth() { return p_screen_width; }
            void setScreenWidth(int value) { p_screen_width = value; }
            int getScreenHeight() { return p_screen_height; }
            void setScreenHeight(int value) { p_screen_height = value; }
            int getColorDepth() { return p_color_depth; }
            void setColorDepth(int value) { p_color_depth = value; }
            int getFullscreen() { return p_full_screen; }
            void setFullscreen(int value) { p_full_screen = value; }
            bool getMaximizeProcessor() { return p_maximizeProcessor; }
            void setMaximizeProcessor(bool value) { p_maximizeProcessor = value; }

            AudioManager *audio_manager;    //Manejador de audio
            ActorManager *actor_manager; //Manejador de actores
            StageManager *stage_manager; //manejador de escena
            ControlManager *control_manager; //manejador de controles
            CollisionManager *collision_manager; //manejador de colisiones

        private:
            int p_versionMajor, p_versionMinor, p_revision;
            int p_graphic_tick, p_old_tick; //variables para la velicidad del juego
            int p_actual_tick, p_frame_skip, p_max_frame_skip;

            std::string p_apptitle;
            int p_full_screen;
            int p_screen_width;
            int p_screen_height;
            int p_color_depth;
            bool p_pause_mode;
            bool p_maximizeProcessor;

            /*Incia el juego*/
            void start();
            /*Libera toda la memoria y cierra allegro*/
            //void shutdown(std::string message="Gracias por jugar");
            /*Instancia un manejador de actores*/
            virtual void create_actormanager();
            /*instancia un manejador de escena*/
            virtual void create_stagemanager();
            /*Instancia un manejador de controles*/
            virtual void create_controlmanager();
            /*Instancia un manejador de colisiones*/
            virtual void create_collisionmanager();
            /*Instancia un manejador de audio*/
            virtual void create_audiomanager();
            /*Setea el maximo de frames skip*/
            void set_max_frame_skip(int max_fs);
    }; //class
};//namespace

//define the global engine object (visible everywhere!)
extern Advanced2D::Engine *g_engine;
#endif
