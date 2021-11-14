import sys

def main(prefix):
    # input file
    infile = open(prefix + '.xyz',"r")
    # Output position
    outfile = open(prefix+"-fixed.xyz","w")
    i = 0
    for line in infile:
        if i >= 2:
            lst = line.split()
            if lst[0] == '1':
                lst[0] = 'O'
            if lst[0] == '2':
                lst[0] = 'Ti'
            strng = "    ".join(lst) + "\n"
            outfile.write(strng)
        else:
            outfile.write(line)
        i += 1


if __name__ == '__main__':
    main(sys.argv[1])