#include <iostream>
#include <string>
#include <stdlib.h>

using namespace std;

int main()
{
	string people, pieces;
	int peopleInt, piecesInt, pizzasInt, leftover;
	
	cout << "How Many People? ";
	cin >> people;
	cout << "How Many pieces of Pizzas they want? ";
	cin >> pieces;
	
	peopleInt = atoi(people.c_str());
	piecesInt = atoi(pieces.c_str());
	
	pizzasInt = (piecesInt * peopleInt) / 8;
	leftover = (piecesInt * peopleInt) % 8;
	
	cout << peopleInt << " people want " << piecesInt << " pieces each\n";
	if (leftover != 0)
		pizzasInt += 1;
	cout << "You need " << pizzasInt << " pizzas.\n";
	//cout << "There are " << leftover << " leftover pieces.\n";
} 

/*TO DO: Check if input is valid*/
