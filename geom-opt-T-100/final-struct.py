import sys

def main(prefix):
    infile = open(prefix + '.lammpstrj',"r")
    # Output position
    outfile = open(prefix+"-last.lammpstrj","w")
    numStruct = 0
    i = 0
    start = []
    for line in infile:
        if line.strip() == 'ITEM: TIMESTEP':
            numStruct += 1
            start.append(i)
        i += 1
    infile2 = open(prefix + '.lammpstrj',"r")
    j = 0
    for line in infile2:
        if j == start[len(start)-1]:
            outfile.write(line)
        if j == start[len(start)-1] + 1:
            outfile.write(str(0) + '\n')   
        if j >= start[len(start)-1] + 2:
            outfile.write(line)
        j += 1

if __name__ == '__main__':
    main(sys.argv[1])
