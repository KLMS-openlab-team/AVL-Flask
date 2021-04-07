# def search(self, root, bookname):
#         if not root:
#             return False
#         if root.bookname.startswith(bookname):
#             self.searchNode(root,bookname,[])
#         elif bookname < root.val:
#             root.left = self.search(root.left, bookname)
#         elif bookname > root.val:
#             root.right = self.search(root.right, bookname)
#         else:
#             return root

# def searchNode(self,root,bookname, searchOutput):
#     if root==None:
#         return False
#     if root.bookname.startswith(bookname):
#         searchOutput.append(root)
#     self.searchNode(root.left,bookname,searchOutput)
#     self.searchNode(root.right,bookname,searchOutput)
# from configparser import ConfigParser
# config = ConfigParser()

# config.read('config.ini')
# print(config.get('main','host'))
from datetime import datetime
print(datetime.now())
print(datetime.fromisoformat('2021-04-07T05:59:12.457031'))
print(datetime('{}'.format(datetime.now())))
