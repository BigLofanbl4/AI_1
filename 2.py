#!/usr/bin/env python3
# -*- coding: utf-8 -*-s

import math

from utils import Node, Problem, expand


class TSP(Problem):
    # state - список уже пройденных городов (конфигурация системы)
    # action - строка, которая говорит какой город будет следующим

    def __init__(self, initial, graph):
        super().__init__(initial, goal=None)
        self.graph = graph
        self.cities_num = len(graph)

    def actions(self, state):
        # Список возможных городов для посещения
        return [
            city
            for city in self.graph[state[-1]]
            if city not in state
            or (len(state) == self.cities_num and city == state[0])
        ]

    def result(self, state, action):
        # Вернет новое состояние
        new_state = [i for i in state]
        new_state.append(action)
        return new_state

    def is_goal(self, state):
        # Посещены ли все города
        solved = True
        for city in list(self.graph.keys()):
            if city not in state:
                solved = False

        # Вернулись ли мы в начальный город
        return solved and state[-1] == state[0]

    def action_cost(self, s, a, s1):
        # Расстояние между последним городом и новым
        return self.graph[s[-1]][a]


failure = Node("failure", path_cost=math.inf)
cutoff = Node("cutoff", path_cost=math.inf)


# Для вывода оптимального пути
def path_actions(node):
    if node in (cutoff, failure, None):
        return []
    # у самого первого узла action = None, заменим этот action на стартовый город
    action = node.action if node.action is not None else node.state[0]
    return path_actions(node.parent) + [action]


def tsp_solution(initial, graph):
    problem = TSP(initial, graph)
    best_node = None
    min_cost = math.inf
    frontier = [
        Node(
            [
                initial,
            ]
        )
    ]

    while frontier:
        curr_node = frontier.pop()

        if problem.is_goal(curr_node.state):
            if curr_node.path_cost < min_cost:
                best_node = curr_node
                min_cost = curr_node.path_cost
            continue
        elif curr_node.path_cost > min_cost:
            continue

        frontier.extend(expand(problem, curr_node))

    return best_node, min_cost


if __name__ == "__main__":
    graph = {
        "Ставрополь": {
            "Александровское": 83,
            "Невинномыск": 44,
            "Изобильный": 40,
            "Пятигорск": 61,
            "Черкеск": 91,
            "Кисловодск": 56,
        },
        "Александровское": {
            "Ставрополь": 83,
            "Пятигорск": 74,
            "Черкеск": 67,
            "Невинномыск": 50,
            "Кисловодск": 90,
            "Изобильный": 81,
        },
        "Пятигорск": {
            "Александровское": 74,
            "Черкеск": 91,
            "Кисловодск": 36,
            "Ставрополь": 61,
            "Невинномыск": 78,
            "Изобильный": 82,
        },
        "Черкеск": {
            "Пятигорск": 91,
            "Невинномыск": 70,
            "Ставрополь": 84,
            "Александровское": 67,
            "Кисловодск": 55,
            "Изобильный": 63,
        },
        "Кисловодск": {
            "Пятигорск": 36,
            "Ставрополь": 56,
            "Александровское": 90,
            "Черкеск": 55,
            "Невинномыск": 48,
            "Изобильный": 71,
        },
        "Невинномыск": {
            "Ставрополь": 44,
            "Черкеск": 70,
            "Александровское": 50,
            "Пятигорск": 78,
            "Кисловодск": 48,
            "Изобильный": 39,
        },
        "Изобильный": {
            "Ставрополь": 40,
            "Александровское": 81,
            "Пятигорск": 82,
            "Черкеск": 63,
            "Кисловодск": 71,
            "Невинномыск": 39,
        },
    }

    initial_city = "Ставрополь"

    best_node, cost = tsp_solution(initial_city, graph)

    print("Оптимальный маршрут:", path_actions(best_node))
    print("Общая стоимость маршрута:", cost)
