import math;
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import numpy
comparisons = 0;
import fileinput;
import time;
searchN = []
searchS = []
averageN = []
averageS = []

def plottree():
  y = searchN;
  x = searchS;
  plt.xlabel("number of objects");
  plt.ylabel("number of comparisons");
  plt.plot(averageS, averageN, "o");
  plt.tight_layout()
  plt.show();
  plt.savefig("comparisons");
  #xnp = numpy.array(x);
  #ynp = numpy.array(y);
  #m, b = numpy.polyfit(xnp, ynp, 1);
  #plt.plot(xnp, m*xnp + b);
  #plt.show();
  #plt.savefig("comparisons tree regress");


class ScapeGoatTree:
  
  def __init__(self):
    self.root = None;
    self.size = 0;
    self.maxsize = 0;
    self.a = 0.70;  
  
  class node:
    def __init__(self, key, parent):
      self.key = key;
      self.left = None;
      self.right = None;
      self.parent = parent;
  
  def getSize(self, node):
    if node is None:
      return 0;
    else:
      return self.getSize(node.left) + self.getSize(node.right) + 1;
  
  def brother(self, node):
    if node.parent.right is not node:
      return node.parent.right;
    else:
      return node.parent.left;

  def search(self, key):
    comparisons = 0;
    node = self.root;
    while node is not None:
      if node.key == key:
        comparisons = comparisons + 1;
        searchN.append(comparisons);
        searchS.append(self.size);
        comparisons = 0;
        return node;
      elif node.key > key:
        comparisons = comparisons + 1;
        node = node.left;
      else:
        comparisons = comparisons + 1;
        node = node.right;
    searchN.append(comparisons);
    searchS.append(self.size);
    comparisons = 0;
    return None;

  def nodeHeight(self, node):
    if node is None:
      return 0;
    else:
      return max(self.nodeHeight(node.left), self.nodeHeight(node.right)) + 1;
  
  def treeHeight(self, tree):
    return self.nodeHeight(tree.root);

#maybe account for foreign node
  def depth(self, node):
    depth = 0;
    while node is not self.root:
      depth = depth + 1;
      node = node.parent;
    return depth;

  def aWeightBalanced(self, node):
    nodeSize = self.getSize(node);
    if self.getSize(node.left) > self.a * nodeSize or self.getSize(node.right) > self.a * nodeSize:
      return False;
    else:
      return True;
  
  def h_a(self, n):
    if n == 0:
      return 0;
    return int(math.log(self.size(n), int(1/self.a)));

  def aHeightBalanced(self, node):
    if self.nodeHeight(node) > self.h_a(node):
      return False;
    else:
      return True;
    
  def Flatten(self, x, y):
    if x is None:
      y.left = None;
      return y;
    x.right = self.Flatten(x.right, y);
    return self.Flatten(x.left, x);

  def altFlatten(self, x, y):
    if x is None:
      return y;
    x.right = self.altFlatten(x.right, y);
    return self.altFlatten(x.left, x);

  def BuildTree(self, n, x):
    if n == 0:
      x.left = None;
      return x;
    r = self.BuildTree(math.ceil((n-1)/2), x);
    s = self.BuildTree(math.floor((n-1)/2), r.right);
    r.right = s.left;
    s.left = r;
    return s;


  def printtree(self, node):
    if node is not None:
      self.printtree(node.left);
      #print(node.key);
      self.printtree(node.right);

  def Rebuilt(self, n, scapegoat):
    w = self.node(10000, None);
    #self.printtree(scapegoat);
    #print("flatten");
    z = self.Flatten(scapegoat, w);
    l = z;
    #self.printtree(z);
    #print("Buildtree");
    self.BuildTree(n, z);
    #self.printtree(w.left);
    #print("Doen rebuild");
    return w.left;

  def fixParent(self, node, parent):  
    if node is not None: 
      if parent is not None:
        node.parent = parent;
      self.fixParent(node.left, node);
      self.fixParent(node.right, node);

  def insert(self, key):
    comparisons = 0;
    cNode = self.root;
    notDone = True;

    if self.root is None:
      self.root = self.node(key, None);
      self.size = self.size + 1;
      self.maxsize = max(self.maxsize, self.size);
      return self.root;

    while notDone:
      if cNode.key == key:
        comparisons = comparisons + 1;
        return None;
      elif cNode.key > key:
        comparisons = comparisons + 1;
        if cNode.left is None:
          cNode.left = self.node(key, cNode);
          notDone = False;
          cNode = cNode.left;
        else:
          cNode = cNode.left;
      elif cNode.key < key:
        comparisons = comparisons + 1;
        if cNode.right is None:
          cNode.right = self.node(key, cNode);
          notDone = False;
          cNode = cNode.right;
        else:
          cNode = cNode.right;
    self.size = self.size + 1;
    self.maxsize = max(self.maxsize, self.size);

    iNode = cNode
    while cNode is not None:
      if self.aWeightBalanced(cNode) is not True:
        parent = cNode.parent;
        cNode = self.Rebuilt(self.getSize(cNode), cNode);
        
        if parent is not None:
          if(parent.key < cNode.key):
            parent.right = cNode;
            cNode.parent = parent;
          else:
            parent.left = cNode;
            cNode.parent = parent;
        else:
          self.root = cNode;
          cNode.parent = None;
        self.fixParent(cNode.left, cNode);
        self.fixParent(cNode.right, cNode);
        break;
      cNode = cNode.parent;
    
    comparisons = 0;
    return iNode;

  def deleteSGT(self, key):
    comparisons = 0;
    size = self.size;
    self.root = self.delete(self.root, key);
    if self.root is not None:
      if self.size < self.a * self.maxsize:
        self.root = self.Rebuilt(self.size, self.root);
    comparisons = 0;
    if size == self.size:
      return None;
    else:
      return 1;
    

  def delete(self, root, key):
    if root is None:
      return None;
    elif root.key > key:
      comparisons = comparisons + 1;
      root.left = self.delete(root.left, key);
    elif root.key < key:
      comparisons = comparisons + 1;
      root.right = self.delete(root.right, key);
    else:
      if root == self.root and root.left is None and root.right is None:
        root = None;
      else:
        if root.left is None:
          self.size = self.size - 1;
          root.right.parent = root.parent;
          return root.right;
        elif root.right is None:
          self.size = self.size - 1;
          root.left.parent = root.parent;
          return root.left;
      
        temp = root.right;
        while temp.left is not None:
          temp = temp.left;
        root.key = temp.key;
        root.right = self.delete(root.right, temp.key);
      self.size = self.size - 1;
    return root;
