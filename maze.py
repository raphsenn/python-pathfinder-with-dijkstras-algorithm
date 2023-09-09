from priorityqueue import PriorityQueue, PriorityQueueItem


class Maze:
    """
    Interprete the maze as an undirected graph.

    Attributes:
        world: A 2D list representing the maze layout with 0 for walls and 1 for open paths.
        adjacency_list: A dictionary to store the adjacency list representation of the graph.
    """
    def __init__(self, world):
        """
        Initializes tow Maze object with the given Matrix layout.
        Args:
            world (list[list[int]]): A 2D list representing the maze.
        """
        self.world = world
        self.adjacency_list = {}
        rows = len(world)
        cols = len(world[0])
        for i in range(rows):
            for j in range(cols):
                node_index = cols * i + j

                if j + 1 < cols:
                    if world[i][j] != 0 and world[i][j+1] != 0:
                        if node_index not in self.adjacency_list:
                            self.adjacency_list[node_index] = [(node_index + 1, 1)]
                        else:
                            self.adjacency_list[node_index].append((node_index + 1, 1))

                if j - 1 >= 0:
                    if world[i][j-1] != 0 and world[i][j] != 0:
                        if node_index not in self.adjacency_list:
                            self.adjacency_list[node_index] = [(node_index - 1, 1)]
                        else:
                            self.adjacency_list[node_index].append((node_index - 1, 1))

                if i + 1 < rows:
                    if world[i][j] != 0 and world[i+1][j] != 0:
                        if node_index not in self.adjacency_list:
                            self.adjacency_list[node_index] = [(node_index + cols, 1)]
                        else:
                            self.adjacency_list[node_index].append((node_index + cols, 1))

                if i - 1 >= 0:
                    if world[i-1][j] != 0 and world[i][j] != 0:
                        if node_index not in self.adjacency_list:
                            self.adjacency_list[node_index] = [(node_index - cols, 1)]
                        else:
                            self.adjacency_list[node_index].append((node_index - cols, 1))

    def dijkstra(self, start, end):
        """
        Simple Implementation of the Dijkstra Algorithm for the shortest path of a directed graph.
        This Algorithm uses a self implemented PriorityQueue.

        Runtime: O(m * log(n))

        """
        costs = {v: float('inf') for v in self.adjacency_list}
        settled = {}
        costs[start] = 0
        pq = PriorityQueue()
        pq.insert(PriorityQueueItem(0, start))

        while pq.size() > 0:
            min_node = pq.get_min()
            pq.delete_min()

            if min_node.value == end:
                break

            for u, cost in self.adjacency_list[min_node.value]:
                new_cost = min_node.key + cost

                if costs[u] > new_cost:
                    costs[u] = new_cost
                    settled[u] = min_node.value
                    pq.insert(PriorityQueueItem(new_cost, u))

        if end not in settled:
            return []

        path = []
        path.append(end)
        current_node = end
        while current_node != start:
            current_node = settled[current_node]
            path.append(current_node)
        path.reverse()

        return path

    def shortest_path(self, start, end):
        """
        Computes the shortest path from node start to end using
        Dijkstra's algorithm.
        """
        path = sorted(self.dijkstra(start, end))
        if path == []:
            print("NO_PATH_EXISTS")
        new_world = self.world
        rows = len(self.world)
        cols = len(self.world[0])
        pointer_path = 0
        for i in range(rows):
            for j in range(cols):
                current_node = cols * i + j
                if pointer_path < len(path):
                    if current_node == path[pointer_path]:
                        new_world[i][j] = "#"
                        pointer_path += 1
        return new_world

    def __repr__(self):
        lst = []
        for u, adj_lst in self.adjacency_list.items():
            for v in adj_lst:
                lst.append(f"{u}->{v[0]}|{v[1]}")
        return "[" + ", ".join(lst) + "]"
