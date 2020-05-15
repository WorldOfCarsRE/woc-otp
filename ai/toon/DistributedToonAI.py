from ai.DistributedObjectAI import DistributedObjectAI
from ai.DistributedSmoothNodeAI import DistributedSmoothNodeAI
from otp.util import getPuppetChannel
from dc.util import Datagram


class DistributedAvatarAI(DistributedSmoothNodeAI):
    def __init__(self, air):
        DistributedSmoothNodeAI.__init__(self, air)

        self.name = 'Toon'

    def setName(self, name):
        self.name = name

    def getName(self):
        return 'Toon'


class DistributedPlayerAI(DistributedAvatarAI):
    def __init__(self, air):
        DistributedAvatarAI.__init__(self, air)

        self.accountName = ''
        self.DISLid = 0
        self.access = 0

    def setAccountName(self, name):
        self.accountName = name

    def getAccountName(self):
        return self.accountName

    def getFriendsList(self):
        return []

    def setDISLid(self, DISLid):
        self.DISLid = DISLid

    def getDISLid(self):
        return self.DISLid

    def getPreviousAccess(self):
        # AccessFull = 2
        return 2

    def setAccess(self, access):
        self.access = access

    def getAccess(self):
        return self.access

    def getAsGM(self):
        return False


class DistributedToonAI(DistributedPlayerAI):
    STREET_INTEREST_HANDLE = (1 << 15) + 1

    def __init__(self, air):
        DistributedPlayerAI.__init__(self, air)

        self.dnaString = ''
        self.hp = 15
        self.maxHp = 15
        self.maxMoney = 40
        self.money = 0
        self.bankMoney = 0
        self.maxBankMoney = 1000
        self.trackAccess = [0, 0, 0, 0, 1, 1, 0]
        self.experience = Experience()
        self.inventory = Inventory()

    def setDNAString(self, dnaString):
        self.dnaString = dnaString

    def getDNAString(self):
        return self.dnaString

    def getGM(self):
        return False

    def setMaxBankMoney(self, money):
        self.maxBankMoney = money

    def getMaxBankMoney(self):
        return self.maxBankMoney

    def setBankMoney(self, money):
        self.bankMoney = money

    def getBankMoney(self):
        return self.bankMoney

    def setMaxMoney(self, maxMoney):
        self.maxMoney = maxMoney

    def getMaxMoney(self):
        return self.maxMoney

    def setMoney(self, money):
        self.money = money

    def getMoney(self):
        return self.money

    def d_setMoney(self, money):
        self.sendUpdate('setMoney', [money])

    def b_setMoney(self, money):
        self.setMoney(money)
        self.d_setMoney(money)

    def takeMoney(self, deltaMoney, useBank=True):
        totalMoney = self.money + (self.bankMoney if useBank else 0)
        if deltaMoney > totalMoney:
            return False

        if useBank and deltaMoney > self.money:
            self.b_setBankMoney(self.bankMoney - (deltaMoney - self.money))
            self.b_setMoney(0)
        else:
            self.b_setMoney(self.money - deltaMoney)
        return True

    def addMoney(self, deltaMoney):
        money = deltaMoney + self.money
        pocketMoney = min(money, self.maxMoney)
        self.b_setMoney(pocketMoney)
        overflowMoney = money - self.maxMoney
        if overflowMoney > 0:
            bankMoney = self.bankMoney + overflowMoney
            self.b_setBankMoney(bankMoney)

    def setMaxHp(self, hp):
        self.maxHp = hp

    def getMaxHp(self):
        return self.maxHp

    def setHp(self, hp):
        self.hp = hp

    def getHp(self):
        return self.hp

    def d_setHp(self, hp):
        self.sendUpdate('setHp', [hp])

    def b_setHp(self, hp):
        self.setHp(hp)
        self.d_setHp(hp)

    def toonUp(self, hpGained, quietly=0, sendTotal=1):
        hpGained = min(self.maxHp, hpGained)
        if not quietly:
            self.sendUpdate('toonUp', [hpGained])
        if self.hp + hpGained <= 0:
            self.hp += hpGained
        else:
            self.hp = max(self.hp, 0) + hpGained
        clampedHp = min(self.hp, self.maxHp)
        if sendTotal:
            self.d_setHp(clampedHp)

    def getBattleId(self):
        return 0

    def setExperience(self, experience):
        self.experience = Experience.fromBytes(experience)
        self.experience.toon = self

    def getExperience(self):
        return self.experience.makeNetString()

    def getMaxCarry(self):
        return 20

    def setTrackAccess(self, trackAccess):
        self.trackAccess = trackAccess

    def getTrackAccess(self):
        return self.trackAccess

    def hasTrackAccess(self, track):
        return self.trackAccess[track] > 0

    def getTrackProgress(self):
        return 0, 0

    def getTrackBonusLevel(self):
        return [0, 0, 0, 0, 0, 0, 0]

    def setInventory(self, inventory):
        self.inventory = Inventory.fromBytes(inventory)
        self.inventory.toon = self

    def getInventory(self):
        return self.inventory.makeNetString()

    def d_setInventory(self, blob):
        self.sendUpdate('setInventory', [blob])

    def getMaxNPCFriends(self):
        return 8

    def getNPCFriendsDict(self):
        return []

    def getDefaultShard(self):
        return 0

    def getDefaultZone(self):
        return 2000

    def getShtickerBook(self):
        return b''

    def getZonesVisited(self):
        return []

    def getHoodsVisited(self):
        return []

    def getInterface(self):
        return b''

    def getLastHood(self):
        return 0

    def getTutorialAck(self):
        return 1

    def getMaxClothes(self):
        return 0

    def getClothesTopsList(self):
        return []

    def getClothesBottomsList(self):
        return []

    def getMaxAccessories(self):
        return 0

    def getHatList(self):
        return []

    def getGlassesList(self):
        return []

    def getBackpackList(self):
        return []

    def getShoesList(self):
        return []

    def getHat(self):
        return 0, 0, 0

    def getGlasses(self):
        return 0, 0, 0

    def getBackpack(self):
        return 0, 0, 0

    def getShoes(self):
        return 0, 0, 0

    def getGardenSpecials(self):
        return []

    def getEmoteAccess(self):
        return [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def getCustomMessages(self):
        return []

    def getResistanceMessages(self):
        return []

    def getPetTrickPhrases(self):
        return []

    def getCatalogSchedule(self):
        return 0, 0

    def getCatalog(self):
        return b'', b'', b''

    def getMailboxContents(self):
        return b''

    def getDeliverySchedule(self):
        return b''

    def getGiftSchedule(self):
        return b''

    def getAwardMailboxContents(self):
        return b''

    def getAwardSchedule(self):
        return b''

    def getAwardNotify(self):
        return 0

    def getCatalogNotify(self):
        return 0, 0

    def getSpeedChatStyleIndex(self):
        return 1

    def getTeleportAccess(self):
        return []

    def getCogStatus(self):
        return [0] * 32

    def getCogCount(self):
        return [0] * 32

    def getCogRadar(self):
        return [0] * 4

    def getBuildingRadar(self):
        return [0] * 4

    def getCogLevels(self):
        return [0] * 4

    def getCogTypes(self):
        return [0] * 4

    def getCogParts(self):
        return [0] * 4

    def getCogMerits(self):
        return [0] * 4

    def getHouseId(self):
        return 0

    def getQuests(self):
        return []

    def getQuestHistory(self):
        return []

    def getRewardHistory(self):
        return 0, []

    def getQuestCarryLimit(self):
        return 1

    def getCheesyEffect(self):
        return 0, 0, 0

    def getPosIndex(self):
        return 0

    def getFishCollection(self):
        return [], [], []

    def getMaxFishTank(self):
        return 20

    def getFishTank(self):
        return [], [], []

    def getFishingRod(self):
        return 0

    def getFishingTrophies(self):
        return []

    def getFlowerCollection(self):
        return [], []

    def getFlowerBasket(self):
        return [], []

    def getMaxFlowerBasket(self):
        return 20

    def getGardenTrophies(self):
        return []

    def getShovel(self):
        return 0

    def getShovelSkill(self):
        return 0

    def getWateringCan(self):
        return 0

    def getWateringCanSkill(self):
        return 0

    def getPetId(self):
        return 0

    def getPetTutorialDone(self):
        return 0

    def getFishBingoTutorialDone(self):
        return 0

    def getFishBingoMarkTutorialDone(self):
        return 0

    def getKartBodyType(self):
        return -1

    def getKartBodyColor(self):
        return -1

    def getKartAccessoryColor(self):
        return -1

    def getKartEngineBlockType(self):
        return -1

    def getKartSpoilerType(self):
        return -1

    def getKartFrontWheelWellType(self):
        return -1

    def getKartBackWheelWellType(self):
        return -1

    def getKartRimType(self):
        return -1

    def getKartDecalType(self):
        return -1

    def getTickets(self):
        return 200

    def getKartingHistory(self):
        return [0] * 16

    def getKartingTrophies(self):
        return [0] * 33

    def getKartingPersonalBest(self):
        return [0] * 6

    def getKartingPersonalBest2(self):
        return [0] * 12

    def getKartAccessoriesOwned(self):
        return [0] * 16

    def getCogSummonsEarned(self):
        return [0] * 32

    def getGardenStarted(self):
        return 0

    def getGolfHistory(self):
        return [0] * 18

    def getPackedGolfHoleBest(self):
        return [0] * 18

    def getGolfCourseBest(self):
        return [0] * 3

    def getPinkSlips(self):
        return 0

    def getNametagStyle(self):
        return 0

    def handleZoneChange(self, old_zone: int, new_zone: int):
        channel = getPuppetChannel(self.do_id)

        if old_zone in self.air.vismap and new_zone not in self.air.vismap:
            self.air.removeInterest(channel, DistributedToonAI.STREET_INTEREST_HANDLE, 0)
        elif new_zone in self.air.vismap:
            visibles = self.air.vismap[new_zone][:]
            if len(visibles) == 1 and visibles[0] == new_zone:
                # Playground visgroup, ignore
                return
            self.air.setInterest(channel, DistributedToonAI.STREET_INTEREST_HANDLE, 0, self.parentId, visibles)


NUM_TRACKS = 7
UBER_INDEX = 6
NUM_PROPS = 7

Levels = [
    [0, 20, 200, 800, 2000, 6000, 10000],
    [0, 20, 100, 800, 2000, 6000, 10000],
    [0, 20, 100, 800, 2000, 6000, 10000],
    [0, 40, 200, 1000, 2500, 7500, 10000],
    [0, 10, 50, 400, 2000, 6000, 10000],
    [0, 10, 50, 400, 2000, 6000, 10000],
    [0, 20, 100, 500, 2000, 6000, 10000]
]

CarryLimits = (
    (
        (10, 0, 0, 0, 0, 0, 0),
        (10, 5, 0, 0, 0, 0, 0),
        (15, 10, 5, 0, 0, 0, 0),
        (20, 15, 10, 5, 0, 0, 0),
        (25, 20, 15, 10, 3, 0, 0),
        (30, 25, 20, 15, 7, 3, 0),
        (30, 25, 20, 15, 7, 3, 1)
    ),
    (
        (5, 0, 0, 0, 0, 0, 0),
        (7, 3, 0, 0, 0, 0, 0),
        (10, 7, 3, 0, 0, 0, 0),
        (15, 10, 7, 3, 0, 0, 0),
        (15, 15, 10, 5, 3, 0, 0),
        (20, 15, 15, 10, 5, 2, 0),
        (20, 15, 15, 10, 5, 2, 1)),
    (
        (10, 0, 0, 0, 0, 0, 0),
        (10, 5, 0, 0, 0, 0, 0),
        (15, 10, 5, 0, 0, 0, 0),
        (20, 15, 10, 5, 0, 0, 0),
        (25, 20, 15, 10, 3, 0, 0),
        (30, 25, 20, 15, 7, 3, 0),
        (30, 25, 20, 15, 7, 3, 1)
    ),
    (
        (10, 0, 0, 0, 0, 0, 0),
        (10, 5, 0, 0, 0, 0, 0),
        (15, 10, 5, 0, 0, 0, 0),
        (20, 15, 10, 5, 0, 0, 0),
        (25, 20, 15, 10, 3, 0, 0),
        (30, 25, 20, 15, 7, 3, 0),
        (30, 25, 20, 15, 7, 3, 1)
    ),
    (
        (10, 0, 0, 0, 0, 0, 0),
        (10, 5, 0, 0, 0, 0, 0),
        (15, 10, 5, 0, 0, 0, 0),
        (20, 15, 10, 5, 0, 0, 0),
        (25, 20, 15, 10, 3, 0, 0),
        (30, 25, 20, 15, 7, 3, 0),
        (30, 25, 20, 15, 7, 3, 1)
    ),
    (
        (10, 0, 0, 0, 0, 0, 0),
        (10, 5, 0, 0, 0, 0, 0),
        (15, 10, 5, 0, 0, 0, 0),
        (20, 15, 10, 5, 0, 0, 0),
        (25, 20, 15, 10, 3, 0, 0),
        (30, 25, 20, 15, 7, 3, 0),
        (30, 25, 20, 15, 7, 3, 1)
    ),
    (
        (10, 0, 0, 0, 0, 0, 0),
        (10, 5, 0, 0, 0, 0, 0),
        (15, 10, 5, 0, 0, 0, 0),
        (20, 15, 10, 5, 0, 0, 0),
        (25, 20, 15, 10, 3, 0, 0),
        (30, 25, 20, 15, 7, 3, 0),
        (30, 25, 20, 15, 7, 3, 1)
    )
)

regMaxSkill = 10000
UberSkill = 500
MaxSkill = UberSkill + regMaxSkill
UnpaidMaxSkills = [Levels[0][1] - 1,
 Levels[1][1] - 1,
 Levels[2][1] - 1,
 Levels[3][1] - 1,
 Levels[4][4] - 1,
 Levels[5][4] - 1,
 Levels[6][1] - 1]
ExperienceCap = 200


class Inventory:
    __slots__ = 'inventory', 'toon'

    def __init__(self, inventory=None, toon=None):
        if not inventory:
            self.inventory = [0] * NUM_TRACKS * NUM_PROPS
        else:
            self.inventory = inventory

        self.toon = toon

    def __getitem__(self, key):
        if not type(key) == int:
            raise IndexError

        return self.inventory[key]

    def __iter__(self):
        yield from self.inventory

    @property
    def totalProps(self):
        return sum(self.inventory)

    def get(self, track, level):
        return self[track * NUM_TRACKS + level]

    def getMax(self, track, level):
        if self.toon.experience:
            return CarryLimits[track][self.toon.experience.getExpLevel(track)][level]
        else:
            return 0

    def addItems(self, track, level, amount):
        if not self.toon.hasTrackAccess(track):
            return

        if self.toon.experience.getExpLevel(track) < level:
            return

        if self.totalProps + amount > self.toon.getMaxCarry() and level < 6:
            return

        self[track * NUM_TRACKS + level] += amount
        return self[track * NUM_TRACKS + level]

    def validatePurchase(self, newInventory, currentMoney, newMoney):
        if newMoney > currentMoney:
            return False

        newTotal = newInventory.totalProps
        oldTotal = self.totalProps

        if newTotal > oldTotal + currentMoney:
            return False

        if newTotal - oldTotal > currentMoney - newMoney:
            return False

        if newTotal > self.toon.getMaxCarry():
            print('more than max carry')
            return False

        for i in range(0, NUM_TRACKS * NUM_PROPS, UBER_INDEX):
            if newInventory[i] > self[i]:
                # Can't buy level 7 gags.
                print('tried buying uber')
                return False

        if not newInventory.validateItems():
            return False

        # TODO: check access

        return True

    def validateItems(self):
        for index, amount in enumerate(self):
            track, level = index // NUM_TRACKS, index % NUM_PROPS

            if not self.toon.hasTrackAccess(track) and amount:
                print('no track acccess and tried to buy')
                return False

            if amount > self.getMax(track, level):
                print('over max')
                return False

        return True


    @staticmethod
    def fromBytes(data):
        return Inventory.fromNetString(Datagram(data).iterator())

    @staticmethod
    def fromNetString(dgi):
        return Inventory([dgi.get_uint8() for _ in range(NUM_TRACKS * NUM_PROPS)])

    def makeNetString(self):
        return b''.join((prop.to_bytes(1, 'little') for prop in self.inventory))


from ai import OTPGlobals


class Experience:
    __slots__ = 'experience', 'toon'

    def __init__(self, experience=None, toon=None):
        if not experience:
            self.experience = [0] * NUM_TRACKS
        else:
            self.experience = experience

        self.toon = toon

    def __getitem__(self, key):
        if not type(key) == int:
            raise IndexError

        return self.experience[key]

    @staticmethod
    def fromBytes(data):
        return Experience.fromNetString(Datagram(data).iterator())

    @staticmethod
    def fromNetString(dgi):
        return Experience([dgi.get_uint16() for _ in range(NUM_TRACKS)])

    def makeNetString(self):
        return b''.join((trackExp.to_bytes(2, 'little') for trackExp in self.experience))

    def addExp(self, track, amount=1):
        current = self.experience[track]

        if self.toon.getAccess() == OTPGlobals.AccessFull:
            maxExp = MaxSkill
        else:
            maxExp = UnpaidMaxSkills[track]

        self.experience[track] = min(current + amount, maxExp)

    def getExpLevel(self, track):
        xp = self[track]
        for amount in Levels[track]:
            if xp < amount:
                return max(Levels[track].index(amount) - 1, 0)
        else:
            return NUM_PROPS - 1
