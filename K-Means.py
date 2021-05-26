#!/usr/bin/env python
# coding: utf-8

# Submitted By :
#   Navpreet Singh
#   ns4767@nyu.edu



# defines the condition that each clusters has atleast 2 data points

def condition(clusters):
    for i in clusters:
        if len(i) < 2:
            return True
    return False


# finds the mean of all the points belonging to a single cluster

def mean(cluster,data):
    d = len(data[cluster[0]])
    m = [0 for _ in range(d)]
    for clust in cluster:
        for j in range(d):
            m[j]+=data[clust][j]
    n = len(cluster)
    for i in range(len(m)):
        m[i] = round(m[i]/n,2)
    return m


# finds and returns the index of center which is closest to the given data point

def closestcentre(datapoint,centers):
    d = len(datapoint)

    closest = 0
    idx = 0
    for i in range(d):
        closest += (datapoint[i]-centers[0][i])**2
    for i in range(1,len(centers)):
        dist = 0
        for j in range(d):
            dist += (datapoint[j]-centers[i][j])**2
        if dist < closest:
            closest = dist
            idx = i
    return idx


# calculates the total cost which is the squared euclidean distance of all the points
# from their center of the cluster they belong to

def cost(clusters,centers,data):

    cst = 0
    for k in range(len(clusters)):
        for c in range(len(clusters[k])):
            datapoint = clusters[k][c]
            for d in range(len(centers[k])):
                cst += (data[datapoint][d]-centers[k][d])**2
                
    return cst


# prints the output in the format as given in the assignment statement

def verboseReport(clusters, centers, data):
    k = len(clusters)
    for p in range(k):
        print("Clusters {}: {}. Center={}".format(p+1,clusters[p],centers[p]))
    print("Cost={:.2f}".format(cost(clusters,centers,data)))


# Implementation of the kMeans algorithm as described in the programming assignment

def kMeans(k,data,verbose):
    
    centers = []
    n = len(data)
    clusters = [[] for _ in range(k)]
    
    while condition(clusters):
        clusters = [[] for _ in range(k)]
        for i in data.keys():
            ak = random.randint(0, k-1)
            clusters[ak].append(i)
    
    i = 0
    Reassigned = True
    starve = False
    
    while Reassigned:
        Reassigned = False
        i+=1
        centers = [[] for _ in range(k)]
        for j in range(k):
            centers[j] = mean(clusters[j],data)
        
        if verbose:
            verboseReport(clusters, centers, data)
            print("")
        
        newclusters = [[] for _ in range(k)]
        
        for j in data.keys():
            u = closestcentre(data[j],centers)
            newclusters[u].append(j)
        kNew = 0

        if newclusters != clusters:
            Reassigned = True
        for clust in newclusters:
            if clust!=[]:
                kNew+=1
                
        if kNew<k:
            starve = True
            clusters = []
            for clust in newclusters:
                if clust!=[]:
                    clusters.append(clust)
            k=kNew
        else:
            clusters = newclusters
            
    if verbose:
        print("KMeans terminates with final clustering")
        verboseReport(clusters, centers, data)
        print("{} iteration".format(i))
        print("")
            
    return clusters,i,centers,starve



# Implementation of kMeans with random restart which calls kMeans implemented above r times and
# returns the lowest cost which is the best output and prints the result

def kMeansWithRandomRestart(k,data,verbose,r):
    mincost = 10e9
    avgiter = 0
    starvation = 0
    costs = []
    for i in range(r):
        if verbose:
            print("\nRandom restart {}".format(i+1))
        clusters,i,centers,starve = kMeans(k,data,verbose)
        avgiter += i
        if starve:
            starvation += 1
        cst = cost(clusters,centers,data)
        costs.append(cst)
        if cst<mincost:
            mincost=cst
            bestclusters = clusters
            bestcenters = centers
            
    within2factor = 0
    for cst in costs:
        if cst<2*mincost:
            within2factor += 1
    
    print("\nBest clustering found")
    verboseReport(bestclusters, bestcenters, data)
    print("Average number of iterations: {}".format(avgiter/r))
    print("Starvation occured {} times.".format(starvation))
    print("A solution within a factor of 2 of the best was found in {} of the random restarts.".format(within2factor/r))
    return bestclusters
    


import csv
import random

# main function which prompts the input of k,r,flag and reads the "input.csv" file and then calls kMeansWithRandomRestart

if __name__ == "__main__":
    
    k = int(input("Input k: "))
    r = int(input("Input r: "))
    flag = int(input("Input flag: "))
    
    coord = {}
    with open('input.csv', 'r') as file:
        reader = csv.reader(file,skipinitialspace=True)
        for row in reader:
            coord[row[0]] = []
            for d in range(1,len(row)):
                coord[row[0]].append(float(row[d]))
    
    #kMeans(k,coord,flag)
    clusters = kMeansWithRandomRestart(k,coord,flag,r)
