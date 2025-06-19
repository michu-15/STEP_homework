'''
オフィスアワーで宿題１について
①経路を全て保存するのではメモリをたくさん使ってしまうこと
②一個でも最短経路がわかったらいい
というアドバイスをもらったのでそれを元に1️⃣を書き直しました。
さらに同じ考え方で最短経路管同じものを複数回答できるように2️⃣で書いてみました。

時間計算量はN(ノードの数)+M(エッジの数)
while dequeのところでO(N)
for neighbor ... のところで合計としてO(M)

'''


#def_initで以下の文を追加しています
'''
    def __init__(self):
    #ID→名前で辿るのは大変なので辞書の形を逆にする
    self.title_to_id = {title: id for id, title in self.titles.items()}
'''

from collections import deque
from collections import defaultdict

#リンクが次についているものを持ってくる
def get_neighbors(self, title):
    id = self.title_to_id.get(title)
    if id is None:
        return []
    return [self.titles[n_id] for n_id in self.links.get(id, [])]



#1️⃣一個だけでも見つかったらいい時
def build_path_one(self, goal, previous_node):
    path = []
    current = goal
    while current is not None:
        path.append(current) #逆順で辿って入れていく
        current = previous_node.get(current)
    path.reverse()  # スタート→ゴールにするため逆順に
    return path 


def find_shortest_path_just_one(self, start, goal):
    queue = deque([start])
    visited = set()
    visited.add(start)
    #直前のノードを記憶させて（一つだけ）あとでgoalから辿れる様に
    previous_node = {}
    previous_node[start] = None

    while queue:
        current = queue.popleft()

        if current == goal:
            ans = self.build_path_one(goal, previous_node)
            return ans

        for neighbor in self.get_neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                #このタイミングで前のノードの記憶をする
                previous_node[neighbor] = current
                queue.append(neighbor)
    return None


#2️⃣同じ深さで複数経路全部見つけたい時
def build_paths(self, current, previous_nodes, path, all_paths):
    #curentがstartになった時終わり
    if not previous_nodes[current]:
        all_paths.append([current] + path) #前に結果をたしていくことで、最後反転の手間を省く
        return
    #再起的に辿っていく
    for prev in previous_nodes[current]:
        self.build_paths(prev, previous_nodes, [current] + path, all_paths)

def find_shortest_paths(self, start, goal):
    queue = deque()
    queue.append(start)
    visited_and_depth = {start:0}
    previous_nodes = defaultdict(list)  #先ほどと違って複数の前のノードを格納する
    previous_nodes[start] = []
    #答えの最短経路を入れるリスト（いくつかある）
    all_paths = []

    while queue:
        current = queue.popleft()
        
        if current == goal:
            self.build_paths(current, previous_nodes, [] , all_paths)
            return all_paths
        
        #次に行ける先を一個ずつみていく
        for neighbor in self.get_neighbors(current):
            next_depth = visited_and_depth[current] + 1
            
            #初めてのノードにであった時
            if neighbor not in visited_and_depth:
                visited_and_depth[neighbor] = visited_and_depth[current] + 1
                previous_nodes[neighbor].append(current)
                queue.append(neighbor)
            #初めてではないが最短距離が同じ時
            elif visited_and_depth[neighbor] == next_depth:
                previous_nodes[neighbor].append(current)


#3️⃣オフィスアワーの前に提出したもの
def find_shortest_path(self, start, goal):
    queue = deque()
    queue.append((start,[start]))
    visited = {}
    answers = []     #最短の経路がいくつかある時にそれらを保存するリスト
    min_lenth = None #最短かどうかを確認するため
    
    while queue:
        current, path = queue.popleft()
        #goalのノードに当たった時、それが最短なのかを確認
        if current == goal:
            if min_lenth is None:
                answers.append(path)
                min_lenth = len(path)
            elif min_lenth == len(path):  #最短経路がいくつかある時
                answers.append(path)
            continue

        #goalにあたっていなくてもすでに最短経路が見つかっていればそれ以降は探索不要
        if min_lenth is not None and len(path) > min_lenth:
            continue
        
        #次に行ける先を一個ずつみていく
        for neighbor in self.get_neighbors(current):
            new_distance = len(path)
            if (neighbor not in visited) or (new_distance <= visited[neighbor]):
                visited[neighbor] = new_distance
                queue.append((neighbor, path + [neighbor]))

    return answers   #時間計算量はN+M　経路を全て保存しているのがよくない

