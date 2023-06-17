import RPi.GPIO as GPIO
import time
import random

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

raw = 8
column = 8
info = [[[0, 0, 0, 0] for i in range(raw)] for j in range(column)]

pinLed = 22
pinSw = 21
pinLedA = [5, 6, 7, 8, 9, 10, 11, 12]
pinLedC = [13, 14, 15, 16, 17, 18, 19, 20]

GPIO.setup(pinSw, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def remove_specified_values(arr, value):
    while value in arr:
        arr.remove(value)

def Lit(info, i, j):
    rawlist = list(range(raw))
    columnlist = list(range(column))

    if ((info[i][j])[0] == 1):
        remove_specified_values(rawlist, i)
        remove_specified_values(columnlist, j)
        GPIO.output(pinLedA[i], GPIO.HIGH)
        GPIO.output(pinLedC[j], GPIO.LOW)
        
        for k in rawlist:
            GPIO.output(pinLedA[k], GPIO.LOW)
        for l in columnlist:
            GPIO.output(pinLedC[l], GPIO.HIGH)
        time.sleep(0.0000000018)
        
    elif( (info[i][j])[0] == 0 ):
        for k in rawlist:
            GPIO.output(pinLedA[k], GPIO.HIGH)
        for l in columnlist:
            GPIO.output(pinLedC[l], GPIO.HIGH)
        time.sleep(0.0000000002)

def displayAnimation(n):
    global info
    #マトリクスLEDにアニメーションを出力する関数
    position = []
    amount = random.randrange(raw)        #どのくらいの量を降らすのかの定義
    list_position = list(range(column))
    print("list_position", list_position)
    print("amount", amount)
    position = random.sample(list_position,amount)  #どの位置から降らすのかの定義
    position = sorted(position)#positionをソート
    print("position", position)
    speed = [0] * (column)
    for i in position:
        speed[i] = random.randrange(n, n+2, 1) #雨の速さを決定する
    check = [0] * (column)
    checksum = 0
    for insert in position:#info行列の各要素を決定する
        for i in range(raw):
            for j in range(column):
                check[j] += (info[i][j])[0]
        for k in range(column):
            checksum += check[k]
        if(checksum <= 4 and check[insert] == 0 and (info[0][insert])[0] == 0):#光っていない時のみ代入する
            (info[0][insert])[0] = 1
            (info[0][insert])[1] = speed[insert]
            (info[0][insert])[2] = speed[insert]
            (info[0][insert])[3] = 3
    for _ in range(40):#光らせる
        for i in range(raw):
            for j in range(column):
                Lit(info, i, j)
    
    #移動を行う。
    for i in range(raw):
        for j in range(column):
            if(i == raw-1):
                if((info[i][j])[2] > 0 and (info[i][j])[1] == 0 ):
                    if((info[i][j])[3] == 0 ):
                        (info[i][j])[0] = 0#shoutou
                        (info[i][j])[2] = 0
                    else:
                        (info[i][j])[3] -= 1 
                else:
                    (info[i][j])[1] -= 1#taikyuujikann-1
            elif((info[i][j])[0] == 1 ):        
                if((info[i][j])[2] > 0 and (info[i][j])[1] == 0 ):
                    if((info[i][j])[3] == 0):
                        (info[i][j])[0] = 0#shoutou
                        (info[i+1][j])[0] = 1
                        (info[i+1][j])[1] = (info[i][j])[2]
                        (info[i+1][j])[2] = (info[i][j])[2]
                        (info[i][j])[2] = 0
                    else:
                        (info[i][j])[3] -= 1
                        (info[i+1][j])[0] = 1
                        (info[i+1][j])[1] = (info[i][j])[2]
                        (info[i+1][j])[2] = (info[i][j])[2]
                        
                else:
                    (info[i][j])[1] -= 1#taikyuujikann-1


for i in range(raw):
    GPIO.setup(pinLedA[i], GPIO.OUT)
for i in range(column):
    GPIO.setup(pinLedC[i], GPIO.OUT)

lastState = GPIO.LOW
count = 1
try:
	while True:
		newState = GPIO.input(pinSw)
		if ((newState == GPIO.HIGH) and (lastState == GPIO.LOW)):
			while True:
				displayAnimation(count)
				if (GPIO.input(pinSw) == GPIO.HIGH):
					for i in range(raw):
						GPIO.output(pinLedA[i], GPIO.LOW)
					for i in range(column):
						GPIO.output(pinLedC[i], GPIO.LOW)
					break
			if (count >= 3):
				count = 1
			else:
				count += 1
			time.sleep(0.2)#チャタリング除去
		lastState = newState
    
        
finally:
	# Ctrl + C de shokika
    for i in range(raw):
        GPIO.output(pinLedA[i], GPIO.LOW)
    for i in range(column):
        GPIO.output(pinLedC[i], GPIO.LOW)
