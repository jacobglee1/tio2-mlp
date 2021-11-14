prefix=$1
cabal res xyze < ${prefix}.res > ${prefix}.xyze
ovito ${prefix}.xyze
