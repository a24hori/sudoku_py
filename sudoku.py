# 'sudoku.py' created by keith1994
# 目的：数独を数理最適化手法で解く（pulpの動作テストおよび学習のためのプログラム程度で作成）
# データ：81文字のテキストデータ（空欄は'.'とする）
# 変数 x[i][j][k] (i,j,k=1,...,9)：行i列jに数kを書き込むか否か（バイナリ変数）
# ------------------------------------------------------------------------------

# pulpライブラリを読み込む
import pulp

# データセット（テストデータ）
dataset = ".94...13..............76..2.8..1.....32.........2...6.....5.4.......8..7..63.4..8"
# 一文字ずつリストとして格納する
datalist = list(dataset)

# 数字データ
numset = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

# 添字集合
I = range(0, 9)
J = range(0, 9)
K = range(0, 9)

# 問題'Sudoku'の定義
prob = pulp.LpProblem('Sudoku', pulp.LpMinimize)
# 変数の宣言
x = pulp.LpVariable.dicts("x", (I, J, K), 0, 1, pulp.LpInteger)
# 目的関数（すべての変数の和が81となるかどうか）
#prob += pulp.lpSum(x)

# ボードリストの定義
board = [[0 for i in I]for j in J]
# 問題データをリシェイプしてボードリストboardに代入
for i in I:
    for j in J:
        if datalist[9*i+j] in numset:
            board[i][j] = int(datalist[9*i+j])

# 求解前のボードを表示
print("+++ Problem data +++")
for i in I:
    for j in J:
        print("%2d" % board[i][j], end='')
    print()

# 所与の値は固定する
for i in I:
    for j in J:
        if str(board[i][j]) in numset:
            prob += x[i][j][board[i][j]-1] == 1

# (i,j)成分にひとつある値kが入る
for i in I:
    for j in J:
        prob += pulp.lpSum([x[i][j][k] for k in K]) == 1

# 行iに関して値kが現れるのは1度のみ
for i in I:
    for k in K:
        prob += pulp.lpSum([x[i][j][k] for j in J]) == 1

# 列jに関して値kが現れるのは1度のみ
for j in J:
    for k in K:
        prob += pulp.lpSum([x[i][j][k] for i in I]) == 1

# 所定の9マス（3*3マス）で値kが現れるのは1度のみ
for i in [0,3,6]:
    for j in [0,3,6]:
        for k in K:
            prob += pulp.lpSum([x[i+p][j+q][k] for p in range(0,3) for q in range(0,3)]) == 1

# 所与の数独を解く
status = prob.solve()

# 求解後のボードを表示
print("+++ Solved data +++")
for i in I:
    for j in J:
        for k in K:
            if x[i][j][k].value() == 1:
                print("%2d" % (k+1), end='')
    print()

# END program