import scapegoat
import random
import numpy

tree = scapegoat.ScapeGoatTree();
k = 0;
inserted = [];
while k < 2:
    i = 0;
    while i < 2:
        r = random.randint(0, 10000)
        print(r);
        if tree.insert(r) is not None:
            inserted.append(r);
        i = i + 1
    i = 0;
    while i < 2:
        c = random.choice(inserted);
        tree.search(c);
        i = i + 1
    xAverage = numpy.average(scapegoat.searchS);
    yAverage = numpy.max(scapegoat.searchN);
    
    scapegoat.searchN = []
    scapegoat.searchS = []

    scapegoat.averageN.append(yAverage);
    scapegoat.averageS.append(len(inserted));
    k = k + 1
print(tree.size);
print(len(inserted))
scapegoat.plottree();