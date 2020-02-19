# The Devil's Dungeon in Python
# Try 6 (think more Python, less BASIC)
# Possibly fixed big problem with contentFlags[]. Mostly works now.

import random	# for random numbers

# Initialize global variables (and think of ways to use less globals)

roomContents=[0]	#R() 0-15
roomFlags=[0]		#F() 0-15
visitedRooms=[0]	#B() 0-15
for loop in range(1,16+1):
	roomContents.append(0.0)
	roomFlags.append(0)
	visitedRooms.append(0)
adjacentRooms=[0]	#L() 0-64
for loop in range(1,65+1):
	adjacentRooms.append(0)
contentFlags=[0.0]	#X() 0-18
for loop in range(1,19+1):
	contentFlags.append(float(0))
pLocation=1			# Player location, starts in room 1
pGold=0				# Player gold
pExp=0				# Player experience points
numberRooms=16		# Number of rooms on a level
depth=1				# Dungeon level player is on
oldDepth=0			# The old level, used for flow control
pStrength=101		# Player strength
pSpeed=101			# Player speed
monsterPresent=0	# Flag for a monster in same room
mStrength=0			# Monster strength
mSpeed=0			# Monster speed
slide=0				# Not sure what this is
treasure=0			# Not 100% sure about this, either
debug=False
#debug=True
################################ End of global variables

def setRooms():	# Set up rooms when game starts and level changes
	if debug:
		print("Setting Rooms")
	r=1
	for loop in range(0,64+1):
		adjacentRooms[loop]=0
	for loop in range(1,numberRooms+1):
		n=int(3*rnd()+1)
		if loop==1:
			n=3
		for j in range(1,n+1):
			while adjacentRooms[r]<>0:
				r=int(64*rnd()+1)
			adjacentRooms[r]=loop
		roomContents[loop]=int(524287*rnd())
		visitedRooms[loop]=0
	visitedRooms[pLocation]=1
	roomContents[1]=24576
	for i in range(1,18+1):
		contentFlags[i]=float(0)
	return
	
def checkHazards():
	global pSpeed
	global pStrength
	
	if rnd()<.01:
		print("Tremor!")
		for i in range(1,20+1):
			adjacentRooms[i]=int(numberRooms*rnd()+1)
	if rnd()<.01:
		print("Tremor!")
		for i in range(1,20+1):
			adjacentRooms[i]=0
	if contentFlags[1]*contentFlags[12]==1 and rnd()<.4:
		print("Cursed by a demon!")
		pSpeed=int(.5*pSpeed)
	if contentFlags[9]*contentFlags[11]==1 and rnd()<.4:
		print("Gassed!")
		pStrength=int(.5*pStrength)
	return

def doAttrition():
	global pSpeed
	global pStrength
	pSpeed=pSpeed-1
	pStrength=pStrength-1
	if pSpeed<=0 or pStrength<=0:
		print("You have died!")
		quit()
	return
	
def rnd():
	return random.random()

def showStatus():
	print("-=-=-=-=-=-=-=-=-=-=")
	print("Gold: "+str(pGold)+" Experience: "+str(pExp)+" Depth: "+str(depth))
	print("Speed: "+str(pSpeed)+" Strength: "+str(pStrength))
	print("-=-=-=-=-=-=-=-=-=-=")
	doAdjacentRooms()	
	doConvert()
	return

def doAdjacentRooms():
	for i in range(1,numberRooms+1):
		roomFlags[i]=0
	for i in range(1,64+1):
		if pLocation<>adjacentRooms[i]:
			continue
		if adjacentRooms[i+1]<>0 and adjacentRooms[i+1]<>pLocation:
			roomFlags[adjacentRooms[i+1]]=1
		if adjacentRooms[i-1]<>0 and adjacentRooms[i-1]<>pLocation:
			roomFlags[adjacentRooms[i-1]]=1
	return

def doConvert():
	n=roomContents[pLocation]
	if debug:
		print("Room contents= "+str(n))
	for i in range(1,19+1):
		q=int(n/2)
		contentFlags[i]=n % 2
		n=q
	return

def monstersDemonsGas():
	global mStrength
	global monsterPresent
	global mSpeed
	global pLocation
	global contentFlags
	
	if contentFlags[2]==0:
		monsterStrength=0
		demonsGas()
		return
	if monsterPresent==1:
		monsterStatus()
		demonsGas()
		return
	mStrength=depth*(contentFlags[3]+2*contentFlags[4]+4*contentFlags[5]+pLocation)
	mSpeed=depth*(contentFlags[6]+2*contentFlags[7]+4*contentFlags[8]+pLocation)
	monsterStatus()
	demonsGas()
	return
	
def demonsGas():
	if contentFlags[1]*contentFlags[12]==1:
		print("Demons")
	if contentFlags[9]*contentFlags[11]==1:
		print("Poisonous Gas")
	return
	
def monsterStatus():
	print("Monster's speed: "+str(mSpeed)+" Strength: "+str(mStrength))
	return
	
def maxTreasure():
	global treasure
	
	if contentFlags[10]<>1:
		treasure=0
		return
	treasure=contentFlags[11]+2*contentFlags[12]+4*contentFlags[13]+1
	print("Maximum Gold: "+str(treasure*pLocation*depth+1))
	if debug:
		print("Treasure = "+str(treasure))
	return

def slideDropoffs():
	global slide
	global contentFlags
	global numberRooms
	
	slide=contentFlags[15]+2*contentFlags[16]+4*contentFlags[17]+8*contentFlags[18]+1
	if slide>numberRooms:
		slide=1
	if slide==0:
		slide=1
	if contentFlags[14]<>0 and slide<>pLocation:
		print("You can slide to: "+str(slide))
	if contentFlags[19]*contentFlags[13]==1:
		print("There is a dropoff here.")
	return
	
def inputMove():
	print("Move from "+str(pLocation)+" to: ")
	for i in range(1,numberRooms+1):
		if roomFlags[i]==1 and i<>pLocation:
			print i,
	print(" ")
	print("Enter 88 for a list of visited rooms.")
	if pLocation == 1:
		print("Enter 99 to leave The Devil's Dungeon. Enter 0 to spend Experience Points.")
	else:
		print("Enter 99 to use your wand.")
	m=input("Your Move --> ")
	return(m)

def printRooms():
	global pLocation
	
	oldLocation=pLocation
	for k in range(1,numberRooms+1):
		if visitedRooms[k]<>1:
			continue
		print(str(k)+"--")
		pLocation=k
		doAdjacentRooms()
		for j in range(1,numberRooms+1):
			if roomFlags[j]==1 and j<>k:
				print j,
		print(" ")
		pLocation=oldLocation
	return

def leaveGame():
	print("You found "+str(pGold)+" pieces of gold.")
	print("You made it to level "+str(depth))
	quit()

def doTrade():
	global pSpeed
	global pStrength
	global pExp
	
	c=False
	print("Experience: "+str(pExp)+" Speed: "+str(pSpeed)+" Strength: "+str(pStrength))
	while c==False:
		n=input("Add speed: ")
		if (pExp-n)<0:
			print("You need more experience.")
		else:
			pExp=pExp-n
			pSpeed=pSpeed+n
			print("Experience left: "+str(pExp))
			c=True
	c=False
	while c==False:
		n=input("Add Strength: ")
		if (pExp-n)<0:
			print("You need mor experience.")
		else:
			pExp=pExp-n
			pStrength=pStrength+n
			c=True
	return

def useWand():
	global pSpeed
	global pStrength
	
	if rnd()<.4:
		print("The wand backfires!")
		pStrength=int(.5*pStrength)
		pSpeed=int(.5*pSpeed)
	else:
		print("The wand worked!")
		roomContents[pLocation]=266240
	return

def getTreasure():
	global pGold
	global pExp
	
	if treasure==0:
		return
	roomGold=int(rnd()*treasure*pLocation*depth)+1
	if contentFlags[1]*contentFlags[12]==1 and rnd()<.4:
		print("A demon got your gold!")
		roomGold=0
	else:
		print("You found "+str(roomGold)+" pieces of gold!")
		pGold=pGold+roomGold
		roomContents[pLocation]=roomContents[pLocation]-512
	pExp=pExp+roomGold
	return
	
def fight():
	global monsterPresent
	global mStrength
	global mSpeed
	global pStrength
	global pSpeed
	global roomContents
	global pExp
	
	pHit=0
	mHit=0
	
	monsterPresent=1
	# it checks for running here
	pHit=int(rnd()*pStrength)
	mHit=int(rnd()*mStrength)
	if pHit>mStrength:
		pHit=mStrength
	if mHit>pStrength:
		mHit=pStrength
	if rnd()*pSpeed>rnd()*mSpeed:
		print("You attack!")
		mStrength=mStrength-pHit
		pSpeed=pSpeed-int(.5*mHit)
	else:
		print("Monster attacks!")
		pStrength=pStrength-mHit
		mSpeed=mSpeed-int(.5*pHit)
	pExp=pExp+2*pHit
	if mStrength<=0:
		print("The monster is dead!")
		roomContents[pLocation]=roomContents[pLocation]-2
		return
	else:
		print("The monster still lives!")
	return

def run():
	global pStrength
	print("You attempt to run away!")
	if rnd()*pSpeed > rnd()*mSpeed:
		print("You escaped!")
	else:
		print("The monster hit you!")
		pStrength=pStrength-int(.2*mStrength)
	return
	
def updateMove(m):
	global slide
	global roomFlags
	global pLocation
	global monsterPresent
	global pExp
	global visitedRooms
	global numberRooms
	
	if m==99 or m==88 or m<=0 or m>numberRooms:
		return
	if roomFlags[m]==1 or m==slide:
		pLocation=m
		monsterPresent=0
		pExp=pExp+depth
		visitedRooms[pLocation]=1
		getTreasure()
	else:
		print("Not adjacent.")
	return
	
def debugShow():
#	print("Room Contents checked: "+str(roomContents[pLocation])+" n="+str(n))
	print("Visited Rooms:\n"+str(visitedRooms))
	print("Room Contents:\n"+str(roomContents))
	print("Content Flags:\n"+str(contentFlags))
	print("Adjacent Rooms:\n"+str(adjacentRooms))
	print("Room Flags:\n"+str(roomFlags))
	print("Depth: "+str(depth))
	print("Old Depth: "+str(oldDepth))
	return

##### Main Game Loop #####
gameLoop=True
	
while gameLoop==True:
	if oldDepth<>depth:
		setRooms()
		oldDepth=depth
	doAttrition()	
	showStatus()
	checkHazards()
	monstersDemonsGas()
	maxTreasure()
	slideDropoffs()
	m=inputMove()
	print("\n")
	
	if m==88:
		printRooms()
		continue
	if m<0 and contentFlags[19]*contentFlags[13]==1:
		oldDepth=depth
		depth=depth+1
		monsterPresent=0
	if m<0 and (oldDepth==depth):
		print("No dropoff.")
	if m==99 and pLocation==1:
		leaveGame()
	if m==99 and pLocation<>1:
		useWand()
	if m==0 and pLocation==1:
		doTrade()
		continue
	if m==0 and pLocation<>1:
		getTreasure()
	if mStrength>0:
		if m>0 and m<numberRooms:
			run()
			
		else:
			fight()
			continue
	if m<>0:
		updateMove(m)
quit()
