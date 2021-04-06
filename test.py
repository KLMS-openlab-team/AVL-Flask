def search(self, root, bookname):
        if not root:
            return False
        if root.bookname.startswith(bookname):
            self.searchNode(root,bookname,[])
        elif bookname < root.val:
            root.left = self.search(root.left, bookname)
        elif bookname > root.val:
            root.right = self.search(root.right, bookname)
        else:
            return root

def searchNode(self,root,bookname, searchOutput):
    if root==None:
        return False
    if root.bookname.startswith(bookname):
        searchOutput.append(root)
    self.searchNode(root.left,bookname,searchOutput)
    self.searchNode(root.right,bookname,searchOutput)
