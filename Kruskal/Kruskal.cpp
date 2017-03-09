//============================================================================
// Name        : Kruskal.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Kruskal implementation
//============================================================================

#include <iostream>
#include <fstream>
#include <cstdio>
#include <string>
#include "DisjointSet.h"

using namespace std;

#define edge pair< int, int >

/*Function tokenize split a string by delimiters*/
void Tokenize(const string& str,
                      vector<string>& tokens,
                      const string& delimiters = ",")
{
    // Skip delimiters at beginning.
    string::size_type lastPos = str.find_first_not_of(delimiters, 0);
    // Find first "non-delimiter".
    string::size_type pos     = str.find_first_of(delimiters, lastPos);

    while (string::npos != pos || string::npos != lastPos)
    {
        // Found a token, add it to the vector.
        tokens.push_back(str.substr(lastPos, pos - lastPos));
        // Skip delimiters.  Note the "not_of"
        lastPos = str.find_first_not_of(delimiters, pos);
        // Find next "non-delimiter"
        pos = str.find_first_of(delimiters, lastPos);
    }
}

int main(int argc, char** argv) {
	int n = 0;
	int initialWeight = 0;

	if (argc != 2)
	{
		std::cout<<"usage: "<< argv[0] <<" <filename>\n";
	return -1;
	}

	std::ifstream infile(argv[1]); //open the file
	std::string str;
	vector<string> lines;
	vector<string> tokens;

	//Read the file and push each line into a vector
	if (infile.is_open() && infile.good()) {
		while (std::getline(infile, str))
		{
		  lines.push_back(str);
		}

	} else {
		cout << "Failed to open file..";
	}

	//create a forest F (a set of trees),
	//where each vertex in the graph is a separate tree
	n = lines.size();
	DisjointSet *vertices = new DisjointSet(n);

	//create a set S containing all the edges in the graph
	//The pair contains weight, edge
	std::vector< pair < int, edge > > G; //declare the graph

	for(int i = 0; i < n; ++i){
		tokens.clear();
		Tokenize(lines[i], tokens); //split each line for take the values of the edges

		for (int j = 0; j < i; ++j) {
			if (tokens[j] != "-") {
				int weight = atoi(tokens[j].c_str());
				G.push_back(pair<int, edge>(weight, edge(i, j))); //complete the graph
				initialWeight += weight;
			}
		}
	}

	sort(G.begin(), G.end()); // increasing weight

	int k = 0;

	//while S is nonempty and F is not yet spanning
	int minSpanningTreeWeight = 0;

	while (!vertices->isSpanning()) {
		//remove an edge with minimum weight from S
		//Since we have a sorted list we just go through the list
		//if that edge connects two different trees, then add it to the forest,
		//combining two trees into a single tree
		if(vertices->find(G[k].second.first) != vertices->find(G[k].second.second)){
			vertices->Union(G[k].second.first, G[k].second.second);
			minSpanningTreeWeight += G[k].first;
		}
		k++;
	}

	std::cout << "the saving is: " << initialWeight - minSpanningTreeWeight << "\n";
	return 0;
}
