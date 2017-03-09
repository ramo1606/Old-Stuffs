/*
 * DisjointSet.h
 *
 *  Created on: 8/5/2015
 *      Author: ramo
 */

#ifndef DISJOINTSET_H_
#define DISJOINTSET_H_

#include <vector>
#include <algorithm>

class DisjointSet {
public:
	DisjointSet(int count);
	int find(int i);
	void Union(int i, int j);
	bool isSpanning();
	virtual ~DisjointSet();
private:
	int count;
	int *parent;
};

#endif /* DISJOINTSET_H_ */
