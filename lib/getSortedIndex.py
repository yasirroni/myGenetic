def getSortedIndex(inp):
    sortedEnum=sorted(enumerate(inp),key=lambda x: x[1])
    idx=[i[0] for i in sortedEnum]
    val=[i[1] for i in sortedEnum]
    return val,idx

def arangeByIndex(inp,idx):
    result=[inp[x] for x in idx]
    return result
