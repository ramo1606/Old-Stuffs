#pragma once
#ifndef __Engine__
#define __Engine__

#include <SDL.h>
#include <SDL_image.h>
#include <stdio.h>
#include <string>
#include <iostream>
#include <vector>
#include "TextureManager.h"
#include "GameObject.h"
#include "Player.h"
#include "Enemy.h"
#include "InputHandler.h"
#include "GameStateMachine.h"

class Engine
{
public:

	static Engine* Instance();

	bool init(const char* title, int xpos, int ypos, int width, int height, bool fullscreen);
	void render();
	void update();
	void handleEvents();
	void clean();

	SDL_Renderer* getRenderer() const { return m_pRenderer; }

	// a function to access the private running variable
	bool running() { return m_bRunning; }

	void quit() { m_bRunning = false; }

	GameStateMachine* getStateMachine() { return m_pGameStateMachine; }

private:
	Engine();
	~Engine();

	static Engine* s_pInstance;
	SDL_Window* m_pWindow;
	SDL_Renderer* m_pRenderer;

	std::vector<GameObject*> m_gameObjects;
	GameStateMachine* m_pGameStateMachine;
	bool m_bRunning;
};
typedef Engine TheEngine;

#endif /* defined(__Engine__) */
