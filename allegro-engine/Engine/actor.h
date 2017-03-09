#ifndef ACTOR_H
#define ACTOR_H

#include <allegro.h>
#include "advanced2d.h"
#include "collisionManager.h"
#include "vector.h"
#include "actorGraphic.h"

namespace Advanced2D
{
    /*La clase actor representa a todos los objetos que se mueven en pantalla
    */
    class Actor{
        public:
            /*Constructor*/
            Actor();
            /*Destructor*/
            virtual ~Actor();

            /*Dibuja al actor en pantalla*/
            virtual void draw(BITMAP *bmp);

            /*Actualiza al actor*/
            virtual void update();
            /*Realiza la logica del actor*/
            virtual void move();
            /**/
            virtual void init();
            /*Retorna el ancho grafico del actor*/
            virtual int getWidth();
            /*retorna la altura grafica del actor*/
            virtual int getHeight();

            virtual void hit(Actor *who, int damage);

            /*Seters y geters de la posicion del actor*/
            double getX();
            double getY();
            void setX(double pos_x);
            void setY(double pos_y);
            void setPosition(Vector pos);
            void setPosition(double x, double y);
            Vector getPosition();

            //movement velocity
            Vector getVelocity();
            void setVelocity(Vector v);
            void setVelocity(double x, double y);

            /*Setea is_detected*/
            void setAlive(bool live);
            bool isAlive();
            void setDirection(int dir);
            int getDirection();
            void setIsDetected(bool tf);
            bool getIsDetected();
            void setPower(int pow);
            int getPower();
            void setCollisionMethod(CollisionManager::collision_method_t cm);
            CollisionManager::collision_method_t getCollisionMethod();
            void setTeam(Engine::team_t tm);
            Engine::team_t getTeam();

            /*setea el actor grafico correspondiente a este actor*/
            void setActorGraphic(ActorGraphic *ag);

            /*Retorna la mascara de su representacion grafica*/
            Mask *getGraphMask();

            ActorGraphic *agraph; //referencia al grafico de este actor

        private:
            Vector position; //posicion del actor
            Vector velocity;
            bool isDetectable; //indica si el actor es detectable o no
            bool alive; //indica si el actor esta vivo
            int state;
            int direction;
            int power; //Dano que produce nuestro actor
            CollisionManager::collision_method_t collisionMethod; //tipo de colision que usamos
            Advanced2D::Engine::team_t team; //Equipo al que pertenece nuestro actor
    };
}; //namespace
#endif
