#include "Engine.h"
#include "MenuState.h"
#include "PlayState.h"


Engine* Engine::s_pInstance = 0;

Engine::Engine()
{
}

Engine::~Engine()
{
}

Engine* Engine::Instance()
{
	if (s_pInstance == NULL)
	{
		s_pInstance = new Engine();
		return s_pInstance;
	}
	return s_pInstance;
}

bool Engine::init(const char* title, int xpos, int ypos, int width, int height, bool fullscreen)
{
	int flags = 0;
	if (fullscreen)
	{
		flags = SDL_WINDOW_FULLSCREEN;
	}

	if(SDL_Init(SDL_INIT_EVERYTHING) == 0)
	{
		std::cout << "SDL_Init success\n";

		TheInputHandler::Instance()->initialiseJoysticks(); //init input 
		m_pWindow = SDL_CreateWindow(title, xpos, ypos, width, height, flags);
		
		if (m_pWindow != 0) // window init success
		{
			std::cout << "window creation success\n";
			m_pRenderer = SDL_CreateRenderer(m_pWindow, -1, 0);
			if (m_pRenderer != NULL) // renderer init success
			{
				std::cout << "renderer creation success\n";
				SDL_SetRenderDrawColor(m_pRenderer, 255, 255, 255, 255);
			}
			else
			{
				std::cout << "renderer init fail\n";
				return false; // renderer init fail
			}

			/*if (!TheTextureManager::Instance()->load("Resources/animate-alpha.png",
				"animate", m_pRenderer))
			{
				std::cout << "Texture init fail\n";
				return false; //texture init fail
			}*/
		}
		else
		{
			std::cout << "window init fail\n";
			return false; // window init fail
		}
	}
	else
	{
		std::cout << "SDL init fail\n";
		return false; // SDL init fail
	}
	std::cout << "init success\n";

	//Create the GameStateMachine
	m_pGameStateMachine = new GameStateMachine();
	m_pGameStateMachine->changeState(new MenuState());

	//Create the GameObjects
	//m_gameObjects.push_back(new Player(new LoaderParams(100, 100, 128, 82, "animate")));
	//m_gameObjects.push_back(new Enemy(new LoaderParams(300, 300, 128, 82, "animate")));

	m_bRunning = true; // everything inited successfully, start the main loop
	return true;
}

void Engine::render()
{
	SDL_RenderClear(m_pRenderer); // clear the renderer to the draw color

	m_pGameStateMachine->render();

	/*for (std::vector<GameObject*>::size_type i = 0; i !=
		m_gameObjects.size(); i++)
	{
		m_gameObjects[i]->draw();
	}*/

	SDL_RenderPresent(m_pRenderer); // draw to the screen
}

void Engine::update()
{
	m_pGameStateMachine->update();
}

void Engine::handleEvents()
{
	TheInputHandler::Instance()->update();

	if (TheInputHandler::Instance()->isKeyDown(SDL_SCANCODE_RETURN))
	{
		m_pGameStateMachine->changeState(new PlayState());
	}
}

void Engine::clean()
{
	std::cout << "cleaning game\n";
	SDL_DestroyWindow(m_pWindow);
	SDL_DestroyRenderer(m_pRenderer);
	TheInputHandler::Instance()->clean();
	m_pGameStateMachine->clean();
	SDL_Quit();
}