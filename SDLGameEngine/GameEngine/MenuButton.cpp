#include "MenuButton.h"



MenuButton::MenuButton(const LoaderParams* pParams, void (*callback)()) : SDLGameObject(pParams), m_callback(callback)
{
	setCurrentFrame(MOUSE_OUT); // start at frame 0
}

void MenuButton::draw()
{
	SDLGameObject::draw(); // use the base class drawing
}

void MenuButton::update()
{
	Vector* pMousePos = TheInputHandler::Instance()->getMousePosition();
	if (pMousePos->getX() < (getPosition().getX() + getWidth())
		&& pMousePos->getX() > getPosition().getX()
		&& pMousePos->getY() < (getPosition().getY() + getHeight())
		&& pMousePos->getY() > getPosition().getY())
	{
		setCurrentFrame(MOUSE_OVER);
		if (TheInputHandler::Instance()->getMouseButtonState(LEFT) && m_bReleased)
		{
			setCurrentFrame(CLICKED);
			if (m_callback != 0)
			{
				m_callback();
			}
			m_bReleased = false;
		}
		else if (!TheInputHandler::Instance()->getMouseButtonState(LEFT))
		{
			m_bReleased = true;
			setCurrentFrame(MOUSE_OVER);
		}
	}
	else
	{
		setCurrentFrame(MOUSE_OUT);
	}
}

void MenuButton::clean()
{
	SDLGameObject::clean();
}