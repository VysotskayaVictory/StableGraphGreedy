# This work is licensed under a Creative Commons Attribution 4.0 International License.
# Author: Victoria Vysotskaya 
# Date: 30.04.2020

import copy 
import collections

def bin(x,y):
	res = 1
	for i in range(y):
		res *= (x-i)*1.0/(i+1)
	return res 

class fs(frozenset):
	def __str__(self):
		return "<{0}>".format(", ".join(str(x) for x in self))
	def __repr__(self):
		return str(self) 

def find_min_deg(vert, v_old, ban, ban_set, edge):
	N = len(vert)  
	first = True 
	for i in range(N): 
		if (i in ban) or (edge.union({i}) in ban_set): 
			continue 
		if first:
			res = i
			first = False 
		elif len(vert[i]) < len(vert[res]): 
			res = i
		elif len(vert[i]) == len(vert[res]):
			if len(v_old[i]) < len(v_old[res]):
				res = i 
	return res

def form_ban(ban_set, count, edge, r, n):
	if r == 0:
		return
	for v in edge:
		tmp = edge - {v}
		count[tmp] += 1
		if count[tmp] == n-r+1:
			ban_set.add(tmp)
			form_ban(ban_set, count, edge-{v}, r-1, n)

def new_edge(v_old, r, edges, ban_set): 
	ban = set()
	vert = copy.deepcopy(v_old) 
	N = len(vert)
	edge = set() 
	inter = set()
	for i in range(r-1):
		inter_local = set()  
		to_add = find_min_deg(vert, v_old, ban, ban_set, edge) 
		edge.add(to_add)
		ban.add(to_add)  
		inter = inter.union(vert[to_add]) 
		for edge_to_rem in vert[to_add]:
			for v in edge_to_rem:
				if v != to_add: 
					vert[v].remove(edge_to_rem)  
	L = len(edges)
	for i in range(L): 
		if edge.issubset(edges[i]):
			ban.add(list(edges[i]-edge)[0])  
	to_add = find_min_deg(vert, v_old, ban, ban_set, edge)
	edge.add(to_add)  
	inter = inter.union(vert[to_add]) 
	return (fs(edge), inter)

def main(r,n):
	stop = bin(n,2*r)
	vert = [set() for i in range(n)]
	edges = [] 
	set_num = 0
	inter = set()
	inter_num = 0
	edge_inter_parts = set()
	part_to_main = dict()
	count = collections.defaultdict(int)
	ban_set = set() 
	rep_num = 0

	while set_num - rep_num - inter_num < stop:
		local_rep = set() 
		(edge, inter) = new_edge(vert,r,edges, ban_set) 
		form_ban(ban_set, count, edge, r, n) 
		edges.append(edge) 
		for i in edge:
			vert[i].add(edge) 
		for e in inter:	 
			to_add = fs(edge.intersection(e))
			edge_inter_parts.add(to_add)
			part_to_main[to_add] = e 
		for e in edge_inter_parts:
			inter_add = edge - e 
			if inter_add in edge_inter_parts: 
				tmp = (part_to_main[e] - edge).union(part_to_main[inter_add] - inter_add)
				if tmp in edges:
					local_rep.add(tmp)  
		rep_num += len(local_rep) 
		set_num = bin(len(edges),2)
		inter_num += len(inter)  
	print(edges)

					





