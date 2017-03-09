#include "PlayState.h"
#include "TextureManager.h"
#include "Engine.h"
#include "PauseState.h"

const std::string PlayState::s_playID = "PLAY";

PlayState::PlayState()
{
}


PlayState::~PlayState()
{
}


void PlayState::update()
{
	if (TheInputHandler::Instance()->isKeyDown(SDL_SCANCODE_ESCAPE))
	{
		TheEngine::Instance()->getStateMachine()->pushState(new PauseState());
	}

	if(!m_gameObjects.empty())
	{
		for (int i = 0; i < m_gameObjects.size(); i++)
		{
			if (m_gameObjects[i] != 0)
			{
				m_gameObjects[i]->update();
			}
		}
	}
}

void PlayState::render()
{
	for (int i = 0; i < m_gameObjects.size(); i++)
	{
		m_gameObjects[i]->draw();
	}
}

bool PlayState::onEnter()
{
	if (!TheTextureManager::Instance()->load("Resources/helicopter.png", 
		"helicopter", TheEngine::Instance()->getRenderer()))
	{
		return false;
	}

	GameObject* player = new Player(new LoaderParams(100, 100, 128, 55, "helicopter"));
	m_gameObjects.push_back(player);

	std::cout << "entering PlayState\n";
	return true;
}

bool PlayState::onExit()
{
	for (int i = 0; i < m_gameObjects.size(); i++)
	{
		m_gameObjects[i]->clean();
		delete m_gameObjects[i];
	}

	m_gameObjects.clear();
	TheTextureManager::Instance()->clearFromTextureMap("helicopter");
	
	std::cout << "exiting PlayState\n";
	return true;
}