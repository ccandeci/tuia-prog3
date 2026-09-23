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

        # Initialize reached with the initial state
        reached = {}
        reached[root.state] = True

        # Initialize frontier with the root node
        frontier = QueueFrontier()
        frontier.add(root)
        while not frontier.is_empty():
            node = frontier.remove()

            if grid.objective_test(node.state):
                return Solution(node, reached)

            for action in grid.actions(node.state):
                state = grid.result(node.state, action)

                if state not in reached:
                    reached[state] = True

                    child = Node(
                        action,
                        state=state,
                        cost=node.cost + 1,
                        parent=node,
                        action=action
                    )

                    frontier.add(child)

        return NoSolution(reached)