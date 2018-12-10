#!/usr/bin/python

import random
import sys
import time

def getMax(data):
	Max=0
	for c in data.split():
		if(c!=' '):
			Max=max(Max, abs(int(c)))
	return Max

def strip(data):
	data=data.replace('\n', '')
	data=data.replace('(', '')
	data=data.replace(')', '')
	data=data.replace(',', ' ')
	return data

def getClause(data):
	count=0
	for c in data:
		if(c==')'):
			count=count+1

	return count

def writeFile(file, data2):
	data2=data2.replace('\n', '')
	data2=data2.replace('(', '')
	data2=data2.replace(',', ' ')
	data2=data2.replace(')', ' #')
	for c in data2.split():
		if(c=='#'):
			file.write("0\n")
		else:
			file.write(c+" ")

def convert(filename):
	with open(filename, 'r') as myfile:
		data=myfile.read()

	data2=data
	numOfClause=getClause(data)
	data=strip(data)
	numOfVar=getMax(data)
	
	file=open("test.convert", "w")
	file.write("c CNF formula\n")
	file.write("p cnf "+str(numOfVar)+" "+str(numOfClause)+"\n")
	writeFile(file, data2)



def outputAns(solution):
	str1="("
	for i in solution:
		if(i>=0):
			str1=str1+"1,"
		else:
			str1=str1+"0,"
	str1=str1[:-1]
	str1=str1+")"
	#print str1
	return str1

def parse(filename):
    clauses = []
    count = 0
    for line in open(filename):

        if line[0] == 'c':
            continue
        if line[0] == 'p':
            n_vars = int(line.split()[2])
            lit_clause = [[] for _ in xrange(n_vars * 2 + 1)]
            continue

        clause = []
        for literal in line[:-2].split():
            literal = int(literal)
            clause.append(literal)
            lit_clause[literal].append(count)
        clauses.append(clause)
        count += 1
    return clauses, n_vars, lit_clause


def get_random_interpretation(n_vars):
    return [i if random.random() < 0.5 else -i for i in xrange(n_vars + 1)]


def get_true_sat_lit(clauses, interpretation):
    true_sat_lit = [0 for _ in clauses]
    for index, clause in enumerate(clauses):
        for lit in clause:
            if interpretation[abs(lit)] == lit:
                true_sat_lit[index] += 1
    return true_sat_lit


def update_tsl(literal_to_flip, true_sat_lit, lit_clause):
    for clause_index in lit_clause[literal_to_flip]:
        true_sat_lit[clause_index] += 1
    for clause_index in lit_clause[-literal_to_flip]:
        true_sat_lit[clause_index] -= 1


def compute_broken(clause, true_sat_lit, lit_clause, omega=0.4):
    break_min = sys.maxint
    best_literals = []
    for literal in clause:

        break_score = 0

        for clause_index in lit_clause[-literal]:
            if true_sat_lit[clause_index] == 1:
                break_score += 1

        if break_score < break_min:
            break_min = break_score
            best_literals = [literal]
        elif break_score == break_min:
            best_literals.append(literal)

    if break_min != 0 and random.random() < omega:
        best_literals = clause

    return random.choice(best_literals)


def run_sat(clauses, n_vars, lit_clause, max_flips_proportion=1000):
	max_flips = n_vars * max_flips_proportion
	
	interpretation = get_random_interpretation(n_vars)
	true_sat_lit = get_true_sat_lit(clauses, interpretation)
	for _ in xrange(max_flips):

		unsatisfied_clauses_index = [index for index, true_lit in enumerate(true_sat_lit) if
								 not true_lit]

		if not unsatisfied_clauses_index:
			return interpretation

		clause_index = random.choice(unsatisfied_clauses_index)
		unsatisfied_clause = clauses[clause_index]
	
		lit_to_flip = compute_broken(unsatisfied_clause, true_sat_lit, lit_clause)
	
		update_tsl(lit_to_flip, true_sat_lit, lit_clause)
	
		interpretation[abs(lit_to_flip)] *= -1
	print 'no solution'

def main():

	convert(sys.argv[1])
	filename="test.convert"
	clauses, n_vars, lit_clause = parse(filename)
	
	start=time.time()
	solution = run_sat(clauses, n_vars, lit_clause) 
	end=time.time()
	
	ttime = str(end-start)
	print 'it took :' + ttime + ' second to finish the calculation'

	sat = 's SATISFIABLE\n'
	#print 'v ' + ' '.join(map(str, solution[1:])) + ' 0'
	result=outputAns(solution)
	result = sat + result
	file=open("result", "w")
	file.write(result)


if __name__ == '__main__':
    main()




