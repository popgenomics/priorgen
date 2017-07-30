#!/usr/bin/python
# -*- coding: utf-8 -*-

# secondary contact
# ms tbs 10000 -t tbs -r tbs tbs -I 2 tbs tbs 0 -m 1 2 tbs -m 2 1 tbs -n 1 tbs -n 2 tbs -eM tbs 0 -ej tbs 2 1 -eN tbs tbs
# nsamtot theta rho L nsamA nsamB M12 M21 N1 N2 Tsc Tsplit Tsplit Na

from numpy.random import uniform
from numpy.random import binomial
from random import shuffle

nMultilocus = 10

N_bound = [0, 30]
T_bound = [0, 30]
M_bound = [0, 10]
P_ntrl_N_bound = [0, 1] # ntrl_N loci with N and (1-ntrl_N) with bf.N
P_ntrl_M_bound = [0, 1] # ntrl_M loci with M >0; (1-ntrl_M) loci with M=0
bf_bound = [0, 1] # reduction in Ne for the (1-ntrl_N)

# read bpfile
infile = open("bpfile", "r")
tmp = infile.readline()
L = infile.readline().strip().split("\t")
nsamA = infile.readline().strip().split("\t")
nsamB = infile.readline().strip().split("\t")
theta = infile.readline().strip().split("\t")
rho = infile.readline().strip().split("\t")
infile.close()


# number of loci
nLoci = len(L)

# sum of nsamA + nsamB
nsam_tot = [ int(nsamA[i]) + int(nsamB[i]) for i in range(nLoci) ]

# param multilocus: values that will be printed in priorfile.txt
## N = N_pop_i / Nref
N1 = uniform(low = N_bound[0], high = N_bound[1], size = nMultilocus)
N2 = uniform(low = N_bound[0], high = N_bound[1], size = nMultilocus)
Na = uniform(low = N_bound[0], high = N_bound[1], size = nMultilocus)

## Miration rates
M12 = uniform(low = M_bound[0], high = M_bound[1], size = nMultilocus)
M21 = uniform(low = M_bound[0], high = M_bound[1], size = nMultilocus)

## times
Tsplit = uniform(low = T_bound[0], high = T_bound[1], size = nMultilocus)
Tsc = [ uniform(low = 0, high = Tsplit[i], size = 1)[0] for i in range(nMultilocus) ]

## bf = factor of local reduction in Ne. Model of "background selection"
bf = uniform(low=bf_bound[0], high=bf_bound[1], size = nMultilocus)

## number of neutral loci
ntrl_N = [ binomial(nLoci, uniform(P_ntrl_N_bound[0], P_ntrl_N_bound[1])) for i in range(nMultilocus) ]
ntrl_M12 = [ binomial(nLoci, uniform(P_ntrl_M_bound[0], P_ntrl_M_bound[1])) for i in range(nMultilocus) ]
ntrl_M21 = [ binomial(nLoci, uniform(P_ntrl_M_bound[0], P_ntrl_M_bound[1])) for i in range(nMultilocus) ]

# param monolocus: values that will be read by ms
priorfile = "N1\tN2\tNa\tprop_ntrl_N\tbf\tTsplit\tTsc\tM12\tprop_ntrl_M12\tM21\tprop_ntrl_M21\n"
for sim in range(nMultilocus):
	priorfile += "{0:.5f}\t{1:.5f}\t{2:.5f}\t{3}\t{4:.5f}\t{5:.5f}\t{6:.5f}\t{7:.5f}\t{8}\t{9:.5f}\t{10}\n".format(N1[sim], N2[sim], Na[sim], ntrl_N[sim], bf[sim], Tsplit[sim], Tsc[sim], M12[sim], ntrl_M12[sim], M21[sim], ntrl_M21[sim])
	# vectors of size 'nLoci' containing parameters
	bf_vec = ntrl_N[sim]*[1] + (nLoci - ntrl_N[sim])*[bf[sim]]
	shuffle(bf_vec)
	N1_vec = [ N1[sim]*bf_vec[i] for i in range(nLoci) ]
	N2_vec = [ N2[sim]*bf_vec[i] for i in range(nLoci) ]
	Na_vec = [ Na[sim]*bf_vec[i] for i in range(nLoci) ]
	
	M12_vec = [M12[sim]]*ntrl_M12[sim] + [0]*(nLoci - ntrl_M12[sim])
	shuffle(M12_vec)
	M21_vec = [M21[sim]]*ntrl_M21[sim] + [0]*(nLoci - ntrl_M21[sim])
	shuffle(M21_vec)
	
	for locus in range(nLoci):
		print("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6:.5f}\t{7:.5f}\t{8:.5f}\t{9:.5f}\t{10:.5f}\t{11:.5f}\t{12:.5f}\t{13:.5f}".format(nsam_tot[locus], theta[locus], rho[locus], L[locus], nsamA[locus], nsamB[locus], M12_vec[locus], M21_vec[locus], N1_vec[locus], N2_vec[locus], Tsc[sim], Tsplit[sim], Tsplit[sim], Na_vec[locus]))

outfile = open("priorfile.txt", "w")
outfile.write(priorfile)
outfile.close()

