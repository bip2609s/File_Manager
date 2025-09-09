import os
import sys
import pickle
class decart_tree_node:
    def __init__(self, name, path, size):
        self.name=name
        self.path=path
        self.size=size
        self.right_child=0
        self.left_child=0
def merge(l, r):
    if not l:
        return r
    if not r:
        return l
    if l.size>r.size:
        l.right_child=merge(l.right_child, r)
        return l
    else:
        r.left_child=merge(l, r.left_child)
        return r
def split(p, x):
    if not p:
        return [0, 0]
    if p.name<=x:
        q=split(p.right_child, x)
        p.right_child=q[0]
        return p, q[1]
    else:
        q=split(p.left_child, x)
        p.left_child=q[1]
        return q[0],p

def insert(root, el):
    if root==0:
        root=el
    else:
        q=split(root, el.name)
        root=merge(q[0], merge(el, q[1]))
    return root
def analyse(folder):
    file_index = {}
    decart_tree=0
    for root, _, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)
            file_index[file] = (file_path, os.path.getsize(file_path))
    for i in file_index:
        decart_tree=insert(decart_tree, decart_tree_node(i, file_index[i][0], file_index[i][1]))
    with open("data_in_heap.pickle", "wb") as f:
        pickle.dump(decart_tree, f)
    print("The data is saved to data_in_heap.pickle")
def search(file_name):
    with open("data_in_heap.pickle", "rb") as f:
        decart_tree = pickle.load(f)
    flag=0
    i=decart_tree
    while i!=0:
        if file_name==i.name:
            file_path, file_size = i.path, i.size
            print(f"File root is {file_path}")
            print(f"File size is {file_size} bytes")
            flag=1
            break
        elif i.name<file_name:
            i=i.right_child
        elif i.name>file_name:
            i=i.left_child
    if flag==0:
        print("No such file has been found")

cmd_argument = sys.argv[1]
if cmd_argument == "analyse":
    folder = sys.argv[2]
    analyse(folder)
elif cmd_argument == "search":
    file_name = sys.argv[2]
    search(file_name)
else:
    print("Invalid command")