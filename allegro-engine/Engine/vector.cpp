#include "vector.h"

namespace Advanced2D
{

	Vector::Vector()
	{
		x = y = z = 0;
	}

	Vector::Vector( const Vector& v )
	{
		*this = v;
	}

	Vector::Vector( double x, double y, double z )
	{
		Set( x, y, z );
	}

	Vector::Vector( int x, int y, int z)
	{
		Set((double)x,(double)y,(double)z);
	}

	void Vector::Set( double x1,double y1,double z1 )
	{
		x=x1; y=y1; z=z1;
	}

	void Vector::Set( const Vector& v)
	{
		x=v.x; y=v.y; z=v.z;
	}

	void Vector::Move( double mx,double my,double mz)
	{
		x+=mx; y+=my; z+=mz;
	}

	void Vector::operator+=(const Vector& v)
	{
		x+=v.x; y+=v.y; z+=v.z;
	}

	void Vector::operator-=(const Vector& v)
	{
		x-=v.x; y-=v.y; z-=v.z;
	}

	void Vector::operator*=(const Vector& v)
	{
		x*=v.x; y*=v.y; z*=v.z;
	}

	void Vector::operator/=(const Vector& v)
	{
		x/=v.x; y/=v.y; z/=v.z;
	}

	//equality operator comparison includes double rounding
	bool Vector::operator==( const Vector& v ) const
	{
		return (
			(((v.x - 0.0001f) < x) && (x < (v.x + 0.0001f))) &&
			(((v.y - 0.0001f) < y) && (y < (v.y + 0.0001f))) &&
			(((v.z - 0.0001f) < z) && (z < (v.z + 0.0001f))) );
	}

	//inequality operator
	bool Vector::operator!=( const Vector& p ) const
	{
		return (!(*this == p));
	}

	//assign operator
	Vector& Vector::operator=( const Vector& v)
	{
		Set(v);
		return *this;
	}

	//distance only coded for 2D
	double Vector::Distance( const Vector& v )
	{
		return sqrt((v.x-x)*(v.x-x) + (v.y-y)*(v.y-y));
	}

	//Vector3 length is distance from the origin
	double Vector::Length()
	{
		return sqrt(x*x + y*y + z*z);
	}

	//dot/scalar product: difference between two directions
	double Vector::DotProduct( const Vector& v )
	{
		return (x*v.x + y*v.y + z*v.z);
	}

	//cross/Vector product is used to calculate the normal
	Vector Vector::CrossProduct( const Vector& v )
	{
		double nx = (y*v.z)-(z*v.y);
		double ny = (z*v.y)-(x*v.z);
		double nz = (x*v.y)-(y*v.x);
		return Vector(nx,ny,nz);
	}

	//calculate normal angle of the Vector
	Vector Vector::Normal()
	{
		double length;
		if (Length() == 0)
			length = 0;
		else
			length = 1 / Length();
		double nx = x*length;
		double ny = y*length;
		double nz = z*length;
		return Vector(nx,ny,nz);
	}
}; //namespace
