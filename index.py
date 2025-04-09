import turtle
import pygame
import random
import sys
import time

default_text_align = "center"
default_font = "NeoDunggeunmo Pro"
default_font_color = "white"
default_shape = "blank"
default_freeze_time = 1

max_x = 250
min_x = max_x - (max_x * 2)
max_y = 250
min_y = max_y - (max_y * 2)
colors = ["beige", "yellow", "pink", "orange", "red", "black"]
shapes = ["hunter", "jewel", "twinkle"]
enemy_shapes = ["devil", "skull", "ghost", "alien", "crocodile", "jellyfish"]

class Hunter(turtle.Turtle): # Turtle 클래스 상속
    def __init__(self, speed = 1):
        turtle.Turtle.__init__(self)
        self.penup()

        self.shape("shape_hunter.gif")
        # 출처: https://emojipedia.org/apple/ios-18.4/turtle
        self.speed = speed
        self.score = 0
        
        self.stamp_idx = 0
    
    def location(self):
        h = self.heading()
        x = self.xcor()
        y = self.ycor()
        dis = self.distance(self)

        print("Location of TresureHunter: ")
        print(f"X Coor: {x}, Y Coor: {y}, Direction: {h}")
        print(f"Distance: {dis}")

    def up(self):
        self.setheading(90)
        
    def down(self):
        self.setheading(90 * 3)
        
    def left(self):
        self.setheading(90 * 2)
        
    def right(self):
        self.setheading(0)
        
    def move(self):
        self.forward(self.speed)

        # TODO 추가 기능 5. Hunter가 화면 밖으로 나갈 수 없도록 처리
        x = self.xcor()
        y = self.ycor()

        if x > max_x:
            self.setheading(90 * 2)
        elif x < min_x:
            self.setheading(0)
        elif y > max_y:
            self.setheading(90 * 3)
        elif y < min_y:
            self.setheading(90)

        if self.stamp_idx >= 5:
            self.clearstamps(5)
            self.stamp_idx = 0
        self.stamp()
        self.stamp_idx += 1
    
    def stop(self):
        self.speed = 0
    
    def die(self):
        self.hideturtle()
    
    def get_score(self):
        self.score += 10
    
    def lose_score(self):
        self.score -= 10
    
    def is_failed(self):
        return self.score < 0
    
    def is_succeed(self):
        return self.score >= 10

class Enemy(turtle.Turtle): # Turtle 클래스 상속
    def __init__(self, hunter, speed = 1):
        turtle.Turtle.__init__(self)
        self.penup()

        # TODO 추가 기능 2. 적 이미지 랜덤 부여
        self.shape(f"shape_{enemy_shapes[random.randint(0, 5)]}.gif")

        self.speed = speed
        self.goto(random.randint(min_x, max_x), random.randint(min_y, max_y))
        
        self.stamp_idx = 0
        self.hunter = hunter
        
    def location(self):
        h = self.heading()
        x = self.xcor()
        y = self.ycor()
        dis = self.distance(self)

        print("Location of Enemy: ")
        print(f"X Coor: {x}, Y Coor: {y}, Direction: {h}")
        print(f"Distance: {dis}")
        
    def move(self):
        self.forward(self.speed)

        x = self.xcor()
        y = self.ycor()

        if x > max_x:
            self.setheading(90 * 2)
        elif x < min_x:
            self.setheading(0)
        elif y > max_y:
            self.setheading(90 * 3)
        elif y < min_y:
            self.setheading(90)

        if random.randint(1, 100) == 1: # TODO 추가 기능 4. 적이 무작위가 아니라 정확히 헌터를 따라오도록
            self.setheading(self.towards(self.hunter))
        
        if self.stamp_idx >= 5:
            self.clearstamps(5)
            self.stamp_idx = 0
        self.stamp()
        self.stamp_idx += 1
    
    def stop(self):
        self.speed = 0
    
    def die(self):
        global enemy_cnt
        self.hideturtle()
        enemy_cnt -= 1
    
class Jewel(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.penup()
        self.shape(default_shape)
        self.goto(random.randint(min_x, max_x), random.randint(min_y, max_y))
        self.is_twinkle = False
    
    def twinkle(self):
        if self.is_twinkle == False:
            self.shape("shape_twinkle.gif")
            self.is_twinkle = True
        else:
            self.shape("shape_jewel.gif")
            self.is_twinkle = False
    
    def die(self):
        global jewel_cnt
        self.hideturtle()
        jewel_cnt -= 1

class FloatingMessage(turtle.Turtle):
    content = None

    def __init__(self, position = "bottom"):
        turtle.Turtle.__init__(self)
        self.shape(default_shape)
        self.color(default_font_color)
        if position == "top":
            self.xcor = 0
            self.ycor = 90
        elif position == "bottom":
            self.xcor = 0
            self.ycor = 200
    
    def display_score(self, score):
        self.content = f"Score: {str(score)}"

        self.clear()
        self.teleport(self.xcor, self.ycor)
        self.write(self.content, False, default_text_align, (default_font, 30))

    def display_content(self, content):
        self.content = content
    
        self.clear()
        self.teleport(self.xcor, self.ycor)
        self.write(self.content, False, default_text_align, (default_font, 30))

class Game(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.penup()
        self.hideturtle()
        self.speed(0)
        self.shape(default_shape)
        self.goto(200, 200)
        self.score = 0 # 여기서는 game score
        self.is_running = True
    
    def scoring(self, hunter, enemies, floating_message, floating_score):
        self.clear()
        
        if self.is_running is False:
            time.sleep(default_freeze_time)
            sys.exit(1)
        
        floating_score.display_score(hunter.score) # 게임 진행 메시지: 점수
        
        if hunter.is_failed():
            self.goto(0, 0)
            hunter.stop()
            for e in enemies:
                e.stop()
            floating_message.display_content("Failed !") # 게임 종료 메시지: 실패
            self.is_running = False
        elif jewel_cnt <= 0:
            self.goto(0, 0)
            hunter.stop()
            for e in enemies:
                e.stop()
            floating_message.display_content("Complete !") # 게임 종료 메시지: 완료
            self.is_running = False

# TODO 추가기능 1. 입력 간소화
input = input()
tmp_input = None
if input.count(" ") == 0: # 숫자 하나만 입력하는 경우 처리
    tmp_input = [int(input)] * 4
elif input.count(" ") == 3: # 숫자 4개 다 입력하는 경우 처리
    tmp_input = map(int, input.split())
else:
    tmp_input = [0] * 4
turtle_speed, enemy_cnt, enemy_speed, jewel_cnt = tmp_input

s = turtle.Screen()
s.title("거북이 보물찾기 게임")

s.bgpic("bg.jpg") # 음원 파일 출처: GPT

# pygame.init() # 에러 발생 원인
s = turtle.Screen()
pygame.mixer.init()
pygame.mixer.music.load("bgm.mp3") # 배경 이미지 파일 출처: https://pixabay.com/ko/music/search/genre/%eb%a9%8d%ec%b2%ad%ec%9d%b4/?pagi=2

game = Game()

s.setup(500, 500)
s.tracer(0) # 코드 실행 과정을 화면에 표시하지 않음

pygame.mixer.music.play(-1)

floating_message = FloatingMessage("top")

if turtle_speed == 0 or enemy_cnt == 0 or enemy_speed == 0 or jewel_cnt == 0:
    floating_message.display_content("Can't Start Game !") # 게임 종료 메시지: 게임을 시작할 수 없음
    time.sleep(default_freeze_time)
    sys.exit(1)

floating_score = FloatingMessage("bottom")
floating_score.display_score(0)

shapes = shapes + enemy_shapes
for shape in shapes:
    s.register_shape(f"shape_{shape}.gif")

hunter = Hunter(turtle_speed)
# hunter.location()

enemies = []
for i in range(enemy_cnt): # 적 거북들 {enemy_cnt}개 생성
    enemy = Enemy(hunter, enemy_speed)
    enemies.append(enemy)
    # enemy.location()

jewels = []
for i in range(jewel_cnt): # 보물 {jewel_cnt}개 생성
    jewels.append(Jewel())

turtle.listen()
turtle.onkeypress(hunter.up, "Up")
turtle.onkeypress(hunter.down, "Down")
turtle.onkeypress(hunter.left, "Left")
turtle.onkeypress(hunter.right, "Right")

# TODO 추가 기능 3. 시작 카운트다운
floating_message.display_content("Start !")
for i in range(3):
    s.update()
    floating_message.display_content(str(3 - i))
    time.sleep(default_freeze_time)

while True:
    s.update()
    hunter.move()

    for e in enemies:
        e.move()
        if hunter.distance(e) < 12:
            e.die()
            enemies.remove(e)
            hunter.lose_score()
    
    for j in jewels:
        j.twinkle()
        if hunter.distance(j) < 12:
            j.die()
            jewels.remove(j)
            hunter.get_score()
            if hunter.is_succeed():
                floating_message.display_content("Success") # 게임 진행 메시지: 성공
    
    game.scoring(hunter, enemies, floating_message, floating_score)
    time.sleep(0.01) # 게임 종료 메시지 보여주기 위함
