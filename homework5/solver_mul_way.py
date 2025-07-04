import sys
import math
from common import print_tour, read_input


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

#距離行列を作る
def distance_matrix(cities):
    N = len(cities)
    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])
    return dist

#貪欲法
def greedy(cities,dist):
    N = len(cities)
    current_city = 0
    unvisited_cities = set(range(1, N)) #全部の年をいれる
    tour = [current_city]   #訪問順に入れていく
    
    #全部の年を回るまで最短で繋ぐ
    while unvisited_cities:
        next_city = min(unvisited_cities,
                        key=lambda city: dist[current_city][city])
        unvisited_cities.remove(next_city)
        tour.append(next_city)
        current_city = next_city

    return tour

#2-opt法
def two_opt(tour, dist):
    N =len(tour)
    #実行が終わらなかったのでループ回数の制限
    count = 0
    max_count = 1000

    improve = True
    while improve and count < max_count :
        improve = False
        count += 1 #
        for i in range(0, N - 2):
            a, b = tour[i], tour[i + 1]
            for j in range(i + 2 , N):
                c, d = tour[j], tour[(j + 1) % N] #ｊ=N　のとき最初に戻るために % N
                

                # print(a,b,c,d)
                old_distance = dist[a][b] + dist[c][d]
                new_distance = dist[a][c] + dist[b][d]
                #短い距離の法を採用
                if new_distance < old_distance:
                    #間の区間を反転
                    tour[i+1:j+1] = reversed(tour[i+1:j+1])
                    improve = True
                    break
            if improve:
                break

    return tour

def solve(cities):
    dist = distance_matrix(cities)
    #始めに貪欲法で繋ぐ
    tour = greedy(cities, dist)
    #2-optで改善
    tour = two_opt(tour, dist)
    return tour

#全体の距離計算
def total_distance(tour, dist):
    total = 0
    n = len(tour)
    for i in range(n):
        start_city = tour[i]
        
        if i == n - 1:
            goal_city = tour[0] # 最後の都市のときだけ、スタート地点に戻る
        else:
            goal_city = tour[i + 1]
        
        total += dist[start_city][goal_city]
    
    return total


if __name__ == '__main__':

    assert len(sys.argv) > 1
    tour = solve(read_input(sys.argv[1]))
    print_tour(tour)
    dist = distance_matrix(read_input(sys.argv[1]))
    print(f"Total distance: {total_distance(tour, dist)}")
