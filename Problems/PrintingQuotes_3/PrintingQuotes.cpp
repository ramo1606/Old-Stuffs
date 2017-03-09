#include <iostream>
#include <string>
#include <cstdlib>

using namespace std;

int main() {
  string quote, author;
  
  cout << "What is the quote? ";
  getline(cin, quote);
  cout << "Who said it? ";
  getline(cin, author);
  
  cout << author << " says, " << "\"" << quote << "\"";
}
