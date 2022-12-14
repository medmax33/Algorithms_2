class BSTNode:

    def __init__(self, key, val, parent):
        self.NodeKey = key  # ключ узла
        self.NodeValue = val  # значение в узле
        self.Parent = parent  # родитель или None для корня
        self.LeftChild = None  # левый потомок
        self.RightChild = None  # правый потомок

    def __str__(self):
        return f"TreeNode({self.NodeKey} - {self.NodeValue})"


class BSTFind:  # промежуточный результат поиска

    def __init__(self, node):
        self.Node = node  # None если в дереве вообще нету узлов
        self.NodeHasKey = False  # True если узел найден
        self.ToLeft = False  # True, если родительскому узлу надо добавить новый узел левым потомком


class BST:

    def __init__(self, node):
        self.Root = node  # корень дерева, или None

        # инициализируем счетчик узлов
        if self.Root:
            self.count = 1
        else:
            self.count = 0

    def FindNodeByKey(self, key):
        # ищем в дереве узел и сопутствующую информацию по ключу
        # создаем первый узел поиска = корневому узлу
        current_node = BSTFind(self.Root)

        return self.BSTFind_by_key(key, current_node)

    def BSTFind_by_key(self, key, node):
        # если дерево пустое, результат None
        if node.Node is None:
            return node

        # проверка NodeKey == key
        if node.Node.NodeKey == key:
            node.NodeHasKey = True
            return node

        # проверка NodeKey < key
        if node.Node.NodeKey > key:
            if node.Node.LeftChild is None:
                node.ToLeft = True
                return node
            node.Node = node.Node.LeftChild

        # проверка NodeKey > key
        if node.Node.NodeKey < key:
            if node.Node.RightChild is None:
                return node
            node.Node = node.Node.RightChild

        # рекурсивно запускаем FindNodeByKey
        return self.BSTFind_by_key(key, node)

    def AddKeyValue(self, key, val):
        # добавляем ключ-значение в дерево
        if self.Root is None:
            self.Root = BSTNode(key, val, None)
        else:
            current_node = self.FindNodeByKey(key)
            if current_node.NodeHasKey:
                return False  # если ключ уже есть
            if current_node.ToLeft:
                current_node.Node.LeftChild = BSTNode(key, val, current_node.Node)
            else:
                current_node.Node.RightChild = BSTNode(key, val, current_node.Node)
        self.count += 1
        return True

    def FinMinMax(self, from_node, find_max):
        # ищем максимальный/минимальный ключ в поддереве
        # возвращается объект типа BSTNode
        if from_node is None:
            from_node = self.Root
        if find_max is True:
            if from_node.RightChild is None:
                return from_node
            from_node = from_node.RightChild
        elif find_max is False:
            if from_node.LeftChild is None:
                return from_node
            from_node = from_node.LeftChild

        return self.FinMinMax(from_node, find_max)

    def DeleteNodeByKey(self, key):
        # удаляем узел по ключу
        # если узел не найден, возвращаем False
        if self.FindNodeByKey(key).NodeHasKey is False:
            return False

        self.Root = self.delete_recursion(self.Root, key)
        self.count -= 1
        return True

    def Count(self):
        return self.count  # количество узлов в дереве

    def delete_recursion(self, root, key):  # node,
        if root is None:
            return root
        if key < root.NodeKey:
            root.LeftChild = self.delete_recursion(root.LeftChild, key)
        elif key > root.NodeKey:
            root.RightChild = self.delete_recursion(root.RightChild, key)
        elif root.LeftChild is not None and root.RightChild is not None:
            average = self.FinMinMax(root.RightChild, False)
            root.NodeKey = average.NodeKey
            root.NodeValue = average.NodeValue
            root.RightChild = self.delete_recursion(root.RightChild, root.NodeKey)
        else:
            if root.LeftChild is not None:
                root.LeftChild.Parent = root.Parent
                root = root.LeftChild
            elif root.RightChild is not None:
                root.RightChild.Parent = root.Parent
                root = root.RightChild
            else:
                root = None
        return root

    def DeepAllNodes(self, order: int) -> tuple:
        all_nodes = []
        node = self.Root
        if order == 0:
            self.in_order(node, all_nodes)
        elif order == 1:
            self.post_order(node, all_nodes)
        elif order == 2:
            self.pre_order(node, all_nodes)
        all_nodes = tuple(all_nodes)
        return all_nodes

    def in_order(self, node: BSTNode, all_nodes: list) -> list:
        if node is None:
            return node
        if node.LeftChild:
            self.in_order(node.LeftChild, all_nodes)
        all_nodes.append(node)
        if node.RightChild:
            self.in_order(node.RightChild, all_nodes)

    def post_order(self, node: BSTNode, all_nodes: list) -> list:
        if node is None:
            return node
        if node.LeftChild:
            self.post_order(node.LeftChild, all_nodes)
        if node.RightChild:
            self.post_order(node.RightChild, all_nodes)
        all_nodes.append(node)

    def pre_order(self, node: BSTNode, all_nodes: list) -> list:
        if node is None:
            return node
        all_nodes.append(node)
        if node.LeftChild:
            self.pre_order(node.LeftChild, all_nodes)
        if node.RightChild:
            self.pre_order(node.RightChild, all_nodes)

    # служебная функция для печати всего дерева in-order
    def PrintTree(self, node):
        # печать всего дерева вглубину
        if self.Root is None:
            print('empty')
            return False
        if node is None:
            node = self.Root
        if node.LeftChild:
            self.PrintTree(node.LeftChild)
        print(node)
        if node.RightChild:
            self.PrintTree(node.RightChild)

    def WideAllNodes(self) -> tuple:
        nodes_visited = []
        nodes_queue = [self.Root]
        while nodes_queue:
            node_current = nodes_queue.pop(0)
            nodes_visited.append(node_current)
            if node_current.LeftChild:
                nodes_queue.append(node_current.LeftChild)
            if node_current.RightChild:
                nodes_queue.append(node_current.RightChild)
        nodes_visited = tuple(nodes_visited)
        return nodes_visited
