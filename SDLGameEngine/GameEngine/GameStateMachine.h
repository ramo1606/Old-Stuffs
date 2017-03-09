#pragma once
#ifndef __GameStateMachine__
#define __GameStateMachine__

#include <vector>
#include "GameState.h"

class GameStateMachine
{
public:
	GameStateMachine();
	virtual ~GameStateMachine();

	void update();
	void render();
	void clean();

	void pushState(GameState* pState);
	void changeState(GameState* pState);
	void popState();

private:
	std::vector<GameState*> m_gameStates;
};

#endif