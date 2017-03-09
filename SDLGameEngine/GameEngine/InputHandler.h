#pragma once
#ifndef __InputHandler__
#define __InputHandler__

#include <vector>
#include <iostream>
#include "SDL.h"

enum mouse_buttons
{
	LEFT = 0,
	MIDDLE = 1,
	RIGHT = 2
};

class InputHandler
{
public:
	static InputHandler* Instance();
	void update();
	void clean();

	void initialiseJoysticks();
	bool joysticksInitialised();

	bool getButtonState(int joy, int buttonNumber);
	bool getMouseButtonState(int buttonNumber);
	Vector* getMousePosition();
	void reset();
	bool isKeyDown(SDL_Scancode key);

private:
	InputHandler();
	virtual ~InputHandler() {}

	// private functions to handle different event types

	// handle keyboard events
	void onKeyDown();
	void onKeyUp();

	// handle mouse events
	void onMouseMove(SDL_Event& event);
	void onMouseButtonDown(SDL_Event& event);
	void onMouseButtonUp(SDL_Event& event);

	// handle joysticks events
	void onJoystickButtonDown(SDL_Event& event);
	void onJoystickButtonUp(SDL_Event& event);

	static InputHandler* s_pInstance;

	std::vector<SDL_Joystick*> m_joysticks;
	bool m_bJoysticksInitialised;

	std::vector<std::vector<bool>> m_buttonStates;
	std::vector<bool> m_mouseButtonStates;
	Vector* m_mousePosition;
	const Uint8* m_keystates;
};
typedef InputHandler TheInputHandler;

#endif