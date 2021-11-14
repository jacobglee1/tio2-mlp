import sys

def main(prefix):
    # input file
    infile = open('start.xyz',"r")
    # Output position
    outfile = open("debye.geo","w")
    i = 0
    for line in infile:
        if i >= 2:
            lst = line.split()
            newLst = lst[1:]
            strng = "    ".join(newLst) + "\n"
            outfile.write(strng)
        i += 1


if __name__ == '__main__':
    main(sys.argv[1])