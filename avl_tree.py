class TreeNode(object):
    def __init__(self, bookname,count,price,active,description):
        self.bookname = bookname
        self.count = count
        self.price = price
        self.active = active
        self.description = description
        self.left = None
        self.right = None
        self.height = 1


class AVL_Tree(object):
    def insert(self, root, bookname,count,price,active,description):

        if not root:
            return TreeNode(bookname,count,price,active,description)
        elif bookname < root.bookname:
            root.left = self.insert(root.left, bookname,count,price,active,description)
        else:
            root.right = self.insert(root.right, bookname,count,price,active,description)

        root.height = 1 + max(self.getHeight(root.left),
                              self.getHeight(root.right))

        balance = self.getBalance(root)

       
        if balance > 1 and bookname < root.left.bookname:
            return self.rightRotate(root)

        if balance < -1 and bookname > root.right.bookname:
            return self.leftRotate(root)

        if balance > 1 and bookname > root.left.bookname:
            root.left = self.leftRotate(root.left)
            return self.rightRotate(root)

        if balance < -1 and bookname < root.right.bookname:
            root.right = self.rightRotate(root.right)
            return self.leftRotate(root)

        return root

    def leftRotate(self, z):

        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        z.height = 1 + max(self.getHeight(z.left),
                           self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left),
                           self.getHeight(y.right))

        return y

    def rightRotate(self, z):

        y = z.left
        T3 = y.right

        y.right = z
        z.left = T3

        z.height = 1 + max(self.getHeight(z.left),
                           self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left),
                           self.getHeight(y.right))

        return y

    def getHeight(self, root):
        if not root:
            return 0

        return root.height

    def getBalance(self, root):
        if not root:
            return 0

        return self.getHeight(root.left) - self.getHeight(root.right)

    def Inorder(self, root, searchResult):

        if not root:
            return

        self.Inorder(root.left,searchResult)
        searchResult.append((root.bookname,root.count,root.price,root.active,root.description))
        self.Inorder(root.right,searchResult)

    def delete(self, root, key):
  
        if not root:
            return root
  
        elif key < root.bookname:
            root.left = self.delete(root.left, key)
  
        elif key > root.bookname:
            root.right = self.delete(root.right, key)
  
        else:
            if root.left is None:
                temp = root.right
                root = None
                return temp
  
            elif root.right is None:
                temp = root.left
                root = None
                return temp
  
            temp = self.getMinValueNode(root.right)
            root.bookname = temp.bookname
            root.right = self.delete(root.right,
                                      temp.bookname)
  
        if root is None:
            return root
  
        root.height = 1 + max(self.getHeight(root.left),
                            self.getHeight(root.right))
  
        balance = self.getBalance(root)
  
        if balance > 1 and self.getBalance(root.left) >= 0:
            return self.rightRotate(root)
  
        if balance < -1 and self.getBalance(root.right) <= 0:
            return self.leftRotate(root)
  
        if balance > 1 and self.getBalance(root.left) < 0:
            root.left = self.leftRotate(root.left)
            return self.rightRotate(root)
  
        if balance < -1 and self.getBalance(root.right) > 0:
            root.right = self.rightRotate(root.right)
            return self.leftRotate(root)
  
        return root

    def getMinValueNode(self, root):
        if root is None or root.left is None:
            return root
        return self.getMinValueNode(root.left)

    def searchNode(self,root,bookname, searchOutput):
        if root==None:
            return False
        if root.bookname.startswith(bookname):
            searchOutput.append(root)
        self.searchNode(root.left,bookname,searchOutput)
        self.searchNode(root.right,bookname,searchOutput)
    

    def updateNode(self,root,bookname,count,price,active,description):
        if root==None:
            return False
        if root.bookname==bookname:
            root.count=count
            root.price=price
            root.active=active
            root.description=description
            return True
        return self.searchNode(root.left,bookname,count,price,active,description) or self.searchNode(root.right,bookname,count,price,active,description)

# myTree = AVL_Tree()
# root = None
# root = myTree.insert(root, "Harry Potter",10,200,1,"A book about wizards")
# root = myTree.insert(root, "Prisoner",10,200,1,"A book about how a prisoner lives")
# root = myTree.insert(root, "Beach",10,200,1,"Book on beaches")
# root = myTree.insert(root, "Magic",10,200,1,"Spell book")
# root = myTree.insert(root, "Haufmann",10,200,1,"Algorithm based")
# root = myTree.insert(root, "Legend",10,200,1,"A nice book")

# op = []
# myTree.searchNode(root, "Har",op)
# for i in op:
#     print(i.bookname)
# myTree.updateNode(root, "Haufmann",10,200,1,"Algorithm")
# myTree.Inorder(root)
# print()