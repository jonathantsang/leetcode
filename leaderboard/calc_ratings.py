from collections import defaultdict
from heapq import nsmallest
from os import listdir
from time import time

SCRAPED_DIR_PATH = "C:/leetcode/leaderboard/scraped/"
ratings = defaultdict(lambda: [1500.0, 0])  # rating, participations
skips = 0

with open('saved_ratings.txt', encoding='utf-8') as fi:
    skips = int(fi.readline().split()[0])
    fi.readline()

    for line in fi:
        _, name, r, p = line.split("\t")
        ratings[name][0] = float(r)
        ratings[name][1] = int(p)

    print("skipped first {} contests".format(skips))


def eab(r1, r2):
    # The E_{a, b} function defined in the ratings algo
    return 1.0 / (1.0 + 10.0 ** ((r2 - r1) / 400.0))

def f(k):
    # The 'f' function defined in the ratings algo
    return 2.0 / min(k+3, 9)
    
def mark(results):
    """
    Score a contest, given that the person with name
    results[0] came in 1st place, the person with name
    results[1] came in 2nd place, etc.
    """
    newrating = {}
    ratings_local = [ratings[n] for n in results]
    start_time = time()
    for i, name1 in enumerate(results):
        if i % 200 == 0:
            if i:
                time_per_res = (time() - start_time) / i
                prediction = time_per_res * (len(results) - i)
            else:
                prediction = -1
            print(f"on {i} of {len(results)}; eta={round(prediction, 1)}")
        erank = 1
        r1 = ratings_local[i][0]
        for j, name2 in enumerate(results):
            if i != j:
                r2 = ratings_local[j][0]
                erank += eab(r2, r1)
        rhs = (erank * (i+1)) ** 0.5

        # Binary search for expected rating
        lo, hi = -2000, 5000
        while lo + 1e-4 < hi:
            mi = (lo + hi) / 2.0
            lhs = 1
            for j0, (r3, _) in enumerate(ratings_local):
                if j0 != i:
                    lhs += eab(r3, mi)
            if lhs > rhs:
                lo = mi
            else:
                hi = mi
        assert -1999 <= lo and hi <= 4999, "{} {}".format(lo, hi)
        k1 = ratings_local[i][1] + 1
        delta = f(k1) * ((lo + hi) / 2.0 - r1)
        newrating[name1] = r1 + delta
        if i < 100:
            print(name1, ratings_local[i], erank, newrating[name1])

    for n, r in newrating.items():
        ratings[n][0] = r
        ratings[n][1] += 1
    

ZERO = "###@@@ZERO@@@###"
for fname in sorted(listdir(SCRAPED_DIR_PATH)):
    
    index = int(fname[:3])
    if index < skips:
        continue
    print("!", fname)
    fname = SCRAPED_DIR_PATH + fname

    A = []
    with open(fname, encoding='utf-8') as fi:
        for line in fi:
            A.append(line.rstrip('\r\n'))

    #  For now, do nothing and take scores 'as is'.
    #  Later, could handle tie scores better
    if ZERO in A:
        _ = A.pop(A.index(ZERO))
    else:
        print("WARNING: NO ZERO AT", fname)

    
    mark(A)

    #scores = nsmallest(10, ratings.items(), key = lambda z: -z[1][0])
    #for row in scores:
    #    print(row[0], round(row[1][0], 3))

# Dump ratings info to file
stuff = sorted(ratings.items(), key = lambda z: [-z[1][0], -z[1][1], z[0]])
for stub, items in (('', stuff), ('_top5000', stuff[:5000])):
    with open('saved_ratings'+stub+'.txt', 'w', encoding='utf-8') as fo:
        _ = fo.write("{} contests\n".format(index + 1))
        _ = fo.write("rank\tname\trating\tparticipations\n")
        for i, (name, (r, p)) in enumerate(items, 1):
            _ = fo.write("{}\t{}\t{}\t{}\n".format(i, name, r, p))

print("R  Name                   Rating   Participations")
for i, (name, (r, p)) in enumerate(items[:50], 1):
    print(str(i).zfill(2), name + ' ' * (22 - len(name)), int(round(r)), '   ', p)

          
