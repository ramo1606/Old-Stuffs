#include "MenuState.h"
#include "TextureManager.h"
#include "Engine.h"
#include "MenuButton.h"
#include "PlayState.h"

const std::string MenuState::s_menuID = "MENU";

MenuState::MenuState()
{
}


MenuState::~MenuState()
{
}

void MenuState::update()
{
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

void MenuState::render()
{
	if(!m_gameObjects.empty())
	{
		for (int i = 0; i < m_gameObjects.size(); i++)
		{
			m_gameObjects[i]->draw();
		}
	}
}

bool MenuState::onEnter()
{
	if (!TheTextureManager::Instance()->load("Resources/button.png",
		"playbutton", TheEngine::Instance()->getRenderer()))
	{
		return false;
	}
	if (!TheTextureManager::Instance()->load("Resources/exit.png",
		"exitbutton", TheEngine::Instance()->getRenderer()))
	{
		return false;
	}
	GameObject* button1 = new MenuButton(new LoaderParams(100, 100,
		400, 100, "playbutton"), s_menuToPlay);
	GameObject* button2 = new MenuButton(new LoaderParams(100, 300,
		400, 100, "exitbutton"), s_exitFromMenu);
	m_gameObjects.push_back(button1);
	m_gameObjects.push_back(button2);
	std::cout << "entering MenuState\n";
	return true;
}

bool MenuState::onExit()
{
	if(!m_gameObjects.empty())
	{
		for (int i = 0; i < m_gameObjects.size(); i++)
		{
			m_gameObjects[i]->clean();
			delete m_gameObjects[i];
		}
	}
	m_gameObjects.clear();
	//TheTextureManager::Instance()->clearFromTextureMap("playbutton");
	//TheTextureManager::Instance()->clearFromTextureMap("exitbutton");
	std::cout << "exiting MenuState\n";
	return true;
}

void MenuState::s_menuToPlay()
{
	TheEngine::Instance()->getStateMachine()->changeState(new PlayState());
}

void MenuState::s_exitFromMenu()
{
	TheEngine::Instance()->quit();
}