#include "aircraft.h"
#include "sprite.h"
#include "bullet.h"

namespace Advanced2D
{
    AirCraft::AirCraft() : ControllableActor(){
    }

    void AirCraft::doAction(ControllableObject::action_t act, int magnitude){
        current_action = act;
        switch (act){
            case DOWN:
                setY(getY()+4);
                break;
            case UP:
                setY(getY()-4);
                break;
            case LEFT:
                setX(getX()-4);
                break;
            case RIGHT:
                setX(getX()+4);
                break;
            case SHOOT:
                shootBullet();
                break;
        }
        if (getX()<0) setX(0);
        if (getX()>SCREEN_W-getWidth()) setX(SCREEN_W-getWidth());
        if (getY()<0) setY(0);
        if (getY()>SCREEN_H-(getHeight() + 14)) setY(SCREEN_H-(getHeight() + 14));

        /*Animacion dependiendo la tecla que presiono*/
        Sprite *tmp;
        tmp = dynamic_cast<Sprite *>(agraph);
        tmp->update(getCurrentAction());
    }

    void AirCraft::move()
    {
        double w = (double)agraph->getWidth();
        double h = (double)agraph->getHeight();
        double vx = getVelocity().getX();
        double vy = getVelocity().getY();

        if (getX() < 0) {
            setX(0);
            vx = fabs(vx);
        }
        else if (getX() > SCREEN_W-w) {
            setX(SCREEN_W-w);
            vx = fabs(vx) * -1;
        }
        if (getY() < 0) {
            setY(0);
            vy = fabs(vy);
        }
        else if (getY() > SCREEN_H-(h+14)) {
            setY(SCREEN_H-(h+14));
            vy = fabs(vy) * -1;
        }

        setVelocity(vx,vy);
        setX(getPosition().getX() + getVelocity().getX());
        setY(getPosition().getY() + getVelocity().getY());
    }

    void AirCraft::hit(Actor *a, int damage)
    {
        double x1 = getX();
		double y1 = getY();
		double x2 = a->getX();
		double y2 = a->getY();

		double vx1 = getVelocity().getX();
		double vy1 = getVelocity().getY();
		double vx2 = a->getVelocity().getX();
		double vy2 = a->getVelocity().getY();

        if (x1 < x2) {
			vx1 = fabs(vx1) * -1;
			vx2 = fabs(vx1);
		}
		else if (x1 > x2) {
			vx1 = fabs(vx1);
			vx2 = fabs(vx2) * -1;
		}
		if (y1 < y2) {
			vy1 = fabs(vy1) * -1;
			vy2 = fabs(vy2);
		}
		else {
			vy1 = fabs(vy1);
			vy2 = fabs(vy2) * -1;
		}

		setVelocity(vx1,vy1);
		a->setVelocity(vx2,vy2);
    /*    Explosion *exp=new Explosion(game, 10);
        CircleWithZoom *cwz=new CircleWithZoom(exp, 10);
        exp->set_x(a->get_x()-10+rand()%20);
        exp->set_y(a->get_y()-10+rand()%20);
        exp->set_actor_graphic(cwz);
        exp->set_is_detected(false);
        game->actor_manager->add(exp);
    */
    }

    void AirCraft::update(){
        Sprite *tmp;
        tmp = dynamic_cast<Sprite *>(agraph);
        /*Animacion estandar*/
        tmp->update();
        move();
    }


    ControllableObject::action_t AirCraft::getCurrentAction(){
        return current_action;
    }

    void AirCraft::shootBullet(){
        /*Bullet *bull = new Bullet(this->engine, this);
        BITMAP *bull_bmp = load_bitmap("bullet_Selected.pcx", NULL);
        Bitmap *bull_sp = new Bitmap(bull, bull_bmp);
        //bull_sp->add_frame(bull_bmp, bull_bmp->w/2, bull_bmp->h/2, 10);
        int bullet_x = this->get_graph_x() + (this->get_w()/2);
        bull->set_x(bullet_x);
        bull->set_y(this->get_graph_y() - (this->get_h()/2));
        bull->set_actor_graphic(bull_sp); //el sprite va a ser mi actorGraphic
        bull->set_is_detected(true);
        bull->set_team(Engine::ALLY);
        bull->set_collision_method(CollisionManager::PP_COLLISION);
        engine->actor_manager->add(bull);

        destroy_bitmap(bull_bmp);*/
    }
}; //namespace
