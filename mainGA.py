# import
import random
import math

# d2b function (require math)
def d2b(*arg):
	"""This function returns binary value of the entered number"""
	# get input
	inDec=arg[0]


	# get minimum output length
	if inDec==0:
		outLenMin=1
	else:
		logFloor=math.floor(math.log(inDec,2))
		outLenMin=max(0,logFloor)+1

	# get output length
	inputNumber=len(arg)
	if inputNumber==1:
		outLen=outLenMin
	elif inputNumber==2:
		outLenDet=arg[1]
		outLen=max(outLenMin,outLenDet)
		if outLenDet<outLenMin:
			print('Determined Binnary Size Is Smaller Than Output Binnary Size')
	
	# initialize 
	shift=outLen-outLenMin
	outBin=[None]*outLen

	# compute outBin
	for i in range(0,outLen):
		r=math.floor(inDec/2)
		outBin[shift+outLenMin-1-i]=inDec-2*r
		inDec=r

	return(outBin)

# b2d function
def b2d(inBin):
	"""This function returns decimal value of the entered number"""
	#
	outDec=0
	inLen=len(inBin)

	#
	inBinRev=(inBin[::-1])
	
	#
	for i in range(inLen):
		if inBinRev[i]==1:
			outDec=outDec+2**i	

	return(outDec)

# getKeySecond
def getKeySecond(item):
	return item[1]

# def doInitialPopulation
def doInitialPopulation(numberOfPop,lowerBound,upperBound):
	population=[None]*numberOfPop
	for i in range(numberOfPop):
		population[i]=random.randint(lowerBound, upperBound)
	return(population)

# def doFitness
def doFitness(population,numberOfPop):
	fitness=[None]*numberOfPop
	record=[None]*numberOfPop
	[a,b,c]=equationVariable()
	for i in range(numberOfPop):
		fitness[i]=[a*population[i]**2+b*population[i]+c]
		record[i]=[population[i]]+fitness[i]
	return(fitness,record)

# def doElitism
def doElitism(*arg):
	record=arg[0]
	numberOfPop=arg[1]
	population=[None]*numberOfPop
	fitness=[None]*numberOfPop
	elitismInput=len(arg)
	if elitismInput==2: #initialElitism
		record=sorted(record,key=getKeySecond,reverse=True)
		for i in range(numberOfPop): 
			population[i]=record[i][0] #trivial
			fitness[i]=record[i][1] #trivial
	elif elitismInput==3: #globalElitism
		children=arg[2]
		fourBottom=[None]*4
		fourBottom[:2]=record[-2:]
		fourBottom[2:]=children
		fourBottom=sorted(fourBottom,key=getKeySecond,reverse=True)
		record[-2:]=fourBottom[:2]
		record=sorted(record,key=getKeySecond,reverse=True)
		for i in range(numberOfPop): 
			population[i]=record[i][0] #trivial
			fitness[i]=record[i][1] #trivial 
	return(population,fitness,record)

# def doRouletteWheel
def doRouletteWheel(population,fitness,numberOfPop): 
	"""this code is a modification of standard roulette wheel and only work for 
	maximazing objective function"""
	fitnessMin=fitness[-1] #min(fitness)
	fitnessTotal=sum(fitness)
	parent=[None]*2
	probInd=[None]*numberOfPop
	probCum=[None]*numberOfPop
	probCumTemp=1
	# probInd
	if (fitnessTotal-fitnessMin*numberOfPop)==0:
		probInd=[1/numberOfPop]*numberOfPop
	else:
		for i in range(numberOfPop):
				probInd[numberOfPop-1-i]=((fitness[numberOfPop-1-i]-fitnessMin)/
																(fitnessTotal-fitnessMin*numberOfPop))
	# probCum
	for i in range(numberOfPop):
		if i==0:
			probCum[-1]=1
		else:
			probCumTemp=probCumTemp-probInd[numberOfPop-i]
			probCum[numberOfPop-1-i]=probCumTemp
	# spin
	for i in range (2):
		rouletteValue=random.random()
		k=0
		while (True):
			if rouletteValue<probCum[k]:
				parent[i]=population[k]
				break
			else:
				k=k+1
	return(parent)

# def doCrossover
def doCrossover(parent,binaryMax):
	children=[None]*2
	for k in range(2):
		parent[k]=d2b(parent[k],binaryMax)
	cutLocation=random.randint(1,binaryMax-1)
	children[0]=parent[0][0:cutLocation]+parent[1][cutLocation:]
	children[1]=parent[1][0:cutLocation]+parent[0][cutLocation:]
	for k in range(2):
		children[k]=b2d(children[k])
	return children

# def doMutation
def doMutation(children,mutationRate,binaryMax):
	numberOfMember=len(children)
	for k in range(numberOfMember):
		mutationValue=random.random()
		print(mutationValue)
		if mutationValue<=mutationRate:
			children[k]=d2b(children[k],binaryMax)
			mutationLocation=random.randint(0,binaryMax-1)
			if children[k][mutationLocation]==1:
				children[k][mutationLocation]=0
			else:
				children[k][mutationLocation]=1
			children[k]=b2d(children[k])
	return(children)

#def doFilter
def doFilter(children,lowerBound,upperBound,globalPopulation,binaryMax):
	for k in range(2):
		while(True):
			if children[k] < lowerBound:
				children[k]=lowerBound
			if children[k] > upperBound:
				children[k]=upperBound
			if children[k] in globalPopulation:
				childrenTemp=doMutation([children[k]],1,binaryMax) #mutationRate=1
				children[k]=childrenTemp[0]
			if 	children[k] >= lowerBound and children[k] <= upperBound and not(children[k] in globalPopulation):
				break
	return(children)

#def equationVariable
def equationVariable():
	a=-0.001
	b=0.05
	c=10
	return[a,b,c]

if __name__ == '__main__':
    # set parameters
    numberOfPop=10
    lowerBound=0
    upperBound=100
    binaryMax=len(d2b(upperBound))
    generationMax=10
    mutationRate=0.8
    population=[None]*numberOfPop
    fitness=[None]*numberOfPop
    record=[None]*numberOfPop
    parent=[None]*2
    children=[None]*2

    # initial population
    population=doInitialPopulation(numberOfPop,lowerBound,upperBound)
    globalPopulation=population
    print(population)

    # fitness
    [fitness,record]=doFitness(population,numberOfPop)
    globalFitness=[r[1] for r in record]
    print(fitness)
    print(record)

    # elitism
    [population,fitness,record]=doElitism(record,numberOfPop)
    print(population)
    print(fitness)
    print(record)

    for i in range(generationMax):
        print('Generation: ',i)
        # parentSelection	 
        parent=doRouletteWheel(population,fitness,numberOfPop)
        print('The parents: ', parent)

        # crossover
        children=doCrossover(parent,binaryMax)
        print('The Children: ',children)

        # mutation
        children=doMutation(children,mutationRate,binaryMax)
        print('The Mutated Children: ',children)

        # filter (if children is element of globalPopulation, mutate)
        # filter (if children is outOfbound, setTobound)
        children=doFilter(children,lowerBound,upperBound,globalPopulation,binaryMax)
        print('The Filtered Children: ',children)

        # globalPopulation
        globalPopulation=globalPopulation+children

        # fitness
        _,children=doFitness(children,2)
        print(children)
        childrenFitness=[r[1] for r in children]
        globalFitness=globalFitness+childrenFitness

        # elitism
        [population,fitness,record]=doElitism(record,numberOfPop,children)
        print(population)
        print(fitness)
        print(record)

    print('globalPopulation: \n',globalPopulation)
    print('sortedGlobalPopulation: \n',sorted(globalPopulation))
