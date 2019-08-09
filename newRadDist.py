import math 
from scipy.interpolate import make_interp_spline, BSpline
import matplotlib.pyplot as plt
import numpy as np
import yaml

# Normalizes the set based on the total 
#   number of trials in the set
# Returns the radial distribution function
def calculateRadDist(N,numberTrials,total_dens):
    G = np.zeros(len(N))
    G = [x/(n_particles*numberTrials*total_dens) for x in N]
    print(n_particles,len(N),total_dens)
    return G

# Creates an unnormalized vector of densities
# Accepts a vector of the number density and
#   the value of deltaR
def calcDensity(num_dens, r_iter, deltaR):
    N = np.zeros(len(num_dens))
    for k in range(len(r_iter)): 
        if(k == 0):
            area = math.pi * deltaR**2 / 4.0
        else: 
            area = 2.0 * math.pi * r_iter[k]*deltaR
        N[k] = num_dens[k]/area    

    return N 

# Read in the number density
# The data has not yet been normalized 
def readData(file_name): 
    with open(file_name,'r') as f: 
        n = f.read().split(' ')
        n = [float(i) for i in n if(i != '' and i != '\n')]    
        n = np.asarray(n)
    f.close()
    return n 

### GIVES THE OPTION TO SAVE THE GENERATED IMAGE ##
def saveImage():
    s = input("would you like to save the image? (y/n)")
    if(s == 'y'):
#         file_name = 'RDF_dens_' + str(redDens).replace('.','_') + \
#                     'temp_' + str(red_temp).replace('.','_') + \
#                     '.png'
        file_name = input("Enter the name of the image: ") + '.png'    
        print(file_name)
        plt.savefig('data/' + file_name)
        plt.close()

n_dens = readData('numDensity.txt')
par_dens = readData('par_numDensity.txt')
antp_dens = readData('antp_numDensity.txt')

dens_vec = [n_dens,par_dens,antp_dens]

# read in system parameters from yaml file
with open("params.yaml",'r') as yf:
    yaml_dict = yaml.safe_load(yf)

boxL = yaml_dict["boxLength"]
n_particles = yaml_dict["totalParticles"]
sigma = yaml_dict["sigma"]
redDens = yaml_dict["reducedDens"]
n_eq = yaml_dict["equilibriate_sweep"]
n_updates = yaml_dict["numberUpdates"]
interval = yaml_dict["data_collect_interval"]
red_temp = yaml_dict["reducedTemp"]

if(boxL == 0): 
    boxL = sigma * math.sqrt(n_particles/redDens)
if(sigma == 0):
    sigma = boxL * math.sqrt(redDens/n_particles)
if(redDens == 0):
    redDens = n_particles * sigma**2 / boxL**2

total_dens = n_particles / boxL**2
 
##### PREPARE SYSTEM ##############
numberTrials = (n_updates-n_eq)/interval - 1  # this needs to be added to the yaml file
deltaR = sigma/20.0 
r_iter = np.linspace(0,.5*boxL,(.5 * boxL)/deltaR + 1.0)

##### PLOT DATA ###################
choice = input("Do you want all of the plots?(y/n)")

# 'y' will create an image with the regular RDF, parallel RDF, and antiparallel RDF
# anything else will create an image with the regular RDF
if(choice == 'y'):  
    fig, axs = plt.subplots(1,3, figsize=(12, 3), 
               facecolor='w', edgecolor='k',squeeze = False)
    fig.subplots_adjust(hspace = .5, wspace=.2)
    num = 3
else: 
    fig, axs = plt.subplots(figsize = (7,5),
               facecolor = 'w',edgecolor='k',squeeze = False)
    num = 1

titles = ['Radial Distribution Function','Parallel RDF','Antiparallel RDF' \
         ,'x RDF', 'y RDF']
for k in range(num):
    N = calcDensity(dens_vec[k],r_iter,deltaR)
    G = calculateRadDist(N,numberTrials,total_dens)
    
    axs[0,k].plot(r_iter,G)
    axs[0,k].axvline(x = 2.0**(1.0/6.0),color = 'r', linestyle = '--')
    axs[0,k].axvline(x = 2.0**(7.0/6.0),linestyle = '--')
    axs[0,k].axhline(y = 1, linestyle = '--')

    axs[0,k].set_title(titles[k])
    axs[0,k].legend(['RDF',r'$2^{1/6}$',r'$2^{7/6}$']) # ,r'$3*2^{1/6}$'])
    axs[0,k].set_xlabel(r'$\frac{r}{\sigma}$')

    axs[0,k].set_xlim([0,boxL/2 - 2 * deltaR])
    if(k == 0):
        axs[0,k].set_ylabel(r'$g(\frac{r}{\sigma})$')
        max_y = max(G) * 1.1
    axs[0,k].set_ylim([0,max_y])


# saveImage()
# plt.show()  

def init_pos_matrix(val,cell_L): # this creates a 3D matrix that is 
    s_2 = math.sqrt(2)
    M = np.zeros(shape=(val,val,2)) # contains each x,y coordinate
    for k in range(val):            # associated with the 2D 
        k0 = -.5 *s_2* boxL + k*cell_L; # number density and is used to 
        for n in range(val):        # calculate the RDF from the 
            n0 = -.5 *s_2* boxL + n*cell_L # PCF
            M[k][n] = [k0,n0]
    return M 

def format_xy_dens(val,data):
    matrices = []
    for z in range(len(data)): 
        d = data[z]
        d = [x/(n_particles*numberTrials) for x in d]
        M = np.zeros(shape=(val,val))
        flg = 0
        for k in range(val):
            for n in range(val): 
                M[k][n] = d[flg]
                flg = flg + 1
        matrices.append(M)
    return matrices # returns a list of 3 2D arrays

def display_PCF(val,dens):
    num = len(dens)
    if(num == 1): 
        f = (5,5)
    else:
        f = (12,4)
    fig,axs = plt.subplots(1,num, figsize = f, \
              facecolor='w', edgecolor='k',squeeze = False)
    txt = '2D Histogram of the Pair Correlation Function'

    if(num != 1): 
        fig.tight_layout()
        fig.subplots_adjust(top = .85,bottom = .12,left=.05,wspace=.22)
        fig.suptitle(txt)
        titles = ['Parallel and Antiparallel','Parallel','Antiparallel']
    else:
        titles = [txt]
    
    x = np.linspace(-boxL/2,boxL/2,val)
    y = x
    for k in range(num): 
        print(k)
        axs[0][k].contourf(x,y,dens[k])
        axs[0][k].set_title(titles[k])
        
        axs[0][k].set_xlabel('x Position')
        axs[0][k].set_ylabel('y Position')
    
    saveImage();
    plt.show()

def create_1D_num_dens(dens_2D,pos,val,delta_r):
    r_vec = np.linspace(0,boxL/2.0,boxL/(2.0 * delta_r) + 1.0)
    dens_1D = np.zeros(len(r_vec))
    M = []
    for z in range(len(dens_2D)): 
        d = dens_2D[z]
        dens_1D = np.zeros(len(r_vec))
        for k in range(val):
            for n in range(val): 
                x = pos[k][n][0]
                y = pos[k][n][1]
                r = math.sqrt(x**2 + y**2)
                if(r < boxL/2.0 - delta_r):
                    index = int(r/delta_r)
                    if(r > (index + .5) * delta_r):
                        index = index + 1
                    dens_1D[index] = dens_1D[index] + d[k][n]
        M.append(dens_1D)
    return r_vec,M

def calc_RDF(r_vec,dens_1D,delta_r):
    total_dens = n_particles/boxL**2
    for z in range(len(dens_1D)): 
        d = dens_1D[z]
        for k in range(len(r_vec)): 
            if(k == 0): 
                area = math.pi*delta_r**2*.25
            else: 
                area = 2.0*math.pi*r_vec[k]*delta_r

            d[k] = d[k] / area
        d = [i/total_dens for i in d]
        dens_1D[z] = d
    return dens_1D

def plot_RDF(r_vec,RDF,delta_r): 
    num = len(RDF)
    if(num == 1): 
        f = (7,5)
    else:
        f = (12,3)
    
    fig,axs = plt.subplots(1,num, figsize = f, \
              facecolor='w', edgecolor='k',squeeze = False)
    txt = 'RDF from the Pair Correlation Function'
    
    if(num != 1): 
        fig.tight_layout()
        fig.subplots_adjust(top = .8,bottom =.18,left=.05,wspace=.22)
        fig.suptitle(txt)
        titles = ['Parallel and Antiparallel','Parallel','Antiparallel']
    else:
        titles = [txt]
    for k in range(num): 
        axs[0][k].plot(r_vec,RDF[k])
        axs[0][k].axvline(x = 2.0**(1.0/6.0),color = 'red',linestyle = '--')
        axs[0][k].axhline(y = 1,color = 'orange',linestyle = '--')
        axs[0][k].axvline(x = 2.0**(2.0/3.0),color = 'yellow',linestyle = '--')
#         axs[0][k].axvline(x = 1,color = 'red',linestyle = '--')
#         axs[0][k].axvline(x = math.sqrt(2),color = 'orange',linestyle = '--')
        axs[0][k].set_title(titles[k])
        axs[0][k].set_xlabel(r'$\frac{r}{\sigma}$')
        axs[0][k].set_ylabel(r'$g(\frac{r}{\sigma})$')

        axs[0][k].set_xlim([0,boxL/2 - 2*delta_r])
        axs[0][k].set_ylim([0,max(RDF[0])*1.1])
    
    saveImage() 
    plt.show()

def run_pcf():
    
    # read in data and set parameters
    n      = readData("xy_numDensity.txt")
    par_n  = readData("par_xy_numDensity.txt")
    antp_n = readData("antp_xy_numDensity.txt")
    
    c = input("Would you like all of the plots?(y/n) ")
    if(c == 'y'):
        densities = [n,par_n,antp_n]
    else:
        densities = [n]
    
    cell_L = sigma/20.0
    delta_r = sigma/15.0

    # create a matrix of the different x,y
    # coordinate positions
    val = int(math.sqrt(2)*boxL/cell_L) + 1
    pos = init_pos_matrix(val,cell_L)
    
    # normalize the number density data
    densities = format_xy_dens(val,densities)

    # plot the pair correlation function
    display_PCF(val,densities)   
    
    # create a matrix of the different x,y 
    # coordinate positions and create 
    # a 1D number density vector
    r_vec,dens_1D = create_1D_num_dens(densities,pos,\
                                        val,delta_r); 
    # calculate and plot the radial 
    # distribution function
    RDF = calc_RDF(r_vec,dens_1D,delta_r)
    plot_RDF(r_vec,RDF,delta_r)

run_pcf()
# plt.show();
