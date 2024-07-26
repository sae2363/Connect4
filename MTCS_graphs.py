import matplotlib.pyplot as plt
import bot_Runner as b
import threading
import concurrent.futures
import time,math
def plot_graphs(graphs):
    n = len(graphs)
    cols = math.ceil(math.sqrt(n))
    rows = math.ceil(n / cols)
    fig, axs = plt.subplots(rows, cols, figsize=(cols * 5, rows * 4))
    
    # Flatten axs array if more than one row or column
    if rows > 1 and cols > 1:
        axs = axs.flatten()
    elif rows == 1 or cols == 1:
        axs = [axs] if n == 1 else axs

    colors = ['blue', 'orange']

    for i, graph in enumerate(graphs):
        ax = axs[i]

        if graph['type'] == 'line':
            ax.plot(graph['x'], graph['y'])
        elif graph['type'] == 'bar':
            ax.bar(graph['x'], graph['y'])
        elif graph['type'] == 'bar2':
            bars = ax.bar(graph['x'], graph['y'])
            for j, bar in enumerate(bars):
                bar.set_color(colors[j % len(colors)]) 
        elif graph['type'] == 'scatter':
            ax.scatter(graph['x'], graph['y'])
        elif graph['type'] == 'hist':
            ax.hist(graph['y'], bins=graph.get('bins', 10))

        ax.set_title(graph.get('title', ''))
        ax.set_xlabel(graph.get('x_label', ''))
        ax.set_ylabel(graph.get('y_label', ''))

    # Hide any unused subplots
    for i in range(len(graphs), len(axs)):
        fig.delaxes(axs[i])
        
    plt.tight_layout()
    plt.show()

def average_at_indices(lists):
    max_length = max(len(lst) for lst in lists)
    sums = [0] * max_length
    counts = [0] * max_length

    for lst in lists:
        for i, value in enumerate(lst):
            sums[i] += value
            counts[i] += 1

    averages = [sums[i] / counts[i] for i in range(max_length)]
    return averages

start=time.time()

results_list = []
timeList=[]
def worker():
    result = b.runBotUTC()
    results_list.append(result)

def worker1():
    result = b.runBotUTC_Ran()
    results_list.append(result)
def worker2():
    result = b.runBotUTC_ab()
    results_list.append(result)
def worker3():
    result = b.runBotab_ran()
    results_list.append(result)
def worker4():
    result,timeListOfMove = b.runBotab_MCTS_Time()
    timeList.append(timeListOfMove)
    results_list.append(result)
def worker5():
    result,timeListOfMove = b.runBotMCTS_MCTS_Time()
    timeList.append(timeListOfMove)
    results_list.append(result)

def submit_for_thread(method,total_runs=16,num_threads=4):
    threads = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        for run_id in range(total_runs):
            futures.append(executor.submit(method))

        # Ensure all futures are completed
        concurrent.futures.wait(futures)
results_list = []
submit_for_thread(worker)
#win rate of utc vs utc 
x1=["Draw","P1_Win","P2_Win"]
y1=[0,0,0]
for i in results_list:
    y1[i]+=1
results_list = []

submit_for_thread(worker1)
#win rate of utc vs random 
x2=["Draw","P1_Win","P2_Win"]
y2=[0,0,0]
for i in results_list:
    y2[i]+=1
results_list = []
submit_for_thread(worker2)
#win rate of utc vs AB 
x3=["Draw","P1_Win","P2_Win"]
y3=[0,0,0]
for i in results_list:
    y3[i]+=1
results_list = []
submit_for_thread(worker3)
#win rate of AB vs random 
x4=["Draw","P1_Win","P2_Win"]
y4=[0,0,0]
for i in results_list:
    y4[i]+=1
results_list = []

submit_for_thread(worker4)
# x is move number y is time
x5=[]
y5=[]

y5=average_at_indices(timeList)
for i in range(len(y5)):
    x5.append(i)

results_list = []
timeList=[]
submit_for_thread(worker5)
# x is move number y is time 
x6=[]
y6=[]
y6=average_at_indices(timeList)
for i in range(len(y6)):
    x6.append(i)
for i in results_list:
    y6[i]+=1


#data
graphs = [
    {
        'type': 'bar',
        'title': 'mc vs mc',
        'x_label': 'Player',
        'y_label': 'Win Count',
        'x': x1,
        'y': y1
    },
    {
        'type': 'bar',
        'title': 'mc vs random',
        'x_label': 'Player',
        'y_label': 'Win Count',
        'x': x2,
        'y': y2
    },
    {
        'type': 'bar',
        'title': 'mc vs ab',
        'x_label': 'Player',
        'y_label': 'Win Count',
        'x': x3,
        'y': y3
    },
    {
        'type': 'bar',
        'title': 'ab vs random',
        'x_label': 'Player',
        'y_label': 'Win Count',
        'x': x4,  
        'y': y4
    },
    {
        'type': 'bar2',
        'title': 'ab over time vs MCTS',
        'x_label': 'Move number overall',
        'y_label': 'Time for Move',
        'x': x5,
        'y': y5
    },
    {
        'type': 'bar',
        'title': 'MCTS over time vs MCTS',
        'x_label': 'Move number overall',
        'y_label': 'Time for Move',
        'x': x6,  
        'y': y6
    }
]

end=time.time()
print("total time = "+str(end-start))
plot_graphs(graphs)
