#include <iostream>
#include "Parameters.h"

// Parameters::Parameters(){
// 	n_updates = 0; 
// 	n_particles = 0; 
// 	seed = 0; 
// 	weight = 0; 
// }

///// GETTERS ////////////////

int Parameters::getUpdates(){
	return n_updates; 
} 	
int Parameters::getNumParticles(){
	return n_particles; 
}
long Parameters::getSeed(){
	return seed; 
}

double Parameters::getWeight(){
	return weight; 
}

bool Parameters::getRigidBC(){
	return rigidBC; 
}

///////// SETTERS /////////////

void Parameters::setUpdates(int u){
	n_updates = u; 
}
void Parameters::setNumParticles(int num){
	n_particles = num; 
}
void Parameters::setSeed(long s){
	seed = s; 
}

void Parameters::setWeight(double w){
	weight = w; 
}

void Parameters::setRigidBC(bool r){
	rigidBC = r; 
}