/*
 * DisjointSet.cpp
 *
 *  Created on: 8/5/2015
 *      Author: ramo
 */

#include "DisjointSet.h"

DisjointSet::DisjointSet(int count): count(count) {
	parent = new int[this->count];
	for(int i = 0; i < this->count; i++){
		parent[i] = i;
	}
	int j = parent[26];
}

int DisjointSet::find(int i){
	if (parent[i] == i) {
		return i;
	} else {
		parent[i] = find(parent[i]);
		return parent[i];
	}
}

void DisjointSet::Union(int i, int j){
	parent[find(i)] =  find(j);
}

bool DisjointSet::isSpanning(){
	for (int i = 1; i < count; ++i) {
		if (find(0) != find(i)) return false;
	}
	return true;
}

DisjointSet::~DisjointSet() {
	// TODO Auto-generated destructor stub
}
