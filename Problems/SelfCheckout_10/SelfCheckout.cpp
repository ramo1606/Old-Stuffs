#include <iostream>
#include <string>
#include <stdlib.h>
#include <math.h>
#include <map>

using namespace std;

int main()
{
    const double taxRate = 0.055;
    double subtotal, total, tax;
    string addItem = "yes", item, quantity;
	bool moreItems = true;
	int itemCount = 1;
	map<string, string> itemList;

	while(moreItems)
	{
		cout << "Enter the price of item " << itemCount << " : ";
		cin >> item;
		cout << "Enter the quantity of item " << itemCount << " : ";
		cin >> quantity;
		
		itemList.insert(pair<string, string>(item, quantity));
		cout << "Add another item? ";
		cin >> addItem;
		if(addItem == "no")
			moreItems = false;
		else
		{
			itemCount++;
		}
		/*while(true)
		{
			if(addItem.)
			{
			}
			else if()
			{
			}
			else
			{
			}
		}*/
	}
	
	for(map<string, string>::const_iterator it = itemList.begin(); it != itemList.end(); ++it)
	{
		subtotal += atof(it->first.c_str()) * atof(it->second.c_str());
	}

	tax = subtotal * taxRate;
	total = tax + subtotal;

	cout << "Subtotal: " << subtotal << "\n";
	cout << "Taxes: " << tax << "\n";
	cout << "Total: " << total << "\n";
}

/*TO DO: Check if input is valid and program the add another item flow*/
