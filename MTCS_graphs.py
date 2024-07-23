import matplotlib.pyplot as plt
import bot_Runner as b
import threading
import concurrent.futures
import time
def plot_graphs(graphs):
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))

    for i, graph in enumerate(graphs):
        ax = axs[i // 2, i % 2]

        if graph['type'] == 'line':
            ax.plot(graph['x'], graph['y'])
        elif graph['type'] == 'bar':
            ax.bar(graph['x'], graph['y'])
        elif graph['type'] == 'scatter':
            ax.scatter(graph['x'], graph['y'])
        elif graph['type'] == 'hist':
            ax.hist(graph['y'], bins=graph.get('bins', 10))

        ax.set_title(graph['title'])
        ax.set_xlabel(graph['x_label'])
        ax.set_ylabel(graph['y_label'])

    plt.tight_layout()
    plt.show()

start=time.time()

results_list = []

def worker(thread_id, run_id):
    result = b.runBotUTC(thread_id, run_id)
    results_list.append(result)

def worker1(thread_id, run_id):
    result = b.runBotUTC_Ran(thread_id, run_id)
    results_list.append(result)

def submit_for_thread(method,total_runs=6,num_threads=3):
    threads = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        for run_id in range(total_runs):
            futures.append(executor.submit(method, run_id % num_threads, run_id))

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


#data
graphs = [
    {
        'type': 'bar',
        'title': 'mc vs mc',
        'x_label': 'X-axis',
        'y_label': 'Y-axis',
        'x': x1,
        'y': y1
    },
    {
        'type': 'bar',
        'title': 'mc vs random',
        'x_label': 'X-axis',
        'y_label': 'Y-axis',
        'x': x2,
        'y': y2
    },
    {
        'type': 'scatter',
        'title': 'Scatter Plot',
        'x_label': 'X-axis',
        'y_label': 'Y-axis',
        'x': [1, 2, 3, 4, 5],
        'y': [5, 4, 3, 2, 1]
    },
    {
        'type': 'hist',
        'title': 'Histogram',
        'x_label': 'Value',
        'y_label': 'Frequency',
        'x': [],  # Histograms don't need x data
        'y': [1, 2, 2, 3, 3, 3, 4, 4, 4, 4],
        'bins': 4
    }
]

end=time.time()
print("total time = "+str(end-start))
plot_graphs(graphs)
