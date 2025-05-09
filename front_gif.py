from deap import base, creator, tools, algorithms
from deap.tools.emo import sortNondominated
import random
import glob
import matplotlib.pyplot as plt
from PIL import Image

# 個体と目的関数の設定（例）
creator.create("FitnessMulti", base.Fitness, weights=(-1.0, -1.0))
creator.create("Individual", list, fitness=creator.FitnessMulti)

toolbox = base.Toolbox()
toolbox.register("attr_float", random.random)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n=2)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evaluate(ind):
    x = ind[0]
    g = 1.0 + ind[1] * 9  # ZDT1と似た形式
    f1 = x
    f2 = g * (1.0 - (x / g)**0.5)
    return f1, f2

toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxSimulatedBinaryBounded, low=0.0, up=1.0, eta=20.0)
toolbox.register("mutate", tools.mutPolynomialBounded, low=0.0, up=1.0, eta=20.0, indpb=0.1)
toolbox.register("select", tools.selNSGA2)

# 初期集団
pop = toolbox.population(n=60)

# 初期評価
for ind in pop:
    ind.fitness.values = toolbox.evaluate(ind)

# 世代ごとのフロント保存用リスト
fronts_per_generation = []

ref_points = [1.2, 2]

NGEN = 50
for gen in range(NGEN):
    offspring = algorithms.varAnd(pop, toolbox, cxpb=0.7, mutpb=0.3)

    # 評価
    for ind in offspring:
        ind.fitness.values = toolbox.evaluate(ind)

    # 次世代選択
    pop = toolbox.select(pop + offspring, k=100)

    # パレートフロント（最上位のみ）を抽出して保存
    pareto_front = sortNondominated(pop, k=len(pop), first_front_only=True)[0]
    fronts_per_generation.append([ind.fitness.values for ind in pareto_front])

    print(f"Generation {gen}: {len(pareto_front)} individuals on the front")

# 可視化（最終世代のパレートフロント）
    fronts_per_generation[-1] = sorted(fronts_per_generation[-1], key=lambda x: x[0])
    front_hv = [f for f in fronts_per_generation[-1] if f[0] < ref_points[0] and f[1] < ref_points[1]]

    front_line = []

    for k in range(len(front_hv)-1):
        front_line.append(front_hv[k])
        front_line.append(
                [front_hv[k+1][0], front_hv[k][1]]
            )
    front_line.append(front_hv[-1])

    f1 = [f[0] for f in front_line]
    f2 = [f[1] for f in front_line]

    f1 = [ref_points[0]] + [f1[0]] + f1    + [ref_points[0]] + [ref_points[0]]
    f2 = [ref_points[1]] + [ref_points[1]] + f2 + [f2[-1]] + [ref_points[1]]

    plt.cla()
    plt.fill(f1, f2, color='lightsteelblue')
    plt.plot(f1, f2, linewidth=0.8)

    f1 = [f[0] for f in fronts_per_generation[-1]]
    f2 = [f[1] for f in fronts_per_generation[-1]]

    plt.scatter(f1, f2, color="darkblue", zorder=2)
    plt.scatter(ref_points[0], ref_points[1], marker="*", color="darkred", zorder=2)

    plt.title(f"Generation {gen}")
    plt.xlabel("Objective 1")
    plt.ylabel("Objective 2")
    plt.xlim(-0.05, 1.25)
    plt.ylim(-0.1, 2.3)
    plt.grid(True)

    plt.savefig(f"{gen}")


image_paths = sorted(glob.glob("*.png"), key=lambda x : int(x.split(".")[0]))

# 画像を開く
images = [Image.open(image_path) for image_path in image_paths]

# GIFを作成
images[0].save(
    "movie.gif",
    save_all=True,
    append_images=images[1:],
    duration=300,  # フレームの表示時間 (ミリ秒)
    loop=0  # 0は無限ループ
)

