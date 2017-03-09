#include <iostream>
#include <string>
#include <stdlib.h>

using namespace std;

int main()
{
	const double factor = 0.09290304;
	
	string length, width;
	double feetArea, metersArea, lengthFloat, widthFloat;
	
	cout << "What is the length of the room in feet?";
	cin >> length;
	cout << "What is the width of the room in feet?";
	cin >> width;
	
	lengthFloat = atof(length.c_str());
	widthFloat = atof(width.c_str());
	
	feetArea = lengthFloat * widthFloat;
	metersArea = feetArea * factor;
	
	cout << "You entered dimensions of " << lengthFloat << " feet by " << widthFloat << " feet.";
	cout << "The area is\n" << feetArea << " square feet\n" << metersArea << " square meters\n";
} 

/*TO DO: Check if input is valid*/
