#include <iostream>
#include <string>
#include <stdlib.h>

using namespace std;

int main()
{
	string people, pizzas;
	int peopleInt, pizzasInt, leftover, pieces;
	
	cout << "How Many People? ";
	cin >> people;
	cout << "How Many Pizzas do you have? ";
	cin >> pizzas;
	
	peopleInt = atoi(people.c_str());
	pizzasInt = atoi(pizzas.c_str());
	
	pieces = (pizzasInt * 8) / peopleInt;
	leftover = (pizzasInt * 8) % peopleInt;
	
	cout << peopleInt << " people with " << pizzasInt << " pizzas\n";
	cout << "Each person gets " << pieces << " pieces of pizza.\n";
	cout << "There are " << leftover << " leftover pieces.\n";
} 

/*TO DO: Check if input is valid*/
