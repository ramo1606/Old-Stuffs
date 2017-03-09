#pragma once
#ifndef __Vector__
#define __Vector__

#include<math.h>
class Vector
{
public:
public:
	Vector();
	Vector(const Vector& v);
	Vector(double x, double y, double z);
	Vector(int x, int y, int z);

	void Set(double x1, double y1, double z1);
	void Set(const Vector& v);
	double getX() { return x; }
	void setX(double v) { x = v; }
	double getY() { return y; }
	void setY(double v) { y = v; }
	double getZ() { return z; }
	void setZ(double v) { z = v; }
	void Move(double mx, double my, double mz);
	void operator+=(const Vector& v);
	void operator-=(const Vector& v);
	void operator*=(const Vector& v);
	void operator/=(const Vector& v);
	bool operator==(const Vector& v) const;
	bool operator!=(const Vector& p) const;
	Vector& operator=(const Vector& v);
	Vector operator/(double px);
	Vector operator-(const Vector& v) const;
	double Distance(const Vector& v);
	double Length();
	double DotProduct(const Vector& v);
	Vector CrossProduct(const Vector& v);
	Vector Normal();

private:
	double x, y, z;
};

#endif