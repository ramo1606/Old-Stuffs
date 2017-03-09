#include "actor.h"

namespace Advanced2D
{
    Actor::Actor(){
        agraph=NULL;
        setPosition(0., 0.);
        setVelocity(0., 0.);
        state = 0;
        direction = 1;
        power = 0;
        alive = true;
    }

    Actor::~Actor(){
        if (agraph) delete agraph;
    }

    void Actor::draw(BITMAP *bmp){
        if(agraph != NULL)
        {
            agraph->draw(bmp, (int)getX(), (int)getY());
        }
    }

    void Actor::update(){
        if(agraph != NULL)
        {
            agraph->update();
        }
        move();
    }

    void Actor::init(){
        if(agraph != NULL)
        {
            agraph->init();
        }
    }

    void Actor::move(){
    }

    void Actor::setX(double pos_x){
        position.setX(pos_x);
    }

    void Actor::setY(double pos_y){
        position.setY(pos_y);
    }

    void Actor::setPosition(Vector pos)
    {
        position = pos;
    }

    void Actor::setPosition(double x, double y)
    {
        position.Set(x, y, 0);
    }

    Vector Actor::getPosition()
    {
        return this->position;
    }

    Vector Actor::getVelocity()
    {
        return velocity;
    }

    void Actor::setVelocity(Vector v)
    {
        velocity = v;
    }
    void Actor::setVelocity(double x, double y)
    {
        velocity.setX(x);
        velocity.setY(y);
    }

    void Actor::setDirection(int dir)
    {
        direction = dir;
    }

    int Actor::getDirection()
    {
        return direction;
    }

    void Actor::setActorGraphic(ActorGraphic *ag){
        agraph=ag;
    }

    double Actor::getX(){
        return position.getX();
    }

    double Actor::getY(){
        return position.getY();
    }

    int Actor::getWidth(){
        return agraph->getWidth();
    }

    int Actor::getHeight(){
        return agraph->getHeight();
    }

    Mask *Actor::getGraphMask(){
        return agraph->getMask();
    }

    void Actor::setIsDetected(bool tf){
        isDetectable = tf;
    }

    bool Actor::getIsDetected(){
        return isDetectable;
    }

    void Actor::setAlive(bool live)
    {
        alive = live;
    }

    bool Actor::isAlive()
    {
        return alive;
    }

    void Actor::setPower(int pow){
        power = pow;
    }

    int Actor::getPower(){
        return power;
    }

    void Actor::setCollisionMethod(CollisionManager::collision_method_t cm){
        collisionMethod = cm;
    }

    CollisionManager::collision_method_t Actor::getCollisionMethod(){
        return collisionMethod;
    }

    void Actor::hit(Actor *who, int damage){

    }

    void Actor::setTeam(Engine::team_t tm){
        team = tm;
    }

    Engine::team_t Actor::getTeam(){
        return team;
    }
}; //namespace
