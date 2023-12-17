import sys
sys.path.append(r'C:\Users\ghkdr\Appdata\Local\Programs\Python\Python311\Lib\site-packages')
import pyRosetta
import random
import copy
import pygame

mydeckname = "cdruid"
opdeckname = "cdruid"
DISPLAY = True

deck1 = pyRosetta.Deck(pyRosetta.FormatType.WILD, pyRosetta.CardClass.DRUID)
decklist = {"cdruid": deck1}

deckcards = {
    deck1: [
        ["VAN_EX1_169", 2],  # 정신자극
        ["VAN_CS2_013", 2],  # 급속성장
        ["VAN_EX1_154", 2],  # 천벌
        ["VAN_EX1_556", 2],  # Harvest Golem, 커스텀
        ["VAN_CS2_011", 2],  # 야생의포효
        ["VAN_CS2_182", 2],  # 서리바람설인
        ["VAN_EX1_166", 2],  # 숲의수호자
        ["VAN_CS2_179", 2],  # 센진방패대가
        ["VAN_CS2_012", 2],  # 휘둘러치기
        ["VAN_EX1_284", 2],  # 하늘빛비룡
        ["VAN_EX1_165", 2],  # 발톱의드루이드
        ["VAN_EX1_110", 1],  # 케른블러드후프
        ["VAN_EX1_571", 2],  # 자연의군대
        ["VAN_EX1_016", 1],  # 실바나스윈드러너
        ["VAN_NEW1_008", 2],  # 지식의고대정령
        ["VAN_EX1_178", 2]  # 전쟁의고대정령
    ],
}

first = random.randrange(2)
decktype = ["", ""]
deck = [[], []]
deckcard = [[], []]
handcard = [[], []]
fieldcard = [[], []]
fieldcardstat = [[], []]  # [공,체,공격가능성,상태(침묵 등)]
maxmana = [0, 0]
curmana = [0, 0]
hp = [30, 30]
playlog = []
heroab = False


def game(depth0=10000, depth1=10000):
    global fieldcardstat
    global maxmana
    global hp
    global handcard
    global fieldcard
    global deckcard
    handcard = [[], []]
    fieldcard = [[], []]
    fieldcardstat = [[], []]  # [공,체,공격가능성,상태(침묵 등)]
    maxmana = [0, 0]
    curmana = [0, 0]
    cmana = [0, 0]
    hp = [30, 30]

    class cDruid:

        hp = [30, 30]

        def __init__(self, me):
            self.me = me
            self.op = 1 - me
            decktype[self.me] = "comboDruid"
            decklist = pyRosetta.Deck(pyRosetta.FormatType.WILD, pyRosetta.CardClass.DRUID)
            for ID, num in deckcards[deck1]:
                decklist.add_card(ID, num)
            deck[self.me] = decklist.cards()
            curmana = 0

        def draw(self):
            if len(deckcard[self.me]) > 0:
                handcard[self.me].append(deckcard[self.me].pop(0))

        def shuffle(self):
            random.shuffle(deckcard[self.me])

        def cardinmyfield(self, cardname):
            count = 0
            for card in fieldcard[self.me]:
                if card.name == cardname:
                    count += 1
            return count

        def cardinmyhand(self, cardname):
            count = 0
            for card in handcard[self.me]:
                if card.name == cardname:
                    count += 1
            return count

        def cardinmydeck(self, cardname):
            count = 0
            for card in deckcard[self.me]:
                if card.name == cardname:
                    count += 1
            return count

        def cardinopfield(self, cardname):
            count = 0
            for card in fieldcard[self.op]:
                if card.name == cardname:
                    count += 1
            return count

        def cardinophhanddeck(self, cardname):
            count = 0
            for card in handcard[self.me]:
                if card.name == cardname:
                    count += 1
            for card in deckcard[self.me]:
                if card.name == cardname:
                    count += 1
            return count

        # 덱을 생성하고 셔플
        def newgame(self, first):
            deckcard[self.me] = deck[self.me][:]
            self.shuffle()
            my_first = (self.me == first)
            if my_first == True:
                self.draw()
                self.draw()
                self.draw()
            else:
                self.draw()
                self.draw()
                self.draw()
                self.draw()

        # 멀리건
        def mulligun(self, first):
            my_first = (self.me == first)
            if my_first == True:
                temp = 0  # 멀리건을 진행했는지 판단
                if handcard[self.me][0].name not in ["Innervate", "Wild Growth"]:
                    if handcard[self.me][1].name not in ["Innervate", "Wild Growth"]:
                        if handcard[self.me][2].name not in ["Innervate", "Wild Growth"]:
                            temp = 1
                            deckcard[self.me].append(handcard[self.me].pop(0))
                            deckcard[self.me].append(handcard[self.me].pop(0))
                            deckcard[self.me].append(handcard[self.me].pop(0))
                            self.draw()
                            self.draw()
                            self.draw()
                            self.shuffle()
                if temp == 0:
                    costs = [handcard[self.me][0].game_tags[pyRosetta.GameTag.COST],
                             handcard[self.me][1].game_tags[pyRosetta.GameTag.COST],
                             handcard[self.me][2].game_tags[pyRosetta.GameTag.COST]]
                    if costs[0] > costs[1]:
                        costs[0], costs[1] = costs[1], costs[0]
                        handcard[self.me][0], handcard[self.me][1] = handcard[self.me][1], handcard[self.me][0]
                    if costs[1] > costs[2]:
                        costs[1], costs[2] = costs[2], costs[1]
                        handcard[self.me][1], handcard[self.me][2] = handcard[self.me][2], handcard[self.me][1]
                    if costs[0] > costs[1]:
                        costs[0], costs[1] = costs[1], costs[0]
                        handcard[self.me][0], handcard[self.me][1] = handcard[self.me][1], handcard[self.me][0]
                    if costs[0] == 0:
                        if costs[1] == 0:
                            if costs[2] < 5 or handcard[self.me][2].name in ["Force of Nature"]:
                                deckcard[self.me].append(handcard[self.me].pop(2))
                                self.draw()
                                self.shuffle()
                        elif handcard[self.me][1].name in ["Wild Growth"]:
                            if handcard[self.me][2].name in ["Wrath", "Savage Roar", "Swipe", "Force of Nature"]:
                                deckcard[self.me].append(handcard[self.me].pop(2))
                                self.draw()
                                self.shuffle()
                        elif handcard[self.me][2].name in ["Wild Growth"]:
                            deckcard[self.me].append(handcard[self.me].pop(1))
                            self.draw()
                            self.shuffle()
                        else:
                            if costs[2] > 4 or handcard[self.me][2].name in ["Savage Roar", "Swipe", "Wrath"]:
                                deckcard[self.me].append(handcard[self.me].pop(2))
                                self.draw()
                                self.shuffle()
                            if costs[1] > 4 or handcard[self.me][1].name in ["Savage Roar", "Swipe", "Wrath"]:
                                deckcard[self.me].append(handcard[self.me].pop(1))
                                self.draw()
                                self.shuffle()
                    else:
                        if handcard[self.me][0].name in ["Wrath"]:
                            deckcard[self.me].append(handcard[self.me].pop(0))
                            self.draw()
                            self.shuffle()
                            if costs[1] > 4 or handcard[self.me][1].name in ["Savage Roar", "Swipe", "Wrath"]:
                                deckcard[self.me].append(handcard[self.me].pop(1))
                                self.draw()
                                self.shuffle()
                        else:
                            if costs[1] > 4 or handcard[self.me][1].name in ["Savage Roar", "Swipe", "Wrath"]:
                                deckcard[self.me].append(handcard[self.me].pop(1))
                                self.draw()
                                self.shuffle()
                            if costs[1] > 4 or handcard[self.me][1].name in ["Savage Roar", "Swipe", "Wrath"]:
                                deckcard[self.me].append(handcard[self.me].pop(1))
                                self.draw()
                                self.shuffle()
            else:
                temp = 0  # 멀리건을 진행했는지 판단
                if handcard[self.me][0].name not in ["Innervate", "Wild Growth"]:
                    if handcard[self.me][1].name not in ["Innervate", "Wild Growth"]:
                        if handcard[self.me][2].name not in ["Innervate", "Wild Growth"]:
                            if handcard[self.me][2].name not in ["Innervate", "Wild Growth"]:
                                temp = 1
                                deckcard[self.me].append(handcard[self.me].pop(0))
                                deckcard[self.me].append(handcard[self.me].pop(0))
                                deckcard[self.me].append(handcard[self.me].pop(0))
                                deckcard[self.me].append(handcard[self.me].pop(0))
                                self.draw()
                                self.draw()
                                self.draw()
                                self.draw()
                                self.shuffle()
                if temp == 0:
                    costs = [handcard[self.me][0].game_tags[pyRosetta.GameTag.COST],
                             handcard[self.me][1].game_tags[pyRosetta.GameTag.COST],
                             handcard[self.me][2].game_tags[pyRosetta.GameTag.COST],
                             handcard[self.me][3].game_tags[pyRosetta.GameTag.COST]]
                    if costs[0] > costs[1]:
                        costs[0], costs[1] = costs[1], costs[0]
                        handcard[self.me][0], handcard[self.me][1] = handcard[self.me][1], handcard[self.me][0]
                    if costs[1] > costs[2]:
                        costs[1], costs[2] = costs[2], costs[1]
                        handcard[self.me][1], handcard[self.me][2] = handcard[self.me][2], handcard[self.me][1]
                    if costs[2] > costs[3]:
                        costs[2], costs[3] = costs[3], costs[2]
                        handcard[self.me][2], handcard[self.me][3] = handcard[self.me][3], handcard[self.me][2]
                    if costs[0] > costs[1]:
                        costs[0], costs[1] = costs[1], costs[0]
                        handcard[self.me][0], handcard[self.me][1] = handcard[self.me][1], handcard[self.me][0]
                    if costs[1] > costs[2]:
                        costs[1], costs[2] = costs[2], costs[1]
                        handcard[self.me][1], handcard[self.me][2] = handcard[self.me][2], handcard[self.me][1]
                    if costs[0] > costs[1]:
                        costs[0], costs[1] = costs[1], costs[0]
                        handcard[self.me][0], handcard[self.me][1] = handcard[self.me][1], handcard[self.me][0]

                    if costs[1] == 0:
                        if costs[3] < 5 or handcard[self.me][3].name in ["Force of Nature"]:
                            deckcard[self.me].append(handcard[self.me].pop(3))
                            self.draw()
                            self.shuffle()
                        if handcard[self.me][2].name not in ["wild growth"] and costs[2] < 5 or handcard[self.me][
                            2].name in ["Force of Nature"]:
                            deckcard[self.me].append(handcard[self.me].pop(2))
                            self.draw()
                            self.shuffle()

                    else:
                        if costs[3] > 4 or handcard[self.me][3].name in ["Savage Roar", "Swipe", "Wrath"]:
                            deckcard[self.me].append(handcard[self.me].pop(3))
                            self.draw()
                            self.shuffle()
                        if costs[2] > 4 or handcard[self.me][2].name in ["Savage Roar", "Swipe", "Wrath"]:
                            deckcard[self.me].append(handcard[self.me].pop(2))
                            self.draw()
                            self.shuffle()
                        if costs[1] > 4 or handcard[self.me][1].name in ["Savage Roar", "Swipe", "Wrath"]:
                            deckcard[self.me].append(handcard[self.me].pop(1))
                            self.draw()
                            self.shuffle()
                        if costs[0] > 4 or handcard[self.me][0].name in ["Savage Roar", "Swipe", "Wrath"]:
                            deckcard[self.me].append(handcard[self.me].pop(0))
                            self.draw()
                            self.shuffle()
                handcard[self.me].append(pyRosetta.Cards.find_card_by_id('GAME_005'))  # add The Coin

        # 최대 데미지 계산
        def maxatk(self):
            mana = maxmana[self.me] + 2 * self.cardinmyhand("Innervate") + 1 * self.cardinmyhand("The Coin")
            fieldatk = []
            mobcount = 0
            maxatk = 0
            temp = 0
            for i in range(len(fieldcard[self.me])):
                mobcount += 1
                if fieldcardstat[self.me][i][2] == True:
                    fieldatk.append(fieldcard[self.me][i].game_tags[pyRosetta.GameTag.ATK])

            if mana < 2:
                maxatk = max(maxatk, sum(fieldatk))
            elif mana < 3:
                maxatk = max(maxatk, sum(fieldatk) + 1)
            else:
                if self.cardinmyhand("Savage Roar") > 0:
                    if self.cardinmyhand("Druid of the Claw") > 0 and self.cardinmyhand(
                            "Savage Roar") > 1 and mana >= 12:
                        maxatk = max(maxatk, sum(fieldatk) + 4 * len(fieldatk) + 4 + 6 * min(3, 7 - mobcount))
                    if self.cardinmyhand("Druid of the Claw") > 0 and self.cardinmyhand(
                            "Savage Roar") > 1 and mana >= 11:
                        maxatk = max(maxatk, sum(fieldatk) + 4 * len(fieldatk) + 4 + 8 * min(1, 7 - mobcount))
                    if self.cardinmyhand("Force of Nature") > 0 and mana >= 9:
                        if self.cardinmyhand("Savage Roar") > 1:
                            maxatk = max(maxatk, sum(fieldatk) + 4 * len(fieldatk) + 4,
                                         sum(fieldatk) + 2 * len(fieldatk) + 14)
                        maxatk = max(maxatk, sum(fieldatk) + 2 * len(fieldatk) + 2 + 4 * min(3, 7 - mobcount))
                    if self.cardinmyhand("Druid of the Claw") > 0 and mana >= 8:
                        if self.cardinmyhand("Savage Roar") > 1:
                            maxatk = max(maxatk, sum(fieldatk) + 4 * len(fieldatk) + 4,
                                         sum(fieldatk) + 2 * len(fieldatk) + 8)
                        maxatk = max(maxatk, sum(fieldatk) + 2 * len(fieldatk) + 8)
                    if self.cardinmyhand("Savage Roar") > 1 and mana >= 6:
                        maxatk = max(maxatk, sum(fieldatk) + 4 * len(fieldatk) + 4, sum(fieldatk) + 6)
                    if self.cardinmyhand("Force of Nature") > 0 and mana >= 6:
                        maxatk = max(maxatk, sum(fieldatk) + 6, sum(fieldatk) + 2 * len(fieldatk) + 2)
                    if self.cardinmyhand("Druid of the Claw") > 0 and mana >= 5:
                        maxatk = max(maxatk, sum(fieldatk) + 4, sum(fieldatk) + 2 * len(fieldatk) + 2)
                    if self.cardinmyhand("Swipe") > 0 and mana >= 7:
                        maxatk = max(maxatk, sum(fieldatk) + 2 * len(fieldatk) + 4)
                    if self.cardinmyhand("Swipe") > 0 and mana >= 4:
                        maxatk = max(maxatk, sum(fieldatk) + 4)
                    if self.cardinmyhand("Keeper of the Grove") > 0 and mana >= 7:
                        maxatk = max(maxatk, sum(fieldatk) + 2 * len(fieldatk) + 4)
                    if mana >= 5:
                        maxatk = max(maxatk, sum(fieldatk) + 2 * len(fieldatk) + 3)
                    maxatk = max(maxatk, sum(fieldatk) + 2 * len(fieldatk) + 2)
                else:
                    dy = [0] * (mana + 1)
                    temp = [0] * (mana + 1)

                    def dynamic(cardname, cardcost, carddamage):
                        if self.cardinmyhand(cardname) > 0:
                            for i in range(len(dy)):
                                if i >= cardcost:
                                    dy[i] = max(temp[i], temp[i - cardcost] + carddamage)
                            for i in range(len(dy)):
                                temp[i] = dy[i]
                        if self.cardinmyhand(cardname) > 1:
                            for i in range(len(dy)):
                                if i >= cardcost:
                                    dy[i] = max(temp[i], temp[i - cardcost] + carddamage)
                            for i in range(len(dy)):
                                temp[i] = dy[i]

                    dynamic("Force of Nature", 6, 6)
                    dynamic("Druid of the Claw", 5, 4)
                    dynamic("Swipe", 4, 2)
                    dynamic("Keeper of the Grove", 4, 2)
                    for i in range(len(dy)):
                        if i >= 2:
                            dy[i] = max(temp[i], temp[i - 2] + 1)
                    for i in range(len(dy)):
                        temp[i] = dy[i]
                    maxatk = max(maxatk, sum(fieldatk) + dy[-1])
            return maxatk

        # 한 턴의 최선의 플레이
        def myturn(self, DEPTH=10000):
            def dead(target):
                deadcard = curfield.pop(target)
                deadcardstat = curfieldstat.pop(target)
                if deadcard.name == "Cairne Bloodhoof" and deadcardstat[3] != "Silence":
                    curfield.append(pyRosetta.Cards.find_card_by_id("VAN_EX1_110t"))
                    curfieldstat.append([4, 5, False, None])
                elif deadcard.name == "Harvest Golem" and deadcardstat[3] != "Silence":
                    curfield.append(pyRosetta.Cards.find_card_by_id("VAN_CS2_168"))
                    curfield[-1].name = "Damaged Golem"
                    curfieldstat.append([2, 1, False, None])
                elif deadcard.name == "Sylvanas Windrunner":
                    if len(curopfield) != 0 and deadcardstat[3] != "Silence":
                        temp = random.randrange(len(curopfield))
                        curfield.append(curopfield.pop(temp))
                        curfieldstat.append(curopfieldstat.pop(temp))

            def kill(target):
                deadcard = curopfield.pop(target)
                curopfieldstat.pop(target)
                if deadcard.name == "Cairne Bloodhoof":
                    curopfield.append(pyRosetta.Cards.find_card_by_id("VAN_EX1_110t"))
                    curopfield[-1].name = "Baine Bloodhoof"
                    curopfieldstat.append([4, 5, False, None])
                elif deadcard.name == "Harvest Golem":
                    curopfield.append(pyRosetta.Cards.find_card_by_id("VAN_CS2_168"))
                    curopfield[-1].name = "Damaged Golem"
                    curopfieldstat.append([2, 1, False, None])
                elif deadcard.name == "Sylvanas Windrunner":
                    if len(curfield) != 0:
                        temp = random.randrange(len(curfield))
                        curopfield.append(curfield.pop(temp))
                        curopfieldstat.append(curfieldstat.pop(temp))

            def curdraw():
                if len(curdeck) > 0:
                    curhand.append(curdeck.pop(0))

            global fieldcardstat
            global maxmana
            global hp
            global handcard
            global fieldcard
            global deckcard
            global playlog
            global heroab
            # 지금 있는 모든 몬스터는 공격 가능
            for mobstat in fieldcardstat[self.me]:
                mobstat[2] = True
            self.draw()
            if maxmana[self.me] < 10:
                maxmana[self.me] += 1
            cmana[self.me] = maxmana[self.me]
            if DISPLAY:
                gamedisplay()
            if self.maxatk() >= hp[self.op]:
                if self.cardinopfield("Sen'jin Shieldmasta") == 0 and self.cardinopfield(
                        "Druid of the Chaw") == 0 and self.cardinopfield("Ancient of War") == 0:
                    return self.me

            besthand = [[], []]
            bestfield = [[], []]
            bestfieldstat = [[], []]
            bestdeck = [[], []]
            besthp = [0, 0]
            bestplaylog = []
            heroab = False
            bestscore = -10000
            bestmaxmana = copy.deepcopy(maxmana)

            for depth in range(DEPTH):
                curmaxmana = maxmana[self.me]
                curmana = maxmana[self.me]
                curdeck = deckcard[self.me][:]
                curhand = handcard[self.me][:]
                curfield = fieldcard[self.me][:]
                curfieldstat = copy.deepcopy(fieldcardstat[self.me])
                curopfield = fieldcard[self.op][:]
                curopfieldstat = copy.deepcopy(fieldcardstat[self.op])
                curhp = copy.deepcopy(hp)
                curheroab = False
                heroatk = 0
                spellatk = self.cardinmyfield("Azure Drake")
                play = []
                score = 0

                while (True):
                    # 필드 설치 페이즈
                    if len(curhand) == 0:
                        break
                    num = random.randrange(len(curhand))
                    play.append(curhand.pop(num))
                    if curmana >= play[-1].game_tags[pyRosetta.GameTag.COST]:
                        curmana -= play[-1].game_tags[pyRosetta.GameTag.COST]
                    else:
                        curhand.append(play.pop(-1))
                        break
                    if play[-1].name == "Innervate":
                        score = score - 34
                        curmana += 2
                    elif play[-1].name == "The Coin":
                        score = score - 17
                        curmana += 1
                    elif play[-1].name == "Wild Growth":
                        if maxmana[self.me] == 10:
                            curdraw()
                        else:
                            score = score + (2 * (120 - 15 * curmaxmana))
                            curmaxmana += 1
                    elif play[-1].name == "Wrath":
                        if len(curopfield) == 0:
                            curhand.append(play.pop(-1))
                            break
                        else:
                            temp = False
                            for i in range(3):
                                target = random.randrange(len(curopfield))
                                if curopfieldstat[target][1] <= 3 + spellatk:
                                    if curopfieldstat[target][1] <= 1 + spellatk:
                                        kill(target)
                                        curdraw()
                                        score = score + 25
                                    else:
                                        kill(target)
                                    temp = True
                                    break
                            if not temp:
                                if random.randrange(2) == 0:
                                    curopfieldstat[target][1] -= 3 + spellatk
                                else:
                                    curopfieldstat[target][1] -= 1 + spellatk
                                    curdraw()
                                    score = score + 30
                    elif play[-1].name == "Savage Roar":
                        heroatk += 2
                        for i in range(len(curfield)):
                            curfieldstat[i][0] += 2
                        c = False
                        for i in curhand:
                            if i.name == "Savage Roar": c = True
                        if not c:
                            score = score - 60
                    elif play[-1].name == "Swipe":
                        target = random.randrange(len(curopfield) + 1) - 1
                        if target == -1:
                            curhp[self.op] -= 4 + spellatk
                        else:
                            curhp[self.op] -= 1 + spellatk
                        for i in range(len(curopfield)):
                            if target == i:
                                curopfieldstat[i][1] -= 4 + spellatk
                            else:
                                curopfieldstat[i][1] -= 1 + spellatk
                        for i in range(len(curopfield) - 1, -1, -1):
                            if curopfieldstat[i][1] <= 0:
                                kill(i)
                    elif play[-1].name == "Force of Nature":
                        for i in range(3):
                            if len(curfield) == 7:
                                break
                            else:
                                curfield.append(pyRosetta.Cards.find_card_by_id("KAR_300"))
                                curfield[-1].name = "Treant"
                                curfieldstat.append([2, 2, True, "treant"])
                        c = False
                        for i in curhand:
                            if i.name == "Force of Nature": c = True
                        if not c:
                            score = score - 60
                    else:  # 나머지는 모두 몬스터 1체 소환
                        if len(curfield) >= 7:
                            curhand.append(play.pop(-1))
                            break
                        else:
                            curfield.append(play[-1])
                            curfieldstat.append(
                                [play[-1].game_tags[pyRosetta.GameTag.ATK],
                                 play[-1].game_tags[pyRosetta.GameTag.HEALTH], False,
                                 None])
                            cardname = play[-1].name
                            if cardname == "Keeper of the Grove":
                                target = random.randrange(-1, len(curopfield))
                                if target == -1:
                                    curhp[self.op] -= 2
                                else:
                                    if curopfield[target].name == "Sylvanas Windrunner" or curopfield[
                                        target].name == "Cairne Bloodhoof":
                                        curopfieldstat[target][3] = "Silence"
                                    elif curopfield[target].name == "Ancient of War":
                                        if curopfieldstat[target][1] <= 2:
                                            kill(target)
                                        elif curopfieldstat[target][1] <= 6:
                                            curopfieldstat[target][1] -= 2
                                        else:
                                            curopfieldstat[target][1] = 5
                                            curopfieldstat[target][3] = "Silence"
                                    elif curopfield[target].name == "Harvest Golem":
                                        if curopfieldstat[target][1] <= 2:
                                            kill(target)
                                        else:
                                            curopfieldstat[target][3] = "Silence"
                                    else:
                                        if curopfieldstat[target][1] <= 2:
                                            kill(target)
                                        else:
                                            curopfieldstat[target][1] -= 2
                            elif play[-1].name == "Azure Drake":
                                if len(curdeck) > 0:
                                    curdraw()
                                spellatk += 1
                                score = score + 20
                            elif cardname == "Ancient of Lore":
                                if random.randrange(10) == 1:
                                    curhp[self.me] = min(hp[self.me] + 5, 30)
                                else:
                                    if len(curdeck) > 0:
                                        curdraw()
                                    if len(curdeck) > 0:
                                        curdraw()
                                    score = score + 50
                            elif cardname == "Sen'jin Shieldmasta":
                                score += 5
                                curfieldstat[-1][3] = "Taunt"
                            elif cardname == "Druid of the Claw":
                                score += 10
                                curfieldstat[-1][1] += 2
                                curfieldstat[-1][3] = "Taunt"
                            elif cardname == "Ancient of War":
                                score += 20
                                curfieldstat[-1][1] += 5
                                curfieldstat[-1][3] = "Taunt"
                if curmana >= 2:
                    curheroab = True
                    curmana -= 2
                    curhp[self.me] += 1
                    heroatk += 1
                if 0 >= hp[self.op]:
                    return self.me

                # 공격 페이즈
                def attack(a, t):
                    curfieldstat[a][1] -= curopfieldstat[t][0]
                    curopfieldstat[t][1] -= curfieldstat[a][0]
                    for i in range(len(curfieldstat) - 1, -1, -1):
                        if curfieldstat[i][1] <= 0:
                            dead(i)
                    for i in range(len(curopfieldstat) - 1, -1, -1):
                        if curopfieldstat[i][1] <= 0:
                            kill(i)

                targetorder = [i for i in range(len(curopfield))]
                if len(targetorder) != 0: random.shuffle(targetorder)
                if heroatk >= 1:
                    attacked = False
                    if attacked == False:
                        for t in targetorder:
                            if curopfieldstat[t][3] == "Taunt" and curhp[self.me] > curopfieldstat[t][0]:
                                curhp[self.me] -= curopfieldstat[t][0]
                                curopfieldstat[t][1] -= heroatk
                                if curopfieldstat[t][1] <= 0:
                                    kill(t)
                                attacked = True
                                break
                    if attacked == False:
                        for t in targetorder:
                            if heroatk >= curopfieldstat[t][1] and curhp[self.me] >= curopfieldstat[t][0]:
                                curhp[self.me] -= curopfieldstat[t][0]
                                curopfieldstat[t][1] -= heroatk
                                attacked = True
                                if curopfieldstat[t][1] <= 0:
                                    kill(t)
                                break
                    if attacked == False:
                        if random.randrange(2) == 0 or len(targetorder) == 0:
                            curhp[self.op] -= heroatk
                        else:
                            t = targetorder[0]
                            curhp[self.me] -= curopfieldstat[t][0]
                            curopfieldstat[t][1] -= heroatk
                            if curopfieldstat[t][1] <= 0:
                                kill(t)
                numatk = 1
                while numatk != 0:
                    numatk = 0
                    for i in range(len(curfieldstat)):
                        if curfieldstat[i][2] == True:
                            numatk += 1
                    if len(curfield) != 0:
                        attacker = random.randrange(len(curfield))
                        if curfieldstat[attacker][2] == True:
                            curfieldstat[attacker][2] = False
                            attacked = False
                            targetorder = [i for i in range(len(curopfield))]
                            if len(targetorder) != 0: random.shuffle(targetorder)
                            if attacked == False:
                                for t in targetorder:
                                    if curopfieldstat[t][3] == "Taunt":
                                        attack(attacker, t)
                                        attacked = True
                                        break
                            if attacked == False:
                                for t in targetorder:
                                    if curfieldstat[attacker][0] >= curopfieldstat[t][1] and curfieldstat[attacker][
                                        1] >= curopfieldstat[t][0]:
                                        attack(attacker, t)
                                        attacked = True
                                        break
                            if attacked == False:
                                if random.randrange(3) == 0 or len(targetorder) == 0:
                                    curhp[self.op] -= curfieldstat[attacker][0]
                                else:
                                    attack(attacker, targetorder[0])
                for i in range(len(curopfieldstat) - 1, -1, -1):
                    if curopfieldstat[i][1] <= 0:
                        kill(i)
                for i in range(len(curfieldstat) - 1, -1, -1):
                    if curfieldstat[i][1] <= 0:
                        dead(i)
                for i in range(len(curfield)):
                    curfieldstat[i][0] = curfield[i].game_tags[pyRosetta.GameTag.ATK]

                # 점수 페이즈
                def sumstat(player, stat):
                    sum = 0
                    if player == self.me:
                        if stat == "ATK":
                            for stats in curfieldstat:
                                sum += stats[0]
                        if stat == "HEALTH":
                            for stats in curfieldstat:
                                sum += stats[1]
                    if player == self.op:
                        if stat == "ATK":
                            for stats in curopfieldstat:
                                sum += stats[0]
                        if stat == "HEALTH":
                            for stats in curopfieldstat:
                                sum += stats[1]
                    return sum

                def sumtaunthp(player):
                    sum = 0
                    if player == self.me:
                        for stats in curfieldstat:
                            if stats[3] == "Taunt":
                                sum += stats[1]
                    if player == self.op:
                        for stats in curopfieldstat:
                            if stats[3] == "Taunt":
                                sum += stats[1]
                    return sum

                for i in range(len(curfieldstat) - 1, -1, -1):
                    if curfieldstat[i][3] == "treant":
                        dead(i)

                # 점수 계산
                if curhp[self.me] <= 0:
                    score -= 10000
                    return self.op
                if curhp[self.op] <= 0:
                    score += 10000
                    return self.me
                safemyhp = sumstat(self.op, "ATK") + 2 * len(curopfield) + 14
                score = score + 2 * (curhp[self.me])
                if curhp[self.me] > safemyhp - sumtaunthp(self.me):
                    score = score + 50
                safeophp = sumstat(self.me, "ATK") + 2 * len(curfield) + 14
                score = score - 2 * (curhp[self.op])
                if curhp[self.op] > safeophp - sumtaunthp(self.op):
                    score = score - 50
                score = score + sumstat(self.me, "ATK") * 10
                score = score + sumstat(self.me, "HEALTH") * 10
                score = score - sumstat(self.op, "ATK") * 10
                score = score - sumstat(self.op, "HEALTH") * 10

                for i in range(len(curfield)):
                    cardname = curfield[i].name
                    if cardname == "Sylvanas Windrunner" and curfieldstat[i][3] != "Silence":
                        score = score + 50
                    if cardname == "Cairne Bloodhoof" and curfieldstat[i][3] != "Silence":
                        score = score + 60
                    if cardname == "Harvest Golem" and curfieldstat[i][3] != "Silence":
                        score = score + 20
                for i in range(len(curopfield)):
                    cardname = curopfield[i].name
                    if cardname == "Sylvanas Windrunner" and curopfieldstat[i][3] != "Silence":
                        score = score - 50
                    if cardname == "Cairne Bloodhoof" and curopfieldstat[i][3] != "Silence":
                        score = score - 60
                    if cardname == "Harvest Golem" and curopfieldstat[i][3] != "Silence":
                        score = score - 20
                if score > bestscore:
                    bestscore = score
                    bestdeck[self.me] = curdeck[:]
                    bestdeck[self.op] = deckcard[self.op][:]
                    besthand[self.me] = curhand[:]
                    besthand[self.op] = handcard[self.op][:]
                    bestfield[self.me] = curfield[:]
                    bestfield[self.op] = curopfield[:]
                    bestfieldstat[self.me] = copy.deepcopy(curfieldstat)
                    bestfieldstat[self.op] = copy.deepcopy(curopfieldstat)
                    besthp = copy.deepcopy(curhp)
                    bestplaylog = play[:]
                    bestmaxmana[self.me] = curmaxmana
                    cmana[self.me] = curmana
                    heroab = curheroab

            deckcard[self.me] = bestdeck[self.me][:]
            deckcard[self.op] = bestdeck[self.op][:]
            handcard[self.me] = besthand[self.me][:]
            handcard[self.op] = besthand[self.op][:]
            fieldcard[self.me] = bestfield[self.me][:]
            fieldcard[self.op] = bestfield[self.op][:]
            fieldcardstat[self.me] = copy.deepcopy(bestfieldstat[self.me])
            fieldcardstat[self.op] = copy.deepcopy(bestfieldstat[self.op])
            hp = copy.deepcopy(besthp)
            playlog = bestplaylog
            maxmana = bestmaxmana[:]
            return -1

    def gamedisplay():
        pygame.init()
        font = pygame.font.SysFont(None, 60)
        font2 = pygame.font.SysFont(None, 40)
        Hero = pygame.image.load('./image/Hero.png')
        Hero = pygame.transform.scale(Hero, (int(Hero.get_rect().size[0] * 0.5), int(Hero.get_rect().size[1] * 0.5)))

        screen.fill((255, 255, 255))
        if myturn == 1:
            pygame.draw.rect(screen, (255, 255, 127), [0, 0, 1920, 480])
        elif myturn == 0:
            pygame.draw.rect(screen, (255, 255, 127), [0, 480, 1920, 480])
        screen.blit(Hero, (100, 0))
        screen.blit(Hero, (100, 701))
        pygame.draw.rect(screen, (255, 0, 0), [250, 179, 60, 60])
        pygame.draw.rect(screen, (255, 0, 0), [250, 880, 60, 60])
        pygame.draw.rect(screen, (0, 0, 255), [100, 20, 100, 40])
        pygame.draw.rect(screen, (0, 0, 255), [100, 721, 100, 40])
        text = font.render(str(hp[1]), True, (255, 255, 255))
        screen.blit(text, (255, 189))
        text = font.render(str(hp[0]), True, (255, 255, 255))
        screen.blit(text, (255, 890))
        text = font2.render(str(cmana[1]) + ' / ' + str(maxmana[1]), True, (255, 255, 255))
        screen.blit(text, (110, 27))
        text = font2.render(str(cmana[0]) + ' / ' + str(maxmana[0]), True, (255, 255, 255))
        screen.blit(text, (110, 728))
        text = font.render("Turn: " + str(turn), True, (0, 0, 0))
        screen.blit(text, (1620, 10))
        for i in range(len(handcard)):
            for j in range(len(handcard[i])):
                card = pygame.image.load('./image/' + handcard[i][j].name + '.webp')
                card = pygame.transform.scale(card,
                                              (int(Hero.get_rect().size[0] * 0.8), int(Hero.get_rect().size[1] * 0.8)))
                screen.blit(card, (350 + 150 * j, 20 + 700 * (1 - i)))
        for i in range(len(fieldcard)):
            for j in range(len(fieldcard[i])):
                if fieldcardstat[i][j][3] == "Taunt":
                    pygame.draw.rect(screen, (127, 127, 127), [40 + 180 * j, 255 + 230 * (1 - i), 155, 225])
                if fieldcardstat[i][j][3] == "Silence":
                    pygame.draw.rect(screen, (255, 127, 127), [40 + 180 * j, 255 + 230 * (1 - i), 155, 225])

                card = pygame.image.load('./image/' + fieldcard[i][j].name + '.webp')
                card = pygame.transform.scale(card,
                                              (int(Hero.get_rect().size[0] * 1), int(Hero.get_rect().size[1] * 1)))
                screen.blit(card, (20 + 180 * j, 230 + 230 * (1 - i)))
                pygame.draw.rect(screen, (127, 127, 0), [40 + 180 * j, 440 + 230 * (1 - i), 40, 40])
                pygame.draw.rect(screen, (255, 0, 0), [155 + 180 * j, 440 + 230 * (1 - i), 40, 40])
                text = font2.render(str(fieldcardstat[i][j][0]), True, (255, 255, 255))
                screen.blit(text, (50 + 180 * j, 445 + 230 * (1 - i)))
                text = font2.render(str(fieldcardstat[i][j][1]), True, (255, 255, 255))
                screen.blit(text, (165 + 180 * j, 445 + 230 * (1 - i)))
            card = pygame.image.load('./image/Card.webp')
            card = pygame.transform.scale(card,
                                          (int(Hero.get_rect().size[0] * 0.8), int(Hero.get_rect().size[1] * 0.8)))
            screen.blit(card, (1280, 260 + 230 * (1 - i)))
            text = font2.render(str(len(deckcard[i])), True, (255, 255, 255))
            screen.blit(text, (1340, 350 + 230 * (1 - i)))

        pygame.draw.rect(screen, (168, 168, 168), [1820, 0, 100, 960])
        text = font2.render("Log", True, (0, 0, 0))
        screen.blit(text, (1840, 0))
        for i in range(len(playlog)):
            card = pygame.image.load('./image/' + playlog[i].name + '.webp')
            card = pygame.transform.scale(card,
                                          (int(Hero.get_rect().size[0] * 0.5), int(Hero.get_rect().size[1] * 0.5)))
            screen.blit(card, (1820, 20 + 120 * i))
        if heroab == True:
            card = pygame.image.load('./image/Hero Power_Druid.webp')
            card = pygame.transform.scale(card,
                                          (int(Hero.get_rect().size[0] * 0.5), int(Hero.get_rect().size[1] * 0.5)))
            screen.blit(card, (1820, 20 + 120 * len(playlog)))

        pygame.display.update()

        click = False
        while not click:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        click = True
        text = font.render("Loading...", True, (0, 0, 0))
        screen.blit(text, (1620, 920))
        pygame.display.update()

    def printfield():
        for i in fieldcard[1]:
            print(i.name, end=' ')
        print()
        for i in fieldcardstat[1]:
            print(i)
        for i in fieldcardstat[0]:
            print(i)
        for i in fieldcard[0]:
            print(i.name, end=' ')
        print()
        print('--------------------------')

    p0 = cDruid(0)
    p1 = cDruid(1)
    myturn = -1
    first = 0
    turn = 0
    if DISPLAY:
        gamedisplay()
    p0.newgame(first)
    p1.newgame(first)
    if DISPLAY:
        gamedisplay()
    p0.mulligun(first)
    p1.mulligun(first)
    if DISPLAY:
        gamedisplay()
    winner = -1

    while True:
        if first == 0:
            myturn = 0
            turn += 1
            winner = p0.myturn(DEPTH=depth0)
            if winner != -1:
                break
            if DISPLAY:
                gamedisplay()
            # printfield()
            myturn = 1
            turn += 1
            winner = p1.myturn(DEPTH=depth1)
            if winner != -1:
                break
            if DISPLAY:
                gamedisplay()
            # printfield()
        else:
            myturn = 1
            turn += 1
            winner = p1.myturn(DEPTH=depth1)
            if winner != -1:
                break
            if DISPLAY:
                gamedisplay()
            # printfield()
            myturn = 0
            turn += 1
            winner = p0.myturn(DEPTH=depth0)
            if winner != -1:
                break
            if DISPLAY:
                gamedisplay()
            # printfield()

    if DISPLAY:
        gamedisplay()
        font3 = pygame.font.SysFont(None, 200)
        pygame.draw.rect(screen, (0, 0, 0), [610, 380, 700, 200])
        text = font3.render("winner: " + str(winner), True, (255, 255, 255))
        screen.blit(text, (620, 400))
        click = False
        pygame.display.update()
        while not click:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        click = True

    return winner

#시연
if DISPLAY:
    pygame.init()
    screen = pygame.display.set_mode((1920, 960))
    main = pygame.image.load('./image/Logo2.webp')
    main = pygame.transform.scale(main, (1920, 960))
    screen.blit(main, (0, 0))
    font = pygame.font.SysFont(None, 60)
    text = font.render("Loading...", True, (255, 255, 255))
    screen.blit(text, (1620, 920))
    pygame.display.update()

game(depth0=10000, depth1=10000)
if DISPLAY:
    pygame.quit()

#성능 테스트
#for i in [1,10,100,1000,3000]:
#    d0=i
#    if i==0: continue
#    for j in [1,10,100,1000,3000]:
#        win=0
#        for k in range(1000):
#            if game(depth0=d0, depth1=j)==0: win+=1
#        print (str(d0)+" vs "+str(j)+" : "+str(win))
