#pragma once

#ifndef __GameObject__
#define __GameObject__

#include "LoaderParams.h"

class GameObject
{
public:
	virtual ~GameObject() {}

	virtual void draw() = 0;
	virtual void update() = 0;
	virtual void clean() = 0;

protected:
	GameObject(const LoaderParams* pParams){}
};

#endif