import numpy as np
import csv
import os
import matplotlib.pyplot as plt

NUM_REQUEST = 5
UNIQUE_PAGES = 300
PHASE_SHIFTS = 1000
RANDOMIZATION_RATE = 0.25
CACHE_SIZE = 300
PROB_USED = 0.8
DECAY_RATE = 0.99

HARD_PHASE_SHIFT = NUM_REQUEST/2
# LRU_PROB = 0.9

Q = list()
F = {}
time = 0
np.random.seed(123)
## Choose page using a uniform distribution
def Random():
    return np.random.randint(0, UNIQUE_PAGES)



## Choose page using LRU distribution
def LRU():
    n = min(CACHE_SIZE, len(F))
    L = []
    for i,pg in enumerate(Q[::-1]) :
        if i >= n :
            break
        L.append(pg)
    return L[np.random.randint(0, n)]

## Choose page using LFU distribution
def LFU():
    n = min(CACHE_SIZE, len(F))
    L = []
    for key in F :
        L.append((-F[key], key))
    L.sort()
    Q = []
    for i,pg in enumerate(L):
        if i >= n :
            break
        Q.append(pg[1])
    return Q[np.random.randint(0, n)]

def update(page):
    Q.append(page)
    if page not in F :
        F[page] = 0
    for pg in F :
        F[pg] *= DECAY_RATE
    F[page] += 1

def ContiguousBolock(output_writer):
    blocks= [i for i in range(0, UNIQUE_PAGES)]
    for block in blocks:
        update(block)
       
    # print(blocks)
    return blocks

def SlicesofContiguousBolock(output_writer):
    a= np.random.randint(0, UNIQUE_PAGES)
    b =np.random.randint(0, UNIQUE_PAGES)
    blocks =  [i for i in range(0, UNIQUE_PAGES)]
    pages = blocks[a:b]
    for block in pages:
        update(block)
        
    # print(blocks)
    return pages
def generate_churn(RepeatedScan):
    pages = []
    pages = pages + ContiguousBolock(output_writer)
    if RepeatedScan:
        pages = pages + ContiguousBolock(output_writer)
        pages = pages + ContiguousBolock(output_writer)
        pages = pages + ContiguousBolock(output_writer)
        pages = pages + ContiguousBolock(output_writer)
    
    else:
        pages = pages + SlicesofContiguousBolock(output_writer)
    
        for i in range(50):
            q = Random()
            pages.append(q)
            update(q)
           
        
        pages= pages+ SlicesofContiguousBolock(output_writer)
        pages= pages+ SlicesofContiguousBolock(output_writer)
        pages = pages + ContiguousBolock(output_writer)
        print(LRU())
        for i in range(20):
            q = LRU()
            pages.append(q)
            update(q)
           
        
        pages= pages+ SlicesofContiguousBolock(output_writer)
        pages = pages +SlicesofContiguousBolock(output_writer)
        for i in range(20):
            q = LFU()
            pages.append(q)
            update(q)
           

        pages= pages+ SlicesofContiguousBolock(output_writer)
        # pages = pages + blocks
        pages= pages+ SlicesofContiguousBolock(output_writer)
        pages = pages + ContiguousBolock(output_writer)
    return pages

def generate_scan() :
    pages = []
    blocks = []

    # for i in range(25):
    #     q = np.random.randint(2*UNIQUE_PAGES//3, UNIQUE_PAGES)
    #     pages.append(q)
    #     update(q)
    for i in range(50):
        q = np.random.randint(0, UNIQUE_PAGES//3)
        pages.append(q)
        update(q)

    for i in range(280):
        q =  LFU()
        pages.append(q)
        update(q)
        blocks.append(q)
  
    new_blocks =  [i for i in range(0, UNIQUE_PAGES)]
    scans = new_blocks[100:240]
    for scan in scans:
        pages.append(scan)
        update(scan)

    for i in range(260):

        q = np.random.randint(0, UNIQUE_PAGES)
        pages.append(q)
        update(q)

    for q in blocks :
       
        pages.append(q)
        update(q)
    # for q in blocks :
       
    #     pages.append(q)
    #     update(q)

    for i in range(280):
        q = np.random.randint(0, UNIQUE_PAGES)
        pages.append(q)
        update(q)
       
    
    
    return pages

 
class CacheSyntheticPlugin:
 def input(self, inputfile):
    pass
 def run(self):
    pass
 def output(self, outputfile):
    phase = 1
    epsilon = 0.25
    pages=[]
    RepeatedScan = 0
    SingleScan = True
    filename = "SingleScan" if SingleScan else ("RepeatedScan" if RepeatedScan else "MixedScan")
    filename= filename+"_lfu"
    out_file= outputfile+"/" +filename+"_"+ str(NUM_REQUEST) + "_"+ str(CACHE_SIZE) + ".trc"
    
    with open(out_file, mode='w') as output_file:
        output_writer = csv.writer(output_file, delimiter='\n', quotechar='"', quoting=csv.QUOTE_MINIMAL)

      
        if SingleScan:
            pages= generate_scan()
        else:
            pages = generate_churn(RepeatedScan)

        for page in pages:
            output_writer.writerow([page])

        

    print("Finishd")
    print(len(set(pages)))
    
    #folder_name= os.getcwd()+"/Converted_Patterns"
    #if not os.path.exists(folder_name):
    #    os.makedirs(""+folder_name)
    plt.figure(figsize=(8,8))
    # print(range(len(pages)))
    plt.plot(range(len(pages)),pages, 'y.',  linewidth=1)
    plt.ylabel('Block Address')
    plt.xlabel('Time')
                            
    plt.tight_layout()
    # plt.subplots_adjust(hspace = 0.2)
    # plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    # lgd=ax_hitrate.legend(fancybox=True, framealpha=0.5, loc="upper left", ncol=5)
   
    plt.savefig("%s/%s_%s_%s_%s.png" % (outputfile, filename, NUM_REQUEST, UNIQUE_PAGES ,CACHE_SIZE,))
    plt.clf()
        
        
