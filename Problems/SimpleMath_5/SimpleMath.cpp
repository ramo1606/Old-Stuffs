#include <string>
#include <iostream>
#include <stdlib.h>
#include <stdio.h>

using namespace std;

int main ()
{
    string str1, str2, endptr1, endptr2;
    double dbl1, dbl2;
    //while(true)
    //{
        cout << "Enter first number: ";
        cin >> str1;
        cout << "Enter second number: ";
        cin >> str2;
    //}
    dbl1 = atof(str1.c_str());
	dbl2 = atof(str2.c_str());

	double add = dbl1 + dbl2;
	double dif = dbl1 - dbl2;
	double prod = dbl1 * dbl2;
	double quot = dbl1 / dbl2;

	cout << dbl1 << " + " << dbl2 << " = " << add << "\n" << dbl1 << " - " << dbl2 << " = " << dif << "\n";
	cout << dbl1 << " * " << dbl2 << " = " << prod << "\n" << dbl1 << " / " << dbl2 << " = " << quot << "\n";
}

/*TO DO: Check the input to ensure that the input is a valid number*/
