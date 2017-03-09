#include <iostream>
#include <string>
#include <cstdlib>
#include <stdio.h>

using namespace std;

int main() {
  
    string noun, verb, adjective, adverb;
  
    std::cout << "Enter a noun: ";
    cin >> noun;
    std::cout << "Enter a verb: ";
    cin >> verb;
    std::cout << "Enter an adjective: ";
    cin >> adjective;
    std::cout << "Enter an adverb: ";
    cin >> adverb;
  
    printf("Do you %s your %s %s %s?", verb.c_str(), adjective.c_str(), noun.c_str(), adverb.c_str());
}
