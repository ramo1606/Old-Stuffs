#ifndef ACTORMANAGER_H
#define ACTORMANAGER_H

#include <algorithm>
#include <list>
#include "actor.h"

namespace Advanced2D
{
    class Actor;
    class Engine;

    /*La clase ActorManager se encarga de mantener una lista de actores
    */
    class ActorManager{
        public:
            /*Constructor*/
            ActorManager(Engine *e);
            /*Destructor*/
            ~ActorManager();
            /*Agrega un actor a la lista*/
            void add(Actor *a);
            /*Elimina un actor de la lista*/
            void del(Actor *a);
            /*Apunto al primer actor de la lista*/
            void rewind();
            /*Devuelvo el siguiente actor*/
            Actor *next();
            /*Devuelvo el actor actual*/
            Actor *current();
            /*Actualizo el estado de todos los actores*/
            void update();
            /*Devuelve el numero de actores en la lista*/
            int num_actors();
            /*Retorna el iterador inicial de la lista*/
            std::list<Actor*>::iterator get_begin_iterator();
            /*Retorna el iterador final de la lista*/
            std::list<Actor*>::iterator get_end_iterator();

        protected:
            Engine *engine;
            std::list<Actor*> actors; //lista de actores
            std::list<Actor*>::iterator actors_iter; //iterador de la lista
            std::list<Actor*> to_del; //listas de actores a eliminar
            std::list<Actor*> to_create; //lista de actores a crear

            void add_all_to_create();
            void del_all_to_del();
    };
};
#endif
