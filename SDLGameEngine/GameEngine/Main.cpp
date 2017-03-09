#include "Engine.h"

#include <Windows.h>
#include <SDL.h>

Engine* e_engine = NULL;

const int FPS = 60;
const int DELAY_TIME = 1000.0f / FPS;

int main(int argc, char* argv[])
{
	AllocConsole();
	freopen("CON", "w", stdout);

	Uint32 frameStart, frameTime;

	std::cout << "Engine init attempt...\n";
	if (TheEngine::Instance()->init("Chapter 1", 100, 100, 640, 480,
		false))
	{
		std::cout << "Engine init success!\n";
		while (TheEngine::Instance()->running())
		{
			frameStart = SDL_GetTicks();

			TheEngine::Instance()->handleEvents();
			TheEngine::Instance()->update();
			TheEngine::Instance()->render();
			
			frameTime = SDL_GetTicks() - frameStart;
			if (frameTime < DELAY_TIME)
			{
				SDL_Delay((int)(DELAY_TIME - frameTime));
			}
		}
	}
	else
	{
		std::cout << "Engine init failure - " << SDL_GetError() << "\n";
		return -1;
	}

	std::cout << "Engine closing...\n";
	TheEngine::Instance()->clean();

	return 0;
}