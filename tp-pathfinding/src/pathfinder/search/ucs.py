from platform import node

from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node

#En UCS el chequeo de objetivo se hace al sacar el nodo de la frontera, no al crearlo:
#recién ahí tenés la garantía de que es el camino más barato posible hasta ese estado.

class UniformCostSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Uniform Cost Search

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        # Initialize root node
        root = Node("", state=grid.initial, cost=0, parent=None, action=None)

        # Initialize reached with the initial state
        reached = {}
        reached[root.state] = root.cost

        # Initialize frontier with the root node
        frontier = PriorityQueueFrontier()
        frontier.add(root, priority=root.cost) #Guarda el mejor costo conocido para llegar a cada estado

        while not frontier.is_empty():
            node = frontier.pop()
            #el test de objetivo se hace apenas lo sacamos, no antes
            if grid.objective_test(node.state):
                return Solution(node, reached)
            
            for action in grid.actions(node.state):
                new_state = grid.result(node.state, action)
                new_cost = node.cost + grid.individual_cost(node.state, action)
        
            #Recorro los vecinos, con esta condición: nunca lo vi, o lo vi pero por un camino más caro que este?
                if new_state not in reached or new_cost < reached[new_state]:
                    reached[new_state] = new_cost
                    child = Node(action, state=new_state, cost=new_cost, parent=node, action=action)
                    frontier.add(child, priority=new_cost)

        return NoSolution(reached)
