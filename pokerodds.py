#!/usr/bin/python
# -*- coding:utf-8 -*-
import random 
import itertools
import heapq
import copy



def rank_hand(hand):
	sortedcards = sorted(hand,key=lambda x:(x.value,x.suit),reverse=True)
	handranks={
	1:"Straight Flush",
	2:"Quads",
	3:"Full House",
	4:"Flush",
	5:"Straight",
	6:"Triples",
	7:"Two Pair",
	8:"One Pair",
	9:"High Card"
	}
	#print sortedcards
	smap= dict()
	rmap = dict()
	heap = []
	for x in sortedcards:
		rank,suit = x.value,x.suit
		rmap[rank] = rmap.get(rank,0)+1
		smap[suit] = smap.get(suit,0)+1
	for k,v in rmap.items():
		heapq.heappush(heap,(-v,-k))
	#print smap
	#print rmap
	print "Evaluating: ",
	for x in sortedcards:print  x,
	print
	ranklookup = {"sflush":1,"straight":5,"flush":4}
	def valid(name,cardx,cardy):
		if name=="sflush":
			return cardy.suit==cardx.suit and cardx.value==cardy.value+1
		elif name=="straight":
			return cardx.value==cardy.value+1
		elif name=="flush":
			return cardy.suit==cardx.suit

	def straight_flush(handtype):
		if handtype=="flush":cards = sorted(hand,key=lambda x:(x.suit,x.value),reverse=True)
		else: cards = sorted(hand,key=lambda x:(x.value,x.suit),reverse=True)
		currlength,res = 1,0
		values = [cards[0].value]

		for cardx,cardy in zip(cards,cards[1:]):
			if valid(handtype,cardx,cardy):
				values += [cardy.value]
				if len(values)==5:
					return (values,ranklookup[handtype])
			else:
				values = [cardy.value]
			#print cardx,cardy
		return -1
	
	def count_cards():
		temp = copy.deepcopy(heap)
		res=[]
		if temp[0][0]==-4:
			res+= [heapq.heappop(temp)[1]*-1]*4
			res+= [heapq.heappop(temp)[1]*-1]
			return (res,2)
		elif temp[0][0]==-3:
			res+= [heapq.heappop(temp)[1]*-1]*3
			if temp[0][0]==-2:
				res+= [heapq.heappop(temp)[1]*-1]*2
				return (res,3) 
			else:
				res+= [heapq.heappop(temp)[1]*-1]
				res+= [heapq.heappop(temp)[1]*-1]
				return (res,6)
		elif temp[0][0]==-2:
			res+= [heapq.heappop(temp)[1]*-1]*2
			if temp[0][0]==-2:
				res+= [heapq.heappop(temp)[1]*-1]*2
				res+= [heapq.heappop(temp)[1]*-1]
				return (res,7)
			else:
				res+= [heapq.heappop(temp)[1]*-1]
				res+= [heapq.heappop(temp)[1]*-1]
				res+= [heapq.heappop(temp)[1]*-1]
				return (res,8)
		else:
			for i in range(5):
				res+=[sortedcards[i].value]
			return (res,9)

	ans = straight_flush("sflush")
	if ans>0:print "Straight flush" ;return ans
	
	res = count_cards()
	if res[1]>3:
		ans = straight_flush("flush")
		if ans>0:print "Flush" ;return ans
		ans = straight_flush("straight")
		if ans>0:print "Straight" ;return ans
	

	print  handranks[res[1]];return res
	
	
	
class Card:
	def __init__(self,rank,suit,value):
		self.rank = rank
		self.suit = suit
		self.value= value
	def __str__(self):
		return "(" +self.rank +"," + self.suit+")"
	def __eq__(self,other):
		return self.rank==other.rank and self.suit==other.suit and self.value== other.value
	def __hash__(self):
		return hash((self.rank,self.suit,self.value))


flop = [Card("3","♦︎",2),Card("5","♣︎",4),Card("9","♣︎",8)]
p1 = [Card("3","♣︎",2),Card("7","♥︎",6)]
p2 = [Card("A","♠︎",13),Card("10","♠︎",9)]
p3 = [Card("9","♠︎",8),Card("2","♦︎",1)]
p4 = [Card("K","♣︎",12),Card("J","♣︎",10)]





v = set()
for c in flop:v.add(c)
for c in p1:v.add(c)
for c in p2:v.add(c)
for c in p3:v.add(c)
for c in p4:v.add(c)


class Deck:
	ranks = ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]
	suits = ["♣︎","♠︎","♦︎","♥︎"]
	vals = dict()
	deck = []
	def __init__(self):
		
		for i,rank in enumerate(self.ranks):
			for suit in self.suits:
				c = Card(rank,suit,i+1)
				if c not in v:
					self.deck.append(c)


	def shuffle(self):
		random.shuffle(self.deck)
		
	def show(self):
		for card in self.deck:
			print card

	def reset(self):
		self.deck = []
		for rank in self.ranks:
			for suit in self.suits:
				self.deck.append(Card(rank,suit))

	def get_card(self):
		idx = random.randint(0,len(self.deck)-1)
		return self.deck.pop(idx)
	def get_hand(self):
		return [self.get_card(),self.get_card()]
	def remaining(self):
		return len(self.deck)

dec = Deck()

def winner(a,b,c,d):
	return max((a,1),max((b,2),max((d,4),(c,3))))
def tiebreak(hands):
	print "tiebreak: ",hands
	for i in range(5):
		maximum = max([x[0][i] for x in hands])
		hands = [x for x in hands if x[0][i]>=maximum]
		if len(hands)==1:break
		
	return hands[0][1]

wincounts= dict()
gamecount = 0 
for c1,c2 in list(itertools.combinations(dec.deck,2)):
	ahand,arank = rank_hand([c1]+[c2]+p1+flop)
	bhand,brank = rank_hand([c1]+[c2]+p2+flop)
	chand,crank = rank_hand([c1]+[c2]+p3+flop)
	dhand,drank = rank_hand([c1]+[c2]+p4+flop)

	kappa = dict()
	kappa[arank] = kappa.get(arank,[])+ [(ahand,1)]
	kappa[brank] = kappa.get(brank,[])+ [(bhand,2)]
	kappa[crank] = kappa.get(crank,[])+ [(chand,3)]
	kappa[drank] = kappa.get(drank,[])+ [(dhand,4)]
	highest = kappa[min(kappa)]
	if len(highest)==1:
		hand,player = highest[0]
		wincounts[player] = wincounts.get(player,0)+1
	else:
		player = tiebreak(highest)
		wincounts[player] = wincounts.get(player,0)+1
	for k,v in sorted(kappa.items()):
		print k,v,len(v)
	
	
	'''
	gamecount+=1
	w = winner(a,b,c,d)
	wincounts[w[1]]= wincounts.get(w[1],0) + 1
	'''
	print "A= ",ahand,"B= ",bhand,"C= ",chand,"D= ",dhand," ---> "
	print "\n\n"


#print rank_hand(c.get_hand()+c.get_hand()+c.get_hand()+[c.get_card()])

for k,v in wincounts.iteritems():
	print k,v
	print "Player",k,"{:.1%}".format(float(v)/820)

