import sys
import parser

if __name__ == '__main__':
    with open(sys.argv[1], 'r') as file:
        par = parser.Parser(file.read())

    while par.definition():
        pass

    if par.last_error is not None:
        print(par.last_error)
