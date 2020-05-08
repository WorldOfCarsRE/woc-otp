from ai.DistributedObjectAI import DistributedObjectAI
from ai.safezone import ButterflyGlobals

from direct.distributed.ClockDelta import globalClockDelta
from direct.fsm.FSM import FSM


class DistributedButterflyAI(DistributedObjectAI, FSM):
    defaultTransitions = {
        'Off': ['Flying', 'Landed'],
        'Flying': ['Landed'],
        'Landed': ['Flying']
    }

    def __init__(self, air, playground, area, ownerId):
        DistributedObjectAI.__init__(self, air)
        FSM.__init__(self, 'DistributedButterflyAI')
        self.playground = playground
        self.area = area
        self.ownerId = ownerId
        self.stateIndex = -1
        self.curPos, self.curIndex, self.destPos, self.destIndex, self.time = ButterflyGlobals.getFirstRoute(self.playground, self.area, self.ownerId)

    def delete(self):
        ButterflyGlobals.recycleIndex(self.curIndex, self.playground, self.area, self.ownerId)
        ButterflyGlobals.recycleIndex(self.destIndex, self.playground, self.area, self.ownerId)
        self.request('Off')
        DistributedObjectAI.delete(self)

    def d_setState(self, stateIndex, curIndex, destIndex, time):
        self.sendUpdate('setState', [stateIndex, curIndex, destIndex, time, globalClockDelta.getRealNetworkTime()])

    def getArea(self):
        return [self.playground, self.area]

    def getState(self):
        return [self.stateIndex, self.curIndex, self.destIndex, self.time, globalClockDelta.getRealNetworkTime()]

    def start(self):
        self.request('Flying')
