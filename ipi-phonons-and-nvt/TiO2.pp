variable runnerCutoff    equal  8.4668354  # largest symmetry function cutoff (Angstrom)
variable runnerDir    string "../../cur90-r-2"

set type 2 charge 1.6579436 # original 2.196 # Ti
set type 1  charge -0.82897182 # original -1.098 # O

mass 2 47.86
mass 1 16.00

pair_style hybrid/overlay nnp dir ${runnerDir} showew no showewsum 10 resetew yes maxew 100000 cflength 1.8897261328 cfenergy 0.0015936014 buck/coul/long  12.0
pair_coeff * * nnp ${runnerCutoff}        # set up pair style coefficients
# NB the charges on the atoms should be: Ti +2.196e, O -1.098e 
# reMA potential
pair_coeff 2 2 buck/coul/long 409063 0.154 68.9682
pair_coeff 1 2 buck/coul/long 222900 0.194 165.524
pair_coeff 1 1 buck/coul/long 154880 0.234 397.257
kspace_style pppm 1e-5
