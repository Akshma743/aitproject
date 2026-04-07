import heapq
from collections import deque
import tkinter as tk
from tkinter import messagebox

# -------- Graph --------
graph = {
    'A': {'B': 5, 'C': 10},
    'B': {'A': 5, 'C': 3, 'D': 7},
    'C': {'A': 10, 'B': 3, 'D': 1},
    'D': {'B': 7, 'C': 1, 'E': 2},
    'E': {'D': 2}
}

heuristic = {'A':7,'B':6,'C':2,'D':1,'E':0}

# Node positions (for drawing)
pos = {
    'A': (100, 100),
    'B': (250, 50),
    'C': (250, 150),
    'D': (400, 100),
    'E': (550, 100)
}

# -------- Algorithms --------
def bfs(start, goal):
    queue = deque([(start, [start])])
    visited = set()
    while queue:
        node, path = queue.popleft()
        if node == goal:
            return path
        visited.add(node)
        for n in graph[node]:
            if n not in visited:
                queue.append((n, path+[n]))
    return None

def dfs(start, goal):
    stack = [(start, [start])]
    visited = set()
    while stack:
        node, path = stack.pop()
        if node == goal:
            return path
        visited.add(node)
        for n in graph[node]:
            if n not in visited:
                stack.append((n, path+[n]))
    return None

def a_star(start, goal):
    pq = [(heuristic[start], 0, start, [start])]
    visited = set()
    while pq:
        f, cost, node, path = heapq.heappop(pq)
        if node == goal:
            return path, cost
        if node in visited:
            continue
        visited.add(node)
        for n in graph[node]:
            g = cost + graph[node][n]
            h = heuristic[n]
            heapq.heappush(pq, (g+h, g, n, path+[n]))
    return None, float('inf')

def hill(start, goal):
    current = start
    path = [current]
    visited = set([current])
    while current != goal:
        next_node = None
        best = float('inf')
        for n in graph[current]:
            if n not in visited and heuristic[n] < best:
                best = heuristic[n]
                next_node = n
        if next_node is None:
            return path
        current = next_node
        path.append(current)
        visited.add(current)
    return path

# -------- Draw Graph --------
def draw_graph(path=None):
    canvas.delete("all")

    # Draw edges
    for u in graph:
        for v in graph[u]:
            x1,y1 = pos[u]
            x2,y2 = pos[v]
            canvas.create_line(x1,y1,x2,y2,fill="gray",width=2)

    # Highlight path
    if path:
        for i in range(len(path)-1):
            x1,y1 = pos[path[i]]
            x2,y2 = pos[path[i+1]]
            canvas.create_line(x1,y1,x2,y2,fill="red",width=4)

    # Draw nodes
    for node,(x,y) in pos.items():
        canvas.create_oval(x-20,y-20,x+20,y+20,fill="#2563eb")
        canvas.create_text(x,y,text=node,fill="white",font=("Arial",12,"bold"))

# -------- Button Actions --------
def get_nodes():
    s = start_entry.get().upper()
    g = goal_entry.get().upper()
    if s not in graph or g not in graph:
        messagebox.showerror("Error","Enter A-E only")
        return None,None
    return s,g

def run_algo(algo):
    s,g = get_nodes()
    if not s:
        return

    if algo == "BFS":
        path = bfs(s,g)
    elif algo == "DFS":
        path = dfs(s,g)
    elif algo == "A*":
        path,_ = a_star(s,g)
    elif algo == "Hill":
        path = hill(s,g)
    else:
        bfs_p = bfs(s,g)
        dfs_p = dfs(s,g)
        a_p,a_c = a_star(s,g)
        h_p = hill(s,g)

        costs = {
            "BFS": len(bfs_p),
            "DFS": len(dfs_p),
            "A*": a_c,
            "Hill": len(h_p)
        }
        best = min(costs, key=costs.get)
        path = {"BFS":bfs_p,"DFS":dfs_p,"A*":a_p,"Hill":h_p}[best]

    draw_graph(path)
    result.set(f"{algo} Path: {path}")

# -------- GUI --------
root = tk.Tk()
root.title("Smart Route Visualizer")
root.geometry("650x500")
root.config(bg="#0f172a")

tk.Label(root,text="SMART ROUTE VISUALIZER",
         fg="white",bg="#0f172a",
         font=("Arial",16,"bold")).pack(pady=10)

start_entry = tk.Entry(root)
start_entry.pack()
start_entry.insert(0,"A")

goal_entry = tk.Entry(root)
goal_entry.pack()
goal_entry.insert(0,"E")

frame = tk.Frame(root,bg="#0f172a")
frame.pack(pady=10)

for i,algo in enumerate(["BFS","DFS","A*","Hill","Best"]):
    tk.Button(frame,text=algo,width=8,
              command=lambda a=algo: run_algo(a),
              bg="#2563eb",fg="white").grid(row=0,column=i,padx=5)

canvas = tk.Canvas(root,width=600,height=250,bg="white")
canvas.pack(pady=10)

result = tk.StringVar()
tk.Label(root,textvariable=result,
         bg="#1e293b",fg="white",
         width=60,height=2).pack()

draw_graph()
root.mainloop()