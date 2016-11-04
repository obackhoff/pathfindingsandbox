from abc import ABCMeta, abstractmethod
import math

class AbstractHeap():

    __metaclass__ = ABCMeta

    @abstractmethod
    def push(self):
        pass

    @abstractmethod
    def pop(self):
        pass

    @abstractmethod
    def pushpop(self):
        pass

    @abstractmethod
    def heapify(self):
        pass

    @abstractmethod
    def heapreplace(self):
        pass

    @abstractmethod
    def checkIfEmpty(self):
        pass


class AbstractHeapObject():

    __metaclass_ = ABCMeta

    @abstractmethod
    def __lt__(self, other):
        pass


class NodeObjectWrapper(AbstractHeapObject):

    def __init__(self, nodeObject):
        self.nodeObject = nodeObject
        self.index = -1

    def getNodeObject(self):
        return self.nodeObject

    def __lt__(self, other):
        selfNodeObject = self.nodeObject
        otherNodeObject = other.nodeObject
        fCostSelf = selfNodeObject.fCost()
        fCostOther = otherNodeObject.fCost()
        hCostSelf = selfNodeObject.hCost
        hCostOther = otherNodeObject.hCost

        return fCostSelf < fCostOther or fCostSelf == fCostOther and hCostSelf < hCostOther


class ListObjectHeap(AbstractHeap):

    def __init__(self):
        self.l = []

    def push(self, pushObject):
        self.l.append(pushObject)
        pushIndex = len(self.l) - 1
        pushObject.index = pushIndex
        self.sortUp(pushIndex)

    def pop(self):
        if not self.l:
            print(("ERROR: Not possible to pop element from the heap because "
                   "the heap is empty!"))
            return
        popObject = self.l[0]
        if len(self.l) == 1:
            self.l.pop()
            return popObject
        lastObject = self.l[-1]
        self.l[0] = lastObject
        self.l.pop()
        self.sortDown(0)
        return popObject

    def pushpop(self, pushObject):
        self.push(pushObject)
        self.pop()

    def heapify(self, inputList):
        for x in inputList:
            self.push(x)

    def heapreplace(self, pushObject):
        self.pop()
        self.push(pushObject)

    def getParentIndex(self, childIndex):
        if childIndex == 0:
            print (("ERROR: Cannot return parent because the corresponding"
                    "heapObject is at the top of the heap!"))
            return
        parentIndex = math.floor((childIndex - 1) / 2)
        return parentIndex

    def getChildIndexes(self, parentIndex):
        leftChildIndex = 2 * parentIndex + 1
        rightChildIndex = 2 * parentIndex + 2

        if leftChildIndex > len(self.l) - 1:
            leftChildIndex = -1
        if rightChildIndex > len(self.l) - 1:
            rightChildIndex = -1

        return (leftChildIndex, rightChildIndex)

    def swapElements(self, elementIndex1, elementIndex2):
        temp = self.l[elementIndex1]
        self.l[elementIndex1] = self.l[elementIndex2]
        self.l[elementIndex1].index = elementIndex1
        self.l[elementIndex2] = temp
        self.l[elementIndex2].index = elementIndex2

    def compareElements(self, elementIndex1, elementIndex2):
        value1 = self.l[elementIndex1][1::]
        value2 = self.l[elementIndex2][1::]
        if value1[0] != value2[0]:
            if value1[0] > value2[0]:
                return 2
            else:
                return 1
        else:
            if value1[1] > value2[1]:
                return 2
            else:
                return 1

    def checkIfEmpty(self):
        if not self.l:
            return True
        else:
            return False

    def sortUp(self, sortIndex):
        sortObject = self.l[sortIndex]
        while True:
            if sortIndex == 0:
                return
            parentIndex = self.getParentIndex(sortIndex)
            parent = self.l[parentIndex]
            if sortObject < parent:
                self.swapElements(parentIndex, sortIndex)
                sortIndex = parentIndex
            else:
                return

    def sortDown(self, sortIndex):
        sortObject = self.l[sortIndex]
        while True:
            [leftChildIndex, rightChildIndex] = self.getChildIndexes(sortIndex)
            if leftChildIndex == -1 and rightChildIndex == -1:
                break
            elif leftChildIndex == -1 and rightChildIndex != -1:
                rightChild = self.l[rightChildIndex]
                if rightChild < sortObject:
                    self.swapElements(sortIndex, rightChildIndex)
                    break
                else:
                    break
            elif leftChildIndex != -1 and rightChildIndex == -1:
                leftChild = self.l[leftChildIndex]
                if leftChild < sortObject:
                    self.swapElements(sortIndex, leftChildIndex)
                    break
                else:
                    break
            else:
                leftChild = self.l[leftChildIndex]
                rightChild = self.l[rightChildIndex]
                if leftChild < rightChild:
                    if leftChild < sortObject:
                        self.swapElements(sortIndex, leftChildIndex)
                        sortIndex = leftChildIndex
                    else:
                        break
                else:
                    if rightChild < sortObject:
                        self.swapElements(sortIndex, rightChildIndex)
                        sortIndex = rightChildIndex
                    else:
                        break

    def updateHeap(self, o):
        self.sortUp(o)