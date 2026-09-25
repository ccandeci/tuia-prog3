from ..models.grid import Grid
from ..models.frontier import QueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class BreadthFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Breadth First Search

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        # Initialize root node
        root = Node("", state=grid.initial, cost=0, parent=None, action=None)

        # Apply objective test
        
        if grid.objective_test(root.state):
            return Solution(root, reached)
        # inicializo la frontera y agrego a la frontera la raiz
        frontier=QueueFrontier()
        frontier.add(root)
        # Initialize alcanzados con el estado original
        reached = {}
        reached[root.state] = True
              
        while True:
            if frontier.is_empty():
                return NoSolution(reached)
            nodo=frontier.remove()

            for action in grid.actions(nodo.state):
                succesor=grid.result(nodo.state,action)
                if succesor not in reached:
                    son = Node( "",state=succesor, cost=nodo.cost + grid.individual_cost(nodo.state, action),parent=nodo, action=action)                                       
                                        
                    if grid.objective_test(succesor):
                        return Solution(son, reached)
                    reached[succesor]=True
                    frontier.add(son)