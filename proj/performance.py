import sys
import time
from markov import identify_speaker
from driver import read_file
import pandas as pd
import seaborn as sns

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print(
            f"Usage: python3 {sys.argv[0]} <filenameA> <filenameB> <filenameC> <max-k> <runs>"
        )
        sys.exit(1)

    # Extract parameters from command line & convert types
    filenameA, filenameB, filenameC, max_k, runs = sys.argv[1:]
    max_k = int(max_k)
    runs = int(runs)

    # Open files & read text
    speech1 = read_file(filenameA)
    speech2 = read_file(filenameB)
    speech3 = read_file(filenameC)
    
    # Run performance tests as outlined in README.md
    # Create a dataframe to store the results
    df = pd.DataFrame(columns=['Implementation', 'K', 'Run', 'Time'])
    for k in ['hashtable', 'dict']:
        if k == 'hashtable':
            hash_table = True
        else:
            hash_table = False
        for i in range(1, max_k + 1):
            for j in range(1, runs + 1):
                # run identify_speaker and time it
                start = time.perf_counter()
                tup = identify_speaker(speech1, speech2, speech3, i, use_hashtable=hash_table)
                elapsed = time.perf_counter() - start
                # add the result to the dataframe
                df = pd.concat([df, pd.DataFrame([{'Implementation': k, 'K': i, 'Run': j, 'Time': elapsed}])], \
                    ignore_index=True)
    # get the average time for each implementation and k
    average_times = df.groupby(['Implementation', 'K'])['Time'].mean().reset_index()
    
    # write execution_graph.png
    # create the graph
    graph = sns.pointplot(data=average_times, x='K', y='Time', hue='Implementation', \
        linestyles='-', markers='o')
    # set the labels and title
    graph.set_title('HashTable vs. Python dict')
    graph.set_ylabel(f'Average Time (Runs={runs})')
    max_y = max(average_times['Time'])
    # set the y-axis
    graph.set_yticks([i/4.0 for i in range(0, int(4*max_y)+1)])
    graph.get_figure().savefig('execution_graph.png')
