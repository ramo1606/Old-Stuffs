#include "Player.h"



Player::Player(const LoaderParams* pParams) : SDLGameObject(pParams)
{
}

Player::~Player()
{
}


void Player::draw()
{
	SDLGameObject::draw();
}

void Player::update()
{
	setCurrentFrame(int(((SDL_GetTicks() / 100) % 5)));

	handleInput();

	SDLGameObject::update();
}

void Player::clean()
{
}

void Player::handleInput()
{
	Vector* target = TheInputHandler::Instance()->getMousePosition();
	setVelocity(*target - getPosition());
	setVelocity(getVelocity() / 50);
}