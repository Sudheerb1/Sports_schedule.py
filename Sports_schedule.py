import gurobipy as gp
from gurobipy import GRB
import re

#defining the number of teams
n = 8

#defining the total number of weeks
w = n-1

#defining the number of periods

p = int(n/2)

#creating model
Sports_schedule = gp.Model("Sports")

#adding variables to the sports scheduling problem

xijkl = []
for i in range(n):
    x = []
    for j in range(n):
        xi.append(Sports_schedule.addVar(lb=0.0, ub=1.0, vtype=GRB.INTEGER,
                                        name="x_" + str(i) + "_" + str(j) ))
        xi = []
        for k in range(w):
            xij.append(Sports_schedule.addVar(lb=0.0, ub=1.0, vtype=GRB.INTEGER,
                                             name="x_" + str(i) + "_" + str(j)+ "_" + str(k)))
            xij = []
            for l in range(p):
                xijk.append(Sports_schedule.addVar(lb=0.0, ub=1.0, vtype=GRB.INTEGER,name="x_"+str(i)+"_"+str(j)+"_"+str(k)+"_"+str(l)))
    xijkl.append(x)


print(Sports_schedule)

#adding constraints

#c1
#every team cannot play itself
for i in range(n):
    for k in range(w):
        for l in range(p):
            if j == i:
                Sports_schedule.addConstr(xijkl, GRB.EQUAL, 0, "c1_"+str(i)+"_"+str(k)+"_"+str(l))

#c2
#Each team plays only one match in a week
for i in range(n):
    for k in range(w):
        sum = 0
        for l in range(p):
            for j in range(n):
                if i!=j:
                    sum = sum + xijkl[i][j][k][l] + xijkl[j][i][k][l]
        Sports_schedule.addConstr(sum, GRB.EQUAL,1, "c2_"+str(i)+"_"+str(k))

#c3
#Atmost two matches were played by a team in one period
for i in range(n):
    for l in range(p):
        sum = 0
        for k in range(w):
            for j in range(n):
                if i!=j:
                    sum = sum + xijkl[i][j][k][l] + xijkl[j][i][k][l]
        Sports_schedule.addConstr(sum, GRB.LESS_EQUAL,2, "c3_"+str(i)+"_"+str(l))

#c4
#Only one game can be played between a pair of teams
for k in range(w):
    for l in range(p):
        sum = 0
        for i in range(n):
            for j in range(n):
                sum = sum + xijkl[i][j][k][l] + xijkl[j][i][k][l]
        Sports_schedule.addConstr(sum, GRB.EQUAL,1, "c4_"+str(k)+"_"+str(l))

#c5
#Each slot is assigned a slot
for k in range(w):
    for l in range(p):
        sum = 0
        for i in range(n):
            for j in range(n):
                sum = sum + xijkl[i][j][k][l]
        Sports_schedule.addConstr(sum, GRB.EQUAL,1, "c5_"+str(k)+"_"+str(l))

#objective function
obj = 0
for l in range(p):
    for k in range(w):
        for i in range(n):
            for j in range(n):
                obj = obj + xijkl[i][j][k][l]

Sports_schedule.setObjective(obj, GRB.MAXIMIZE)

#optimization
Sports_schedule.update()
Sports_schedule.optimize()

if Sports_schedule.status == GRB.Status.OPTIMAL:
    for l in range(p):
        for k in range(w):
            for i in range(n):
                for j in range(n):
                    xijkl[i][j][k][l] = int(xijkl[i][j][k][l].x)
else:
    Sports_schedule.computeIIS()
    Sports_schedule.write("Sports_schedule.ilp")

