#include <iostream>
#include <string>
#include <stdlib.h>
#include <math.h>

using namespace std;

int main()
{
    const double feetPerGallons = 350;

	string length, width;
	int gallons;
	double lengthDbl, widthDbl, squareArea;

	cout << "What's the length of the room? ";
	cin >> length;
	cout << "What's the width of the room? ";
	cin >> width;

	lengthDbl = atof(length.c_str());
	widthDbl = atof(width.c_str());

	squareArea = lengthDbl * widthDbl;
	gallons = ceil(squareArea / feetPerGallons);

	cout << "You will need to purchase " << gallons << " gallons of paint to cover " << squareArea << " square feets";
}

/*TO DO: Check if input is valid*/
