class MLPlay:
    def __init__(self):
        self.other_cars_position = []
        self.coins_pos = []
        self.player_pos = (0, 0)
        self.leftRoadBlocked = False
        self.rightRoadBlocked = False
        print("Initial ml script")

    def update(self, scene_info: dict):
        """
        Generate the command according to the received scene information
        """
        # print(scene_info)
        if scene_info["status"] != "GAME_ALIVE":
            return "RESET"

        self.player_pos = (scene_info["x"], scene_info["y"])
        self.other_cars_position = scene_info["all_cars_pos"]
        for i in self.other_cars_position:
            # 去除玩家本身的車子
            if i[0] == self.player_pos[0] and i[1] == self.player_pos[1]:
                self.other_cars_position.remove(i)

        frontBlocked = False
        leftBlocked = False
        rightBlocked = False
        playerX = self.player_pos[0]
        playerY = self.player_pos[1]
        for i in self.other_cars_position:
            carX = i[0]
            carY = i[1]

            if carX < playerX-90:
                continue
            if carX - playerX < 230 and abs(carY - self.player_pos[1]) <= 30:
                frontBlocked = True

            if carX - playerX < 100:
                if 30 <= abs(carY - playerY) <= 60:
                    if carY < playerY:
                        leftBlocked = True
                    else:
                        rightBlocked = True

        if playerY <= 130:
            self.leftRoadBlocked = True
        elif playerY >= 160:
            self.leftRoadBlocked = False
        if playerY >= 490:
            self.rightRoadBlocked = True
        elif playerY <= 460:
            self.rightRoadBlocked = False
        leftBlocked |= self.leftRoadBlocked
        rightBlocked |= self.rightRoadBlocked
        #print(
        #    F"X:{self.player_pos[0]}, Y:{self.player_pos[1]}, FRONT:{frontBlocked}, LEFT:{leftBlocked}, RIGHT:{rightBlocked}")
        if frontBlocked:
            if leftBlocked and rightBlocked:
                #print('BRAKE')
                return ['BRAKE']
            elif leftBlocked:
                #print('MOVE_RIGHT')
                return ['MOVE_RIGHT']
            else:
                #print('MOVE_LEFT')
                return ['MOVE_LEFT']
        #print('SPEED')
        return ["SPEED"]

    def reset(self):
        """
        Reset the status
        """
        # print("reset ml script")
        pass
