#include "Enemy.h"



Enemy::Enemy(const LoaderParams* pParams) : SDLGameObject(pParams)
{
}


Enemy::~Enemy()
{
}


void Enemy::draw()
{
	SDLGameObject::draw();
}

void Enemy::update()
{
	setCurrentFrame(int(((SDL_GetTicks() / 100) % 6)));
	setVelocity(1, 1, 0);
	SDLGameObject::update();
}

void Enemy::clean()
{
}