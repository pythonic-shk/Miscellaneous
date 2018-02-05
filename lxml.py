from lxml import etree
idmfTree = etree.parse('C:/AMOTOR_DP/IDMF.txt')
idmfRoot = idmfTree.getroot()
tree = etree.ElementTree(idmfRoot)
result = idmfRoot.findall('.//FirstName')
print(result)
for r in result:
    print(tree.getpath(r))