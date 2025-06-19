import sys
import collections
from collections import deque
from collections import defaultdict

class Wikipedia:

    # Initialize the graph of pages.
    def __init__(self, pages_file, links_file):

        # A mapping from a page ID (integer) to the page title.
        # For example, self.titles[1234] returns the title of the page whose
        # ID is 1234.
        self.titles = {}

        # A set of page links.
        # For example, self.links[1234] returns an array of page IDs linked
        # from the page whose ID is 1234.
        self.links = {}

        # Read the pages file into self.titles.
        with open(pages_file) as file:
            for line in file:
                (id, title) = line.rstrip().split(" ")
                id = int(id)
                assert not id in self.titles, id
                self.titles[id] = title
                self.links[id] = []
        print("Finished reading %s" % pages_file)

        #ID→名前で辿るのは大変なので辞書の形を逆にする
        self.title_to_id = {title: id for id, title in self.titles.items()}

        # Read the links file into self.links.
        with open(links_file) as file:
            for line in file:
                (src, dst) = line.rstrip().split(" ")
                (src, dst) = (int(src), int(dst))
                assert src in self.titles, src
                assert dst in self.titles, dst
                self.links[src].append(dst)
        print("Finished reading %s" % links_file)
        print()


    # Example: Find the longest titles.
    def find_longest_titles(self):
        titles = sorted(self.titles.values(), key=len, reverse=True)
        print("The longest titles are:")
        count = 0
        index = 0
        while count < 15 and index < len(titles):
            if titles[index].find("_") == -1:
                print(titles[index])
                count += 1
            index += 1
        print()


    # Example: Find the most linked pages.
    def find_most_linked_pages(self):
        link_count = {}
        for id in self.titles.keys():
            link_count[id] = 0

        for id in self.titles.keys():
            for dst in self.links[id]:
                link_count[dst] += 1

        print("The most linked pages are:")
        link_count_max = max(link_count.values())
        for dst in link_count.keys():
            if link_count[dst] == link_count_max:
                print(self.titles[dst], link_count_max)
        print()


    # Homework #1: Find the shortest path.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.


    #リンクが次についているものを持ってくる
    def get_neighbors(self, title):
        id = self.title_to_id.get(title)
        if id is None:
            return []
        return [self.titles[n_id] for n_id in self.links.get(id, [])]

    #宿題１ 
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

    # Homework #2: Calculate the page ranks and print the most popular pages.


    def find_most_popular_pages(self):
        #各ノードに１を割り当て
        id_rank = {id: 1.0 for id in self.titles}
        num_pages = len(self.titles)
        max_iterations = 100

        #収束するまでスコアの計算を繰り返す
        for i in range(max_iterations):
            new_rank = defaultdict(float) #メモリ効率アップnew_rankの初期化を不要にした
            
            #リンク先がないページのスコアをまとめる　O(N^2)→O(N)
            dead_end_sum = sum(0.85 * id_rank[id] for id in self.titles if  len(self.links.get(id, [])) == 0)
            dead_end_divid = dead_end_sum / num_pages
            #各ノードごとみていく
            for id in self.titles:
                rank = id_rank[id]
                link_targets = self.links.get(id, [])

                #リンク先の数だけスコアをわけて、それぞれの行き先にスコア追加
                if link_targets:
                    divide_rank = (0.85 * rank)/ len(link_targets)
                    for target in link_targets:
                        new_rank[target] += divide_rank
            
            #リンク先がないと全体にスコア追加
                new_rank[id] += 0.15 + dead_end_divid

            #ページランクの合計の計算
            total_rank  = sum(new_rank.values())
            print(f"Iteration {i + 1}: total rank sum = {total_rank:.6f}")

            #収束しているかどうか確認
            diff = sum((new_rank[id] - id_rank[id]) ** 2 for id in self.titles)
            print(f"Iteration {i + 1}: diff = {diff:.6f}")
            if diff < 0.01:
                print("Converged.")
                break
            id_rank = new_rank
        
        # 上位10件を表示
        top10 = sorted(id_rank.items(), key=lambda x: x[1], reverse=True)[:10]
        print("\nTop 10 popular pages:")
        for id, score in top10:
            print(f"{self.titles[id]} (score: {score:.4f})")

#テスト用
# wikipedia = Wikipedia('wikipedia_dataset/pages_small.txt', 'wikipedia_dataset/links_small.txt')
#wikipedia = Wikipedia('wikipedia_dataset/pages_medium.txt', 'wikipedia_dataset/links_medium.txt')
#wikipedia = Wikipedia('wikipedia_dataset/pages_large.txt', 'wikipedia_dataset/links_large.txt')
#a = wikipedia.find_shortest_path('A', 'F')
#a = wikipedia.find_shortest_path('渋谷', '小野妹子')
#print(a)
#wikipedia.find_most_popular_pages()



    # Homework #3 (optional):
    # Search the longest path with heuristics.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
    def find_longest_path(self, start, goal):
        #------------------------#
        # Write your code here!  #
        #------------------------#
        pass




    # Helper function for Homework #3:
    # Please use this function to check if the found path is well formed.
    # 'path': An array of page IDs that stores the found path.
    #     path[0] is the start page. path[-1] is the goal page.
    #     path[0] -> path[1] -> ... -> path[-1] is the path from the start
    #     page to the goal page.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
    def assert_path(self, path, start, goal):
        assert(start != goal)
        assert(len(path) >= 2)
        assert(self.titles[path[0]] == start)
        assert(self.titles[path[-1]] == goal)
        for i in range(len(path) - 1):
            assert(path[i + 1] in self.links[path[i]])


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: %s pages_file links_file" % sys.argv[0])
        exit(1)


    #wikipedia = Wikipedia(sys.argv[1], sys.argv[2])
    wikipedia = Wikipedia('pages_small.txt', 'links_small.txt')
    path = wikipedia.find_shortest_path('B', 'D')
    print(path)

    # Example
    wikipedia.find_longest_titles()
    # Example
    wikipedia.find_most_linked_pages()
    # Homework #1
    wikipedia.find_shortest_path("渋谷", "パレートの法則")
    # Homework #2
    wikipedia.find_most_popular_pages()
    # Homework #3 (optional)
    wikipedia.find_longest_path("渋谷", "池袋")

