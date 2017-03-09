#include<stdlib.h>
#include<stdio.h>
#include<iostream>

using namespace std;

typedef char * arrayString;

int length(arrayString s)
{
    int _count = 0;
    while(s[_count] != 0)
    {
        _count++;
    }
    return _count;
}

char characterAt(arrayString s, int position)
{
    return s[position];
}

void append(arrayString& s, char c)
{
    int oldLength = length(s);
    arrayString newS = new char[oldLength + 2];
    for(int i = 0; i < oldLength; ++i)
    {
        newS[i] = s[i];
    }

    newS[oldLength] = c;
    newS[oldLength+1] = 0;

    delete[] s;
    s = newS;
}

void concatenate(arrayString& s1, arrayString& s2)
{
    int s1Length = length(s1);
    int s2Length = length(s2);

    int newLength = s1Length + s2Length;

    arrayString newS = new char[newLength + 1];

    for(int i = 0; i < s1Length; ++i)
    {
            newS[i] = s1[i];
    }
    for(int i = 0; i < s2Length; ++i)
    {
            newS[s1Length + i] = s2[i];
    }

    newS[newLength] = 0;
    delete[] s2;
    s2 = newS;
}

int main()
{
    arrayString a = new char[5];
    a[0] = 't'; a[1] = 'e'; a[2] = 's'; a[3] = 't'; a[4] = 0;
    arrayString b = new char[4];
    b[0] = 'b'; b[1] = 'e'; b[2] = 'd'; b[3] = 0;
    append(a, '!');
    concatenate(a, b);
    cout << a << "\n";
    cout << b << "\n";
}
