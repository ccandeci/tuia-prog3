from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class GreedyBestFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Greedy Best First Search

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        # Initialize root node
        root = Node("", state=grid.initial, cost=0, parent=None, action=None) #creamos el nodo raíz con el estado inicial, costo 0 y sin padre ni acción
        root.estimated_distance = grid.heuristic(root)

        # Initialize reached with the initial state
        reached = {}
        reached[root.state] = root.cost

        # Initialize frontier with the root node
        frontier = PriorityQueueFrontier()
        frontier.add(root, priority=root.estimated_distance)

        while not frontier.is_empty():
            node = frontier.pop()

            if grid.objective_test(node.state):
                return Solution(node, reached)

            for action in grid.actions(node.state):
                new_state = grid.result(node.state, action)

                if new_state not in reached:
                    reached[new_state] = True
                    new_cost = node.cost + grid.individual_cost(node.state, action)
                    child = Node(action, state=new_state, cost=new_cost, parent=node, action=action)
                    child.estimated_distance = grid.heuristic(child)
                    frontier.add(child, priority=child.estimated_distance)

        return NoSolution(reached)
