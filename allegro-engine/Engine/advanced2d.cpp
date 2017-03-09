#pragma GCC diagnostic ignored "-fpermissive"

#include <allegro.h>
#include <sstream>

#include "advanced2d.h"
#include "actorManager.h"
#include "stageManager.h"
#include "controlManager.h"
#include "audiomanager.h"

namespace Advanced2D
{
    //funcion y variable global que cuentan los ticks del timer para mantener la velocidad el juego.
    void tick_count();
    volatile int tick;

    void tick_count(){
        tick++;
    }
    END_OF_FUNCTION(tick_count);

    /*Constructor de game, inicializa allegro, el timer,
     *protege las variables globales y pone en null a los managers
     */
    Engine::Engine(){
        allegro_init(); //init allegro
        install_keyboard(); //install the keyboard

        p_maximizeProcessor = false;
        p_pause_mode = false;
        gameover = false;

        p_versionMajor = VERSION_MAJOR;
		p_versionMinor = VERSION_MINOR;
		p_revision = REVISION;

        actor_manager=NULL;
        stage_manager=NULL;
        control_manager=NULL;
        collision_manager=NULL;

        install_timer();//install the timer
        LOCK_VARIABLE(tick); // protect tick variable
        LOCK_FUNCTION(tick_count); // protect function
        install_int(&tick_count, 14); // install interrupts
    }

    /*Desctructor de la clase*/
    Engine::~Engine(){
        if(audio_manager)
        {
            audio_manager->stopAll();
            delete audio_manager;
        }
        if(collision_manager) delete collision_manager;
        if(actor_manager) delete actor_manager;
        if(stage_manager) delete stage_manager;
        if(control_manager) delete control_manager;
    }

    /*Inicializa la clase game, inicializa el modo grafico y crea los managers*/
    int Engine::init(int width, int height, int colordepth, int fullscreen)
	{
        //register_png_file_type();
        set_color_depth(colordepth);
        if (set_gfx_mode(fullscreen,width, height, 0,0)<0){
            shutdown();
            return 0;
        }

        create_actormanager();
        create_stagemanager();
        create_controlmanager();
        create_collisionmanager();
        create_audiomanager();
        if(!audio_manager->init()) return 0;

        if(!game_init()) return 0;
        start();

        return 1;
    }

    /*Destruye los managers y cierra allegro*/
    void Engine::shutdown(/*std::string message="Gracias por jugar"*/){
        gameover = true;
    }

    /*Ciclo del juego, actualiza los managers y realiza el control de velocidad del juego*/
    void Engine::update(){
        if (p_actual_tick<=tick){
            game_update();
            p_actual_tick++;
        }

        if ((p_actual_tick>=tick) || (p_frame_skip>p_max_frame_skip)){
            game_render();
            audio_manager->update();
            if (p_frame_skip>p_max_frame_skip) p_actual_tick=tick;
            p_graphic_tick++;
            p_frame_skip=0;
        }
        else{
            p_frame_skip++;
        }

        //Imprime en pantalla la cantidad de FPS
        if (tick-p_old_tick >=70){ // se cumplió un segundo
            rectfill(screen,0,0,200,14,0); // borrar el antigüo marcador
            textprintf_ex(screen, font, 0,0, makecol(0, 0, 255), -1, "fps: %u frameskip:%u", p_graphic_tick, p_frame_skip);
            p_graphic_tick=0;
            p_old_tick=tick;
        }
    }

    void Engine::close()
	{
		try {
			game_end();
			set_gfx_mode(GFX_TEXT,0,0,0,0);
            std::cout << p_apptitle << std::endl;
            //std::cout << message << std::endl;
            allegro_exit();
		}
		catch (...) { }
	}

    /*Crea un ActorManager*/
    void Engine::create_actormanager(){
        actor_manager = new ActorManager(this);
    }

    /*Crea un StageManager*/
    void Engine::create_stagemanager(){
        stage_manager = new StageManager(this, p_screen_width, p_screen_height);
    }

    /*Crea un ControlManager*/
    void Engine::create_controlmanager(){
        control_manager = new ControlManager();
    }

    void Engine::create_collisionmanager(){
        collision_manager = new CollisionManager();
    }

    void Engine::create_audiomanager(){
        audio_manager = new AudioManager();
    }

    /*Inicia el juego*/
    void Engine::start(){
        p_actual_tick=tick; // se alinea con el timer real
        p_old_tick=tick;
        p_max_frame_skip=15; // estable el salto de cuadro por defecto
    }

    /*ejecuta el juego mientras no se presione la tecla ESC*/
    /*void Game::main(){
        while (!key[KEY_ESC]);
    }*/ //Esto lo hace game_update

    /*Setea el maximo de frame skip*/
    void Engine::set_max_frame_skip(int max_fs){
        p_max_frame_skip=max_fs;
    }

    //Muestra un mensaje en pantalla
    void Engine::message(std::string message, std::string title)
	{
        EasyMessage msg(EasyCentered, message.c_str(), title.c_str());
	}

    //Muestra un mensaje en pantalla y cierra el programa
	void Engine::fatalerror(std::string msg, std::string title)
	{
		message(msg,title);
		shutdown();
	}

    //devuelve la version del engine
    std::string Engine::getVersionText()
	{
		std::ostringstream s;
		s << "Advanced2D Engine v" << p_versionMajor << "." << p_versionMinor << "." << p_revision;
		return s.str();
	}
}//namespace
