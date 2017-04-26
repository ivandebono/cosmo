"""
Written 10 Feb 2016
@Ivan Debono

Runs BINGO.
Writes parameters to temporary file.
Outputs scalar primordial power spectrum to a temporary directory
Reads the output
OUPUT: Wiggly Whipped scalar P(k)_prim plots
"""

def mk_wwi():

    from run_bingo import run_bingo
    from run_bingo import rd_bingo_ps
    from run_bingo import plt_bingo
    import os
    import tempfile

    #Wiggly Whipped parameters
    cosmo_prim={'wwi_gamma': 2.68e-11,'wwi_lambda':5.2e-13,'wwi_phi0':14.59}

    working_dir=os.getcwd()
    bingo_exec_dir='bingo-2.0'

    with tempfile.TemporaryDirectory(prefix='tempdir',dir=os.path.join(working_dir,\
          bingo_exec_dir)) as output_dir_temp:
        output_dir=str(output_dir_temp.split("/")[-1])
        bingo_fname=output_dir_temp+'/fnlparam'+output_dir+'.ini'
        output,input=run_bingo(bingo_exec_dir,bingo_fname,cosmo_prim,
                        output_dir=output_dir)
        ps=rd_bingo_ps(bingo_exec_dir,output_dir)

    plt_bingo(ps)

    return ps

