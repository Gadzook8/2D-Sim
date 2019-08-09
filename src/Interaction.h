#ifndef INTERACTION_H
#define INTERACTION_H

#include <vector>

#include "Parameters.h"
#include "Particle.h"
#include "kiss.h"

class Interaction{ 
	
private:
   double sigma = 0; 
   double sigma_par = 0; 
   
   double rest_L = 0;   // these two quantities are for the 
   double k_spring = 0; // spring like potential
   
   double redDens = 0; 
   double red_temp = 0; 

   double LJ_par = 0; 
   double LJ_antipar = 0; 

   int interact_type = 0; 

   double tail_corr = 0; 
   double truncDist = 0;
   double truncShift = 0; 

   double boxLength = 0; 
   int n_particles = 0;  
public: 

   void initializeInteraction(Parameters* p); 
   void populateCellArray(double x, double y, 
		          std::vector<std::vector<double>>* cellPositions); 

   double distance(double x1, double x2, double y1, double y2, int type);
   
   double lenjones_energy(double r, double a); 
   double WCA_energy(double r); 
   double simple_spring_energy(double r, double a); 

   double nonPeriodicInteraction(std::vector<Particle>* particles, int index); 
   double periodicInteraction   (std::vector<Particle>* particles, int index); 
   bool hardDisks               (std::vector<Particle>* particles, int index);


};
#endif
