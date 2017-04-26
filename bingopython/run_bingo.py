"""
Created on Mon Feb 08 2016

@author: ivandebono

    Runs BINGO, using a pre-written parameters file. Waits for BINGO to finish before 
    returning. 

"""
# The default parameters are suitable for Wiggly Whipped 2nd Order

def run_bingo(bingo_exec_dir,bingo_fname,cosmo_prim,
                param4=1.0e-2,start_with_slow_roll = 'T',phi_i = 16.5e0,phi_dot_i = ' ',
                multi_phase = 'F',expected_multi_phase_end = ' ',pivot_scale =' ',
                Npivot =' ',force_aini= 'F',Nicond=' ',calcfnl= 'F',
                logki =  -5 ,logkf = 1,num_k=581,accuracy=3,Term=0,
                Equilateral='T',Isosceles='F',Squeezed='F',Scalene='F',output_dir='plots'):

    import os
    import subprocess
  
    param1=cosmo_prim['wwi_gamma']
    param2=cosmo_prim['wwi_lambda']
    param3=cosmo_prim['wwi_phi0']

    args = locals()
    
# Get all parameters into the BINGO fnlparam.ini format
    bingo_params_text = ""
    for key in args:
        keyname = key        
        line_str = "=".join((keyname, str(args[key])))
        bingo_params_text += line_str + "\n"

    print("Writing parameters to", bingo_fname)
    f = open(bingo_fname, 'w')
    f.write(bingo_params_text)
    f.close()

# Change directory and call BINGO
    cwd = os.getcwd()
    os.chdir(bingo_exec_dir)
    print("Running BINGO on", bingo_exec_dir)
    #output = subprocess.check_output(['make', 'run'])    
    output = subprocess.check_output(['time', './bingo2.out', bingo_fname])        
    # Capture screen output
    for line in output.decode().split("\n"):
        print(line)
    # Change back to the original directory
    os.chdir(cwd)   

    return output,args


# Read BINGO output
def rd_bingo_ps(bingo_exec_dir,output_dir):

    import numpy as np

    filename=bingo_exec_dir+'/'+output_dir+'/PS.txt'
    k,pkprim=np.loadtxt(filename, unpack=True)
    ps={'k':k,'pkprim':pkprim}
    return ps

# Plot BINGO scalar primordial power spectrum
def plt_bingo(ps):
    
    import matplotlib.pyplot as plt

    plt.loglog(ps['k'],ps['pkprim'])
    plt.xlabel('$k\, [\mathrm{Mpc}^{-1}]$'),plt.ylabel('$P(k)_\mathrm{prim} \, [\mathrm{Mpc}^{3}]$')
    plt.show()


# Read all BINGO output
def rd_bingo(bingo_exec_dir,output_dir):

    import numpy as np
    import os
    directory=os.path.join(bingo_exec_dir,output_dir)

    k,pkprim=np.loadtxt(directory+'/PS.txt', unpack=True)
    ps={'k':k,'pkprim':pkprim}

    n,dphi_dn=np.loadtxt(directory+'/DPHI_DN.dat', unpack=True)
    dphi_dn={'n':n,'dphi_dn':dphi_dn}

    n,epsilon=np.loadtxt(directory+'/EPSILON.dat', unpack=True)
    epsilon={'n':n,'epsilon':epsilon}

    n,phi_n=np.loadtxt(directory+'/PHI.dat', unpack=True)
    phi={'n':n,'phi_n':phi_n}

    n,phi_nn=np.loadtxt(directory+'/PHINN.dat', unpack=True)
    phinn={'n':n,'phi_nn':phi_nn}

    n,h=np.loadtxt(directory+'/HUBBLE.dat', unpack=True)
    hubble={'n':n,'h':h}

    k,k6=np.loadtxt(directory+'/k6-G_0.txt', unpack=True)
    k6={'k':k,'k6':k6}
    
    if 'F_NL-RE.dat' in os.listdir(directory):
        k,f_nl=np.loadtxt(directory+'/F_NL-RE.dat', unpack=True)
        f_nl={'k':k,'f_nl':f_nl}    
        bingo_out={'ps':ps,'dphi_dn':dphi_dn,'epsilon':epsilon,'phi':phi,'hubble':hubble,\
                    'k6':k6,'phinn':phinn,'f_nl':f_nl}
    else:
        bingo_out={'ps':ps,'dphi_dn':dphi_dn,'epsilon':epsilon,'phi':phi,'hubble':hubble,\
                  'phinn':phinn,'k6':k6}


    return bingo_out
