#pragma once
#ifndef __MenuState__
#define __MenuState__

#include <iostream> 
#include <vector>
#include "GameObject.h"
#include "GameState.h"

class MenuState : public GameState
{
public:
	MenuState();
	virtual ~MenuState();

	virtual void update();
	virtual void render();
	virtual bool onEnter();
	virtual bool onExit();
	virtual std::string getStateID() const { return s_menuID; }

private:
	static const std::string s_menuID;

	std::vector<GameObject*> m_gameObjects;

	// call back functions for menu items
	static void s_menuToPlay();
	static void s_exitFromMenu();
};
#endif
