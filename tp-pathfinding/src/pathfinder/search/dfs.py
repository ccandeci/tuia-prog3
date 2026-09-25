from ..models.grid import Grid
from ..models.frontier import StackFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class DepthFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Depth First Search

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        # Creamos el nodo raíz
        root = Node("", state=grid.initial, cost=0, parent=None, action=None)

        # Si el punto de partida ya es la meta, listo
        if grid.objective_test(root.state):
            return Solution(root, {})

        # Acá guardamos los nodos ya expandidos
        expanded = dict()

        # La frontera es una pila (Stack LIFO)
        frontier = StackFrontier()
        frontier.add(root)

        while not frontier.is_empty():
            # Sacamos el nodo que está arriba de la pila
            node = frontier.remove()

            # Si este estado ya lo expandimos antes, lo salteamos
            if node.state in expanded:
                continue

            # Marcamos este estado como expandido
            expanded[node.state] = True

            # Recorremos todas las acciones posibles desde acá (arriba, abajo, izq, der)
            for action in grid.actions(node.state):
                new_state = grid.result(node.state, action)

                # Si el vecino no fue expandido todavía, lo consideramos
                if new_state not in expanded:
                    cost = node.cost + grid.individual_cost(node.state, action)
                    child = Node(action, state=new_state, cost=cost, parent=node, action=action)

                    # Chequeamos si este vecino ya es la meta
                    if grid.objective_test(new_state):
                        return Solution(child, expanded)

                    # Si no es la meta, lo metemos en la pila para revisarlo después
                    frontier.add(child)

        # Si se vació la pila y no encontramos la meta, no hay solución
        return NoSolution(expanded)