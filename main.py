import fileinput
import scapegoat
import skiplist


def mainSkipList():
    skiplisto = skiplist.SkipList(32);
    for line in fileinput.input():
        com = line.split();
        if com[0] == "D":
            result = skiplist.delete(skiplisto, com[1])
        if com[0] == "I":
            result = skiplist.insert(skiplisto, com[1], 0)
        if com[0] == "S":
            result = skiplist.Search(skiplisto, com[1])
        if result is None:
            print("F")
        else:
            print("S")
    return;


def mainScapegoat():
    tree = scapegoat.ScapeGoatTree();
    for line in fileinput.input():
        com = line.split();
        if com[0] == "I":
            result = tree.insert(com[1])
        if com[0] == "D":
            result = tree.deleteSGT(com[1])
        if com[0] == "S":
            result = tree.search(com[1])
        
        if result is None:
            print("F")
        else:
            print("S")
    return;


for line in fileinput.input():
    if line == "p\n":
        fileinput.close();
        mainSkipList();
        break;
    elif line == "a\n":
        fileinput.close();
        mainScapegoat();
        break;