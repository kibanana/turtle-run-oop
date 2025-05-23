import turtle
import pygame
import random
import sys
import time

class GameConfig:
    up = 90
    down = 270
    left = 180
    right = 0
    max_x = 250
    min_x = max_x - (max_x * 2)
    max_y = 250
    min_y = max_y - (max_y * 2)
    max_stamps = 5
    score_unit = 10
    colors = ["beige", "yellow", "pink", "orange", "red", "black"]
    shapes = ["hunter", "jewel", "twinkle"]
    enemy_shapes = ["devil", "skull", "ghost", "alien", "crocodile", "jellyfish"]
    freeze_time = 0.5

class GameVisualConfig:
    default_text_align = "center"
    default_font = "NeoDunggeunmo Pro" # TODO 추가 기능 7. Neo 둥근모 폰트 사용
    default_font_color = "white"
    default_shape = "blank"

class Hunter(turtle.Turtle): # Turtle 클래스 상속
    def __init__(self, speed = 1):
        turtle.Turtle.__init__(self)
        self.penup()

        # 이미지 파일 출처: https://emojipedia.org/apple/ios-18.4/turtle
        self.shape("shape_hunter.gif")
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
        self.setheading(GameConfig.up)
        
    def down(self):
        self.setheading(GameConfig.down)
        
    def left(self):
        self.setheading(GameConfig.left)
        
    def right(self):
        self.setheading(GameConfig.right)
        
    def move(self):
        self.forward(self.speed)

        # TODO 추가 기능 5. 캐릭터 화면 밖으로 나갈 수 없도록 처리
        x = self.xcor()
        y = self.ycor()

        if x > GameConfig.max_x:
            self.setheading(GameConfig.left)
        elif x < GameConfig.min_x:
            self.setheading(GameConfig.right)
        elif y > GameConfig.max_y:
            self.setheading(GameConfig.down)
        elif y < GameConfig.min_y:
            self.setheading(GameConfig.up)

        if self.stamp_idx >= GameConfig.max_stamps:
            self.clearstamps(GameConfig.max_stamps)
            self.stamp_idx = 0
        self.stamp()
        self.stamp_idx += 1
    
    def stop(self):
        self.hideturtle()
    
    def die(self):
        self.hideturtle()
        self.speed = 0
    
    def level_up(self, level):
        global turtle_speed
        self.speed = turtle_speed + level # 레벨업 - 캐릭터 속도 증가
        self.showturtle()
    
    def get_score(self):
        self.score += GameConfig.score_unit
    
    def lose_score(self):
        self.score -= GameConfig.score_unit
    
    def is_failed(self):
        global enemy_cnt
        return enemy_cnt <= 0
    
    def is_succeed(self):
        return self.score >= GameConfig.score_unit

class Enemy(turtle.Turtle): # Turtle 클래스 상속
    def __init__(self, hunter, speed = 1):
        turtle.Turtle.__init__(self)
        self.penup()

        # TODO 추가 기능 2. 적 이미지 랜덤 부여
        # 이미지 파일 출처: https://emojipedia.org/apple/ios-18.4
        self.shape(f"shape_{GameConfig.enemy_shapes[random.randint(0, 5)]}.gif")

        self.speed = speed
        self.goto(random.randint(GameConfig.min_x, GameConfig.max_x),
                  random.randint(GameConfig.min_y, GameConfig.max_y))
        
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

        if x > GameConfig.max_x:
            self.setheading(GameConfig.left)
        elif x < GameConfig.min_x:
            self.setheading(GameConfig.right)
        elif y > GameConfig.max_y:
            self.setheading(GameConfig.down)
        elif y < GameConfig.min_y:
            self.setheading(GameConfig.up)

        # TODO 추가 기능 4. 적이 정확히 캐릭터를 따라오도록 방향 조정
        if random.randint(1, 100) == 1:
            self.setheading(self.towards(self.hunter))
        
        if self.stamp_idx >= GameConfig.max_stamps:
            self.clearstamps(GameConfig.max_stamps)
            self.stamp_idx = 0
        self.stamp()
        self.stamp_idx += 1
    
    def stop(self):
        self.hideturtle()
    
    def die(self):
        global enemy_cnt
        self.clear()
        self.hideturtle()
        self.speed = 0
        enemy_cnt -= 1

    def level_up(self, level):
        global enemy_speed
        self.speed = enemy_speed + level # 레벨업 - 적 속도 증가
        self.showturtle()
    
class Jewel(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.penup()
        self.shape(GameVisualConfig.default_shape)
        self.goto(random.randint(GameConfig.min_x, GameConfig.max_x), random.randint(GameConfig.min_y, GameConfig.max_y))
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
        self.clear()
        self.hideturtle()
        jewel_cnt -= 1
    
    def level_up(self):
        self.showturtle() # 레벨업 - 보석 재생성

class FloatingMessage(turtle.Turtle):
    def __init__(self, position = "bottom"):
        turtle.Turtle.__init__(self)
        self.content = None
        self.shape(GameVisualConfig.default_shape)
        self.color(GameVisualConfig.default_font_color)
        if position == "top":
            self.xcor = 0
            self.ycor = 90
        elif position == "middle":
            self.xcor = 0
            self.ycor = 145
        elif position == "bottom":
            self.xcor = 0
            self.ycor = 200
    
    def display_score(self, score):
        global turtle 

        self.content = f"Score: {str(score)}"

        self.clear()
        self.teleport(self.xcor, self.ycor)
        self.write(self.content,
                   False,
                   GameVisualConfig.default_text_align,
                   (GameVisualConfig.default_font, 30))
        turtle.update()

    def display_content(self, content):
        global turtle 

        self.content = content
        self.clear()
        self.teleport(self.xcor, self.ycor)
        self.write(self.content,
                   False,
                   GameVisualConfig.default_text_align,
                   (GameVisualConfig.default_font, 30))
        turtle.update()
        time.sleep(GameConfig.freeze_time)

class GameManager: # Game -> GameManager 클래스 변경 후 역할 변경
    def __init__(self, initial_et, initial_jt, s, hunter, floating_message, floating_score, floating_countdown):
        self.initial_et = initial_et
        self.initial_jt = initial_jt
        self.s = s
        self.hunter = hunter
        self.enemies = []
        self.jewels = []
        self.floating_message = floating_message
        self.floating_score = floating_score
        self.floating_countdown = floating_countdown
        self.is_continued = True
        self.level = 1

        self._reset(initial_et, initial_jt)

    def start(self):
        # TODO 추가 기능 3. 시작 카운트다운
        self.floating_countdown.display_content("Start !")
        for i in range(3):
            self.floating_countdown.display_content(str(3 - i))
        self.floating_countdown.clear()
    
    def score(self):
        if self.is_continued is False:
            time.sleep(GameConfig.freeze_time)
            # TODO 기본 기능 1. 게임 종료
            sys.exit(1)
        
        if gameManager._is_level_clear():
            self._level_up()
        elif hunter.is_failed():
            self._end()
        else:
            self.floating_score.display_score(hunter.score) # 게임 진행 메시지: 점수

    def _reset(self, enemy_cnt, jewel_cnt):
        for e in self.enemies:
            e.die()
        
        for j in self.jewels:
            j.die()
        
        self.enemies.clear()
        for _ in range(enemy_cnt): # 적 {enemy_cnt}개 생성
            enemy = Enemy(hunter, enemy_speed)
            self.enemies.append(enemy)
        
        self.jewels.clear()
        for _ in range(jewel_cnt): # 보물 {jewel_cnt}개 생성
            self.jewels.append(Jewel())

    def _end(self):
        self.hunter.stop()
        for e in self.enemies:
            e.stop()
        self.floating_message.display_content("Failed!") # 게임 종료 메시지: 실패
        self.is_continued = False

    # TODO 추가 기능 6. 레벨업
    def _level_up(self):
        global enemy_cnt
        global jewel_cnt
        
        self.hunter.stop()
        for e in self.enemies:
            e.stop()

        # 게임 진행 메시지: 완료 & 레벨업
        self.floating_message.display_content(f"Complete ! Level {self.level}")
        self.floating_message.clear()

        self.level += 1
        self.hunter.level_up(self.level)
        self._reset(self.initial_et, self.initial_jt)
        for e in self.enemies:
            e.level_up(self.level)
        enemy_cnt = len(self.enemies)
        for j in self.jewels:
            j.level_up()
        jewel_cnt = len(self.jewels)

        self.start()

    def _is_level_clear(self):
        global jewel_cnt
        return jewel_cnt <= 0

# TODO 추가 기능 1. 입력 간소화
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

# TODO 기본 기능 2. 스크린 배경 그림 넣기
# 이미지 파일 출처: https://www.freepik.com/free-photo/abstract-bright-green-square-pixel-tile-mosaic-wall-background-texture_18487439.htm#fromView=search&page=2&position=19&uuid=f54e2323-252e-4269-be22-c853ed323aa2&query=Game+Background
s.bgpic("bg.png")

# TODO 기본 기능 4. 효과음 넣기(따로 재생)
# 음원 파일 출처: https://pixabay.com/ko/music/search/genre/%eb%a9%8d%ec%b2%ad%ec%9d%b4/?pagi=2
pygame.mixer.init()
pygame.mixer.music.load("bgm.mp3")

s.setup(500, 500)
s.tracer(0) # 코드 실행 과정을 화면에 표시하지 않음

pygame.mixer.music.play(-1)

floating_message = FloatingMessage("top")

if turtle_speed == 0 or enemy_cnt == 0 or enemy_speed == 0 or jewel_cnt == 0:
    # 게임 종료 메시지: 게임을 시작할 수 없음
    floating_message.display_content("Can't Start Game !")
    time.sleep(GameConfig.freeze_time)
    # TODO 기본 기능 1. 게임 종료
    sys.exit(1)

# TODO 기본 기능 3. 캐릭터, 적, 보석 이미지 바꾸기
shapes = GameConfig.shapes + GameConfig.enemy_shapes
for shape in shapes:
    s.register_shape(f"shape_{shape}.gif")

hunter = Hunter(turtle_speed)

floating_score = FloatingMessage("bottom")
floating_score.display_score(0)

floating_countdown = FloatingMessage("middle")

gameManager = GameManager(enemy_cnt, jewel_cnt, s, hunter, floating_message, floating_score, floating_countdown)

turtle.listen()
turtle.onkeypress(hunter.up, "Up")
turtle.onkeypress(hunter.down, "Down")
turtle.onkeypress(hunter.left, "Left")
turtle.onkeypress(hunter.right, "Right")

gameManager.start()

while True:
    s.update()
    hunter.move()

    for e in gameManager.enemies[:]:
        e.move()
        if hunter.distance(e) < 12:
            e.die()
            gameManager.enemies.remove(e)
            hunter.lose_score()
    
    for j in gameManager.jewels[:]:
        j.twinkle()
        if hunter.distance(j) < 12:
            j.die()
            gameManager.jewels.remove(j)
            hunter.get_score()
            if hunter.is_succeed():
                floating_message.display_content("Success") # 게임 진행 메시지: 성공
    
    gameManager.score()
    time.sleep(0.01) # 게임 진행/종료 메시지 보여주기 위함
