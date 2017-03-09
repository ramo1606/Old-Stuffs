#pragma once
#ifndef __SDLGameObject__
#define __SDLGameObject__

#include <SDL.h>
#include <string>
#include <iostream>
#include "TextureManager.h"
#include "GameObject.h"
#include "Vector.h"

class SDLGameObject : public GameObject
{
public:
	SDLGameObject(const LoaderParams* pParams);
	virtual ~SDLGameObject();

	virtual void draw();
	virtual void update();
	virtual void clean();

	void setPosition(double px, double py, double pz) { m_position.Set(px, py, pz); }
	void setPosition(Vector pv) { m_position = pv; }
	Vector getPosition() { return m_position; }
	void setVelocity(double px, double py, double pz) { m_velocity.Set(px, py, pz); }
	void setVelocity(Vector pv) { m_velocity = pv; }
	Vector getVelocity() { return m_velocity; }
	void setAcceleration(double px, double py, double pz) { m_acceleration.Set(px, py, pz); }
	void setAcceleration(Vector pv) { m_acceleration = pv; }
	Vector getAcceleration() { return m_acceleration; }
	
	void setWidth(int pWidth) { m_width = pWidth; }
	void setHeight(int pHeight) { m_height = pHeight; }
	int getWidth() { return m_width; }
	int getHeight() { return m_height; }

	void setTextureID(std::string pID) { m_textureID = pID; }
	void setCurrentFrame(int pCurrentFrame) { m_currentFrame = pCurrentFrame; }
	void setCurrentRow(int pCurrentRow) { m_currentRow = pCurrentRow; }
	std::string getTextureID() { return m_textureID; }
	int getCurrentFrame() { return m_currentFrame; }
	int getCurrentRow() { return m_currentRow; }

private:
	std::string m_textureID;
	int m_currentFrame;
	int m_currentRow;
	Vector m_position;
	Vector m_velocity;
	Vector m_acceleration;
	int m_width;
	int m_height;
};

#endif