#include "actorManager.h"

namespace Advanced2D
{
    ActorManager::ActorManager(Engine *e){
        engine=e;
    }

    ActorManager::~ActorManager(){
        for (actors_iter=actors.begin(); actors_iter!=actors.end(); actors_iter++){
            delete (*actors_iter);
        }
    }

    void ActorManager::add(Actor *a){
        to_create.push_back(a);
    }

    void ActorManager::add_all_to_create(){

        if (to_create.size()==0) return;
        list<Actor *>::iterator tmp_iter;
        for (tmp_iter=to_create.begin(); tmp_iter!=to_create.end(); tmp_iter++)
        {
            actors.push_back(*tmp_iter);
            (*tmp_iter)->init();
        }
        to_create.clear();
    }

    void ActorManager::del(Actor *a){
        to_del.push_back(a);
    }

    void ActorManager::del_all_to_del(){

        if (to_del.size()==0) return;
        list<Actor*>::iterator tmp_iter;
        list<Actor*>::iterator tmp_actors_iter;

        for (tmp_iter=to_del.begin(); tmp_iter!=to_del.end(); tmp_iter++)
        {
            tmp_actors_iter=find(actors.begin(), actors.end(), *tmp_iter);
            if (tmp_actors_iter!=actors.end())
            {
                actors.erase(tmp_actors_iter);
                delete (*tmp_iter);
            }
        }
        to_del.clear();
    }

    void ActorManager::rewind(){
        actors_iter=actors.begin();
    }

    Actor *ActorManager::next(){
        Actor *tmp_a;
        tmp_a=*actors_iter;
        if (actors_iter==actors.end())
            return NULL;
        actors_iter++;
        return tmp_a;
    }

    Actor *ActorManager::current(){
        if (actors_iter==actors.end())
            return NULL;
        else
            return *actors_iter;
    }

    int ActorManager::num_actors(){
        return actors.size();
    }

    void ActorManager::update(){
        std::list<Actor*>::iterator tmp_iter;

        add_all_to_create(); //llamada para agregar todos los actores en espera
        for (tmp_iter=actors.begin(); tmp_iter!=actors.end(); tmp_iter++)
            (*tmp_iter)->update();
        del_all_to_del(); //llamada para eliminar todos los actores en espera
    }

    list<Actor*>::iterator ActorManager::get_begin_iterator(){
        return actors.begin();
    }

    list<Actor*>::iterator ActorManager::get_end_iterator(){
        return actors.end();
    }
}; //namespace
