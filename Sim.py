import os
from time import sleep as slp
cls = lambda : os.system("cls")

addr_def = '00000'
MainMem = [[(addr_def + str(bin(addr))[2:])[-6:], 0] for addr in range(64)]
cache = [[['------', 0] for _ in range(4)] for _ in range(4)]

first = cache
accesses = 0
hits = 0
miss = 0

def display(c,a,h,m, mem):
    hitrate = 0
    misrate = 0
    if a != 0:
        hitrate = int((h/a)*100)
        misrate = int((m/a)*100)
    print(f"""
\033[0;32m +- Config ---------------+\033[0;33m +- Cache -----------------------------------------+\033[0;31m +- Stats --------+\033[0;34m +--------------------------------------------+\033[0m
\033[0;32m |                        |\033[0;33m | +- 00 ----+ +- 01 ----+ +- 10 ----+ +- 11 ----+ |\033[0;31m |                |\033[0;34m |░█████╗░░█████╗░░█████╗░██╗░░██╗███████╗  \t|\033[0m
\033[0;32m | Blocks: 4              |\033[0;33m | |{c[0][0][0]}:{c[0][0][1]}\t| |{c[1][0][0]}:{c[1][0][1]} | |{c[2][0][0]}:{c[2][0][1]} | |{c[3][0][0]}:{c[3][0][1]} | |\033[0;31m | Acc : {a}\t |\033[0;34m |██╔══██╗██╔══██╗██╔══██╗██║░░██║██╔════╝\t|\033[0m
\033[0;32m | Block size : 4 words   |\033[0;33m | |{c[0][1][0]}:{c[0][1][1]}\t| |{c[1][1][0]}:{c[1][1][1]} | |{c[2][1][0]}:{c[2][1][1]} | |{c[3][1][0]}:{c[3][1][1]} | |\033[0;31m | Hits: {h}\t |\033[0;34m |██║░░╚═╝███████║██║░░╚═╝███████║█████╗░░ \t|\033[0m
\033[0;32m | Cache Size : 16 words  |\033[0;33m | |{c[0][2][0]}:{c[0][2][1]}\t| |{c[1][2][0]}:{c[1][2][1]} | |{c[2][2][0]}:{c[2][2][1]} | |{c[3][2][0]}:{c[3][2][1]} | |\033[0;31m | Miss: {m}\t |\033[0;34m |██║░░██╗██╔══██║██║░░██╗██╔══██║██╔══╝░░\t|\033[0m
\033[0;32m | Main Mem   : 64 words  |\033[0;33m | |{c[0][3][0]}:{c[0][3][1]}\t| |{c[1][3][0]}:{c[1][3][1]} | |{c[2][3][0]}:{c[2][3][1]} | |{c[3][3][0]}:{c[3][3][1]} | |\033[0;31m | Hit%: {hitrate}%\t |\033[0;34m |╚█████╔╝██║░░██║╚█████╔╝██║░░██║███████╗ \t|\033[0m
\033[0;32m | wPolicy: Write Through |\033[0;33m | |         | |         | |         | |         | |\033[0;31m | Mis%: {misrate}%\t |\033[0;34m |░╚════╝░╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝╚══════╝ \t|\033[0m
\033[0;32m |                        |\033[0;33m | +---------+ +---------+ +---------+ +---------+ |\033[0;31m |                |\033[0;34m | SIMULATOR          ~ by Arnab Bhattacharya |\033[0m
\033[0;32m +------------------------+\033[0;33m +-------------------------------------------------+\033[0;31m +----------------+\033[0;34m +--------------------------------------------+\033[0m
 +--- Main Memory ------------------------------------------------------------------------------------------------------------------------------+""")
    for i in range(0,64,8):
        print(" |",end='')
        print(f"{mem[i][0]}:{mem[i][1]}\t|{mem[i+1][0]}:{mem[i+1][1]}\t|{mem[i+2][0]}:{mem[i+2][1]}\t|{mem[i+3][0]}:{mem[i+3][1]}\t|{mem[i+4][0]}:{mem[i+4][1]}\t|{mem[i+5][0]}:{mem[i+5][1]}\t|{mem[i+6][0]}:{mem[i+6][1]}\t|{mem[i+7][0]}:{mem[i+7][1]}\t",end='')
        print(" \t\t| ")
    print(" +----------------------------------------------------------------------------------------------------------------------------------------------+")

def addr_input():
    global accesses
    global miss
    global hits
    addr_def = '00000'
    print(" +--- Interface --------------------------------------------------------------------------------------------------------------------------------+")
    print(" |")
    opt = int(input(" | Access Memory [0] Write Data [1] : "))
    if opt == 0:
        addr = int(input(" | Enter address (hex): "),16)
        accesses += 1
        addr = (addr_def + str(bin(addr))[2:])[-6:]
        blk_offset = int(addr[-2:],2)
        idx = int(addr[-4:-2],2)
        tag = addr[:-4]
        tagno = int(tag,2)
        # Initial Load...   

        if cache[idx][0][0] == '------':
            print(" | MISS - Loading Cache...")
            miss += 1
            start = (tagno*16) + (idx * 4)
            for i in range(4):
                cache[idx][i][0] = MainMem[start+i][0]
                cache[idx][i][1] = MainMem[start+i][1]
            slp(2)
        else:
            if cache[idx][blk_offset][0] == addr:
                print(" | HIT - Value: ",cache[idx][blk_offset][1])
                hits += 1
            else:
                print(" | MISS - Loading Cache...")
                miss += 1
                start = (tagno*16) + (idx * 4)
                for i in range(4):
                    cache[idx][i][0] = MainMem[start+i][0]
                    cache[idx][i][1] = MainMem[start+i][1]
            slp(2)
    elif opt == 1:
        addr = int(input(" | Enter address (hex): "),16)
        val = int(input(" | Value: "))
        accesses += 1
        addr = (addr_def + str(bin(addr))[2:])[-6:]
        blk_offset = int(addr[-2:],2)
        idx = int(addr[-4:-2],2)
        tag = addr[:-4]
        tagno = int(tag,2)
        if cache[idx][0][0] == '------':
            print(" | MISS - Loading Cache...")
            miss += 1
            start = (tagno*16) + (idx * 4)
            for i in range(4):
                cache[idx][i][0] = MainMem[start+i][0]
                cache[idx][i][1] = MainMem[start+i][1]
            cache[idx][blk_offset][1] = val
            MainMem[int(addr,2)][1] = val
            slp(2)
            print(" | Data written...")
            slp(2)
        else:
            if cache[idx][blk_offset][0] == addr:
                cache[idx][blk_offset][1] = val
                MainMem[int(addr,2)][1] = val
                print(" | HIT - Data written...")
                hits += 1
            else:
                print(" | MISS - Loading Cache...")
                miss += 1
                start = (tagno*16) + (idx * 4)
                for i in range(4):
                    cache[idx][i][0] = MainMem[start+i][0]
                    cache[idx][i][1] = MainMem[start+i][1]
                cache[idx][blk_offset][1] = val
                MainMem[int(addr,2)][1] = val
                slp(2)
                print(" | Data written...")
            slp(2)

def main():
    while True:
        cls()
        display(cache,accesses,hits,miss,MainMem)
        addr_input()

main()
