#pragma once
#ifndef __Enemy__
#define __Enemy__

#include "SDLGameObject.h"

class Enemy : public SDLGameObject
{
public:
	Enemy(const LoaderParams* pParams);
	virtual ~Enemy();

	virtual void draw();
	virtual void update();
	virtual void clean();
};

#endif