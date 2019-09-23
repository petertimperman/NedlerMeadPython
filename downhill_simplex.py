import numpy as np

import random

class Simplex():
    def __init__(self, initial_point,  npoints=3 , verbose = False):
        self.points = [None] * npoints
        self.verbose = verbose
        unit_vector = initial_point / np.linalg.norm(initial_point)
        for i in range(npoints):
            unit_vector[0] += random.randint(-3,3)
            unit_vector[1] += random.randint(-3,3)

            self.points[i] = initial_point + i*unit_vector

    def order(self, func):
        # if(self.verbose):
        #     print("Ordering")
        pairs = []
        for vertex in self.points:
             pairs.append( (vertex , func(vertex)))
        self.points= [p[0] for p in sorted(pairs, key=lambda x: x[1])]
        return pairs

    def findCentriod(self):

        # if(self.verbose):
        #     print("Finding Centriod")
        sum = np.zeros(self.points[1].shape, dtype=float)
        for n in range(len(self.points)-1):
            sum = np.add( sum, self.points[n])

        self.centriod =  sum/(len(self.points)-1)

    def expand(self, gamma = 2):
        if(self.verbose):
            print("Expanding")
        return self.centriod + gamma*(self.reflect()-self.centriod)

    def reflect(self, alpha =1 ):
        if(self.verbose):
            print("Reflecting")
        return  self.centriod + alpha * ( self.centriod-self.points[-1] )
    def contract(self, target_vertex , beta = .5):
        if(self.verbose):
            print("Contracting")
        return self.centriod + beta * (target_vertex - self.centriod)
    def shrink(self, delta = .5):
        if(self.verbose):
            print("Shrinking")
        for i,vertex in enumerate(self.points[1:]):
            self.points[i+1] = self.points[0]+ delta * (vertex - self.points[0])
    def accept(self, vertex):
        self.points[-1] = vertex
def NedlerMead(func, simplex, max_interations = 100 , function_toler =.01, verbose = False ):
    iterate = True
    iterations = 0
    while iterate:

        print("Iteration->"+str(iterations))
        pairs = simplex.order(func)
        yield simplex.points
        simplex.findCentriod()
        if verbose:
            print("Centriod->" + str(simplex.centriod))
        f_best = func(simplex.points[0])
        f_worst = func(simplex.points[-1])
        f_second = func(simplex.points[-2])


        vert_refl = simplex.reflect()
        f_refl = func(vert_refl)
        if verbose:
            print("Reflection" +str(vert_refl) + "f->" + str(f_refl))
        if (f_refl < f_second and f_refl >= f_best):
            simplex.accept(vert_refl)
            if verbose:
                print("Reflected to" + str(vert_refl))
        elif f_refl < f_best:
            vert_expan = simplex.expand()
            if func(vert_refl )> func(vert_expan):
                simplex.accept(vert_expan)
                if verbose:
                    print("Expanded from " + str(simplex.centriod) +" to " + str(vert_expan))
            else:
                simplex.accept(vert_refl)

                if verbose:
                    print("Reflected to " + str(vert_refl))
        elif f_refl >= f_second:
            if f_second <= f_refl and f_refl < f_worst:
                vert_cont = simplex.contract(vert_refl)
                if func(vert_cont) < f_refl:
                    simplex.accept(vert_cont)

                    if verbose:
                        print("Cotracted outside to " + str(vert_cont))
                else:
                    simplex.shrink()
                    if verbose:
                        print("Shrunk to " + str(simplex.points[1:]))

            elif f_refl >= f_worst:
                vert_cont= simplex.contract(simplex.points[-1])
                if func(vert_cont) < f_second:
                    simplex.accept(vert_cont)
                    if verbose:
                        print("Cotracted inside to " + str(vert_cont))
                else:
                    simplex.shrink()
                    if verbose:
                        print("Shrunk to " + str(simplex.points[1:]))





        iterations += 1
        if iterations >= max_interations:
            iterate = False


