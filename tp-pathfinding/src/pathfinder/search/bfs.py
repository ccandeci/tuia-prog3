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
        # inicializo frontera y agrego a frontera la raiz
        frontier=QueueFrontier()
        frontier.add(root)
        # Initializo alcanzados al estado original
        reached = {}
        reached[root.state] = True

        # Mientras que la frontera no este vacia
        while True:
            if frontier.is_empty(): 
                return NoSolution(reached) # Devuelvo NoSolution
            nodo=frontier.remove() # Borro el nodo de la frontera

            for action in grid.actions(nodo.state): # Recorre las acciones posibles del nodo.
                succesor=grid.result(nodo.state,action) # 
                if succesor not in reached: # Si sucesor no lo tengo en alconzados, lo agrego a la frontera y a alcanzados
                    son = Node( "",state=succesor, cost=nodo.cost + grid.individual_cost(nodo.state, action),parent=nodo, action=action)                                       
                                        
                    if grid.objective_test(succesor): # Si el sucesor que acabamos de generar es el objetivo, devolvemos la solucion
                        return Solution(son, reached)
                    reached[succesor]=True # Si no es el objetivo, lo agrego a alcanzados
                    frontier.add(son) # También lo agrego en la frontera para seguir expandiendo