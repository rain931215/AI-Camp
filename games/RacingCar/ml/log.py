import os
import pickle

path = "../log"
allFile = os.listdir(path)
data_set = []
for file in allFile:
    with open(os.path.join(path, file), "rb") as f:
        data_set.append(pickle.load(f))

X = []
Y = []

for data in data_set:
    # print(data)
    for i, _ in enumerate(data['1P']["scene_info"][3:-2]):
        scene_info = data['1P']['scene_info'][i + 1]
        other_cars_position = scene_info["all_cars_pos"]
        for car in other_cars_position:
            # 去除玩家本身的車子
            if car[0] == scene_info["x"] and car[1] == scene_info["y"]:
                other_cars_position.remove(car)
        cmd = data['1P']['command'][i+1]
        Y.append(str(cmd))
        frontBlocked = False
        leftBlocked = False
        rightBlocked = False
        playerX = scene_info["x"]
        playerY = scene_info["y"]
        for car in other_cars_position:
            carX = car[0]
            carY = car[1]
            if carX < playerX - 30:
                continue
            if carX - playerX < 200 and abs(carY - playerY) <= 30:
                frontBlocked = True

            if carX - playerX < 100:
                if 30 <= abs(carY - playerY) <= 60:
                    if carY < playerY:
                        leftBlocked = True
                    else:
                        rightBlocked = True

        leftRoadBlocked = playerY <= 130
        rightRoadBlocked = playerY >= 550
        leftBlocked |= leftRoadBlocked
        rightBlocked |= rightRoadBlocked
        if not frontBlocked:
            leftRoadBlocked = False
            rightRoadBlocked = False
        data2 = (frontBlocked, leftBlocked, rightBlocked)
        X.append(data2)

from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)
#print(X)
print(Y)
from sklearn import tree

clf = tree.DecisionTreeClassifier()
clf = clf.fit(x_train, y_train)
tree.plot_tree(clf)

predicitions = clf.predict(x_test)

#print(predicitions)

from sklearn.metrics import accuracy_score
score = accuracy_score(y_test, predicitions)
print(F"Accuracy Score:{score}")

with open(os.path.join(os.path.dirname(__file__), "model.pickle"), "wb") as f:
    pickle.dump(clf, f)

