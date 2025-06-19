## 結果　Result
  ### 宿題１ Homework1
 最短経路が複数ある時と、一個だけ探せばいい時で回答が違う。初めのコードとそれらの比較を'homework4-1_comparision.py'にいれました。
 
はじめに3で解いてみたが、オフィスアワーで


*   メモリを多く使っている
*   最短経路を複数調べなくてもいい

と言われたので両方のverでデバッグ



### **1.   最短経路が一つ見つかればそれでおしまい（goalが見つかったらgoalからstartまで逆戻り）**

`previous_node = {'A':None, 'B':'A', 'C':'B','E':'C'}`

のように現在のノード`current`とその一個前の`node`を保存していって`goal`に辿り着いたら`previous_node`を逆から辿って経路の逆向きを保存 → `reverse()`

### **2.   同じ長さの最短経路を全て上げる（再帰で最短経路を再構成）**
ベースのアルゴリズムは1.と同じで「訪問済みと前のノードだけ覚えて、最後に逆算」

→効率的・大規模グラフによい

### **3.   同じ長さの最短経路を全て上げる(経路を全て保存しておく)**

`queue = ((current: [start, ・・・current]))` のように今のノードとそのノードが辿って来た道を記録。currentがgoalになった時、visitedの値のリストの長さが短いものの経路を返す。

**よくない点：**


*   全部の経路を保存しているからメモリを使う
*   大規模なデータの探索には向かない

**結果**
` ['渋谷', 'マクドナルド', 'Twitter', 'パレートの法則']`

 
  ### 宿題2 Homework1
  **small**

    Iteration 3: total rank sum = 6.000000
    Iteration 3: diff = 0.008348

    **Top 10 popular pages**
    
    C (score: 1.3347)
    D (score: 1.3347)
    B (score: 1.1647)
    E (score: 0.8566)
    F (score: 0.8566)
    A (score: 0.4528)


  **medium**

    Iteration 26: total rank sum = 631853.000000
    Iteration 26: diff = 0.007329

    *Top 10 popular pages*
    
    英語 (score: 1507.2838)
    ISBN (score: 959.7011)
    2006年 (score: 526.1046)
    2005年 (score: 502.2639)
    2007年 (score: 491.4850)
    東京都 (score: 480.2768)
    昭和 (score: 459.3787)
    2004年 (score: 445.3724)
    2003年 (score: 404.7407)
    2000年 (score: 401.8920)
  
  **large**

    Iteration 32: total rank sum = 2215900.000000
    Iteration 32: diff = 0.007233

    *Top 10 popular pages*

    英語 (score: 4576.8147)
    日本 (score: 4569.2297)
    VIAF_(識別子) (score: 3806.8221)
    バーチャル国際典拠ファイル (score: 3320.3689)
    アメリカ合衆国 (score: 2714.5335)
    ISBN (score: 2711.5198)
    ISNI_(識別子) (score: 2060.6638)
    国際標準名称識別子 (score: 1865.4494)
    地理座標系 (score: 1815.8507)
    SUDOC_(識別子) (score: 1518.7878)


### 宿題3
doing
