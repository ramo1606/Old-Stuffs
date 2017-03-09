#include <iostream>
#include <string>
#include <cstdlib>

using namespace std;

int main()
{
	int lenght;
	string str;

	while (true)
	{
		cout << "Introduce a string: ";
		getline(cin, str);
		lenght = str.length();

		if (str == "")
		{
			str = "Please introduce a correct string.\n";
			cout << str;
			getchar();
			system("cls");
		}
		else
		{
			str = str + " has " + to_string(lenght) + " characters.\n";
			break;
		}
	}

	cout << str;

	return 0;
}