#!/usr/bin/python
# -*- coding: utf-8 -*-

# isolation with migration (IM) 
# ms tbs 10000 -t tbs -r tbs tbs -I 2 tbs tbs 0 -n 1 tbs -n 2 tbs -m 1 2 tbs -m 2 1 tbs -ej tbs 2 1 -eN tbs tbs
# nsamtot theta rho L nsamA nsamB N1 N2 M12 M21 Tsplit Tsplit Na

from numpy.random import uniform
from numpy.random import binomial
from random import shuffle

nMultilocus = 10000

N_bound = [0, 30]
T_bound = [0, 30]
M_bound = [0, 10]

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

# param monolocus: values that will be read by ms
priorfile = "N1\tN2\tNa\tTsplit\tM12\tM21\n"
for sim in range(nMultilocus):
	priorfile += "{0:.5f}\t{1:.5f}\t{2:.5f}\t{3:.5f}\t{4:.5f}\t{5:.5f}\n".format(N1[sim], N2[sim], Na[sim], Tsplit[sim], M12[sim], M21[sim])
	
	for locus in range(nLoci):
		# SC print("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6:.5f}\t{7:.5f}\t{8:.5f}\t{9:.5f}\t{10:.5f}\t{11:.5f}\t{12:.5f}\t{13:.5f}".format(nsam_tot[locus], theta[locus], rho[locus], L[locus], nsamA[locus], nsamB[locus], M12_vec[locus], M21_vec[locus], N1_vec[locus], N2_vec[locus], Tsc[sim], Tsplit[sim], Tsplit[sim], Na_vec[locus]))
		print("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6:.5f}\t{7:.5f}\t{8:.5f}\t{9:.5f}\t{10:.5f}\t{11:.5f}\t{12:.5f}".format(nsam_tot[locus], theta[locus], rho[locus], L[locus], nsamA[locus], nsamB[locus], N1[sim], N2[sim], M12[sim], M21[sim], Tsplit[sim], Tsplit[sim], Na[sim]))

outfile = open("priorfile.txt", "w")
outfile.write(priorfile)
outfile.close()

