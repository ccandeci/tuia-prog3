from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class AStarSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using A* Search

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        # Initialize root node
        root = Node("", state=grid.initial, cost=0, parent=None, action=None)
       
        # h(n): estimación de lo que falta desde la raíz hasta la meta (distancia Manhattan)
        root.estimated_distance = grid.heuristic(root)
        
        # Initialize reached with the initial state
        reached = {}
        reached[root.state] = root.cost

        # Initialize frontier with the root node
        frontier = PriorityQueueFrontier()
        # Prioridad de A*: f(n) = g(n) + h(n)  ->  costo ya gastado + estimación de lo que falta
        frontier.add(root, priority=root.cost + root.estimated_distance)

        while not frontier.is_empty():
            # Saco el nodo con MENOR f(n): el que parece dar el camino total más barato
            node = frontier.pop()

            # Como en UCS, el test de objetivo se hace al SACAR el nodo, no al crearlo
            if grid.objective_test(node.state):
                return Solution(node, reached)

            for action in grid.actions(node.state):
                # Estado al que llego si hago esta acción
                new_state = grid.result(node.state, action)

                # g(n) del hijo: costo del padre + costo de dar este paso
                new_cost = node.cost + grid.individual_cost(node.state, action)

                # Lo agrego si nunca lo vi, o si lo vi pero ahora llego más barato (como en UCS)
                if new_state not in reached or new_cost < reached[new_state]:
                    reached[new_state] = new_cost

                    child = Node(
                        action, state=new_state, cost=new_cost, parent=node, action=action
                    )

                    # h(n) del hijo: estimación desde su posición hasta la meta
                    child.estimated_distance = grid.heuristic(child)

                    # f(n) = g(n) + h(n): la mezcla de UCS (g) y GBFS (h)
                    frontier.add(child, priority=child.cost + child.estimated_distance)

        return NoSolution(reached)
