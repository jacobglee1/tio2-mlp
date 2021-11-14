#units real # distances in A, energy in Kcal/mole, pressure in atmospheres,time in femtoseconds

variable n2p2Cutoff equal  8.467 # largest symmetry function cutoff (Angstrom) (8.467A=16Bohr)
variable n2p2Dir string "../../cur90-r-2"

mass 2 47.86 # Ti
mass 1 16.00 # O

set type 2 charge 1.6579436 # original 2.196 # Ti
set type 1  charge -0.82897182 # original -1.098 # O

kspace_style pppm 1e-6

pair_style hybrid/overlay nnp dir ${n2p2Dir} showew no showewsum 10 resetew yes maxew 100000 cflength 1.8897261328 cfenergy 0.0015936014 emap "1:O,2:Ti" buck/coul/long  12.0
#pair_style buck/coul/long  12.0

# n2p2
pair_coeff * * nnp ${n2p2Cutoff}

# reMA
pair_coeff 2 2 buck/coul/long 409063 0.154 68.9682 # Ti Ti
pair_coeff 1 2 buck/coul/long 222900 0.194 165.524 # O Ti
pair_coeff 1 1 buck/coul/long 154880 0.234 397.257 # O O
