import requests 
import sys 
import re
from poker.website.pokerstars import get_status, get_current_tournaments


touru5 = 0
touro5 = 0
tourz = 0 
players = []
buyinz = [] 
rakez = []
for tour in get_current_tournaments():
	if 'Play Money' not in tour.name:
		if '$' in tour.buyin: 
			s = tour.buyin 
			s = s.replace('$',' ')
			sfinal = s.split('+')
			bi = float(sfinal[0])
			rake = float(sfinal[1])
			totalbi = float(bi + rake)
			playerz = int(tour.players)
			#print ('$'+str(bi), '+', '$'+str(rake)), tour.name
			if bi < 3:
				print '${a} | {c} | {d}'.format(a=totalbi,c=tour.name, d=tour.start_date)
				touru5 += 1
			else: 
				touro5 += 1 
			tourz += 1 	
			buyinz.append(bi)
			rakez.append(rake)
			players.append(playerz)


print '----------------------------'
print 'Total tours (Under $5): {a}'.format(a=touru5)
print 'Total tours (Over $5): {b}'.format(b=touro5)
print 'Total tours (Overall) : {c}'.format(c=tourz)
print '----------------------------'
print 'Avg. BI: {d}'.format(d = int(reduce(lambda x, y: x + y, buyinz)/len(buyinz)))
print 'Max. Players: {e}'.format(e = max(players))





