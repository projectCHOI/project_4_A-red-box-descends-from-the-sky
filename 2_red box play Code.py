import pygame
import random
import time

# 게임 초기화 및 설정
pygame.init()
width, height = 1000, 600
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Dodge a Red Box")

# 색상 설정
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

# 폰트 설정
pygame.font.init()
font = pygame.font.SysFont("comicsans", 40)

# 플레이어 설정
player_size = 50
player_speed = 40

# 떨어지는 물체 설정
enemy_size = 50
enemy_speed = 40
#
# pygame.mixer 모듈 초기화
pygame.mixer.init()

# 음악 파일 로드
pygame.mixer.music.load('C:\\Users\\HOME\\Desktop\\새싹_교육\\GitHub_CHOI\\project_4_A-red-box-descends-from-the-sky\\240211_red box_music.wav')
pygame.mixer.music.play(-1)  # -1은 음악을 무한 반복 재생

# 게임 시작 화면에서 음악 재생 시작
def show_start_screen():
    global game_started
    win.fill(black)
    title = font.render("Dodge a Red Box", True, white)
    start_message = font.render("Start : Spacebar", True, white)

    # 타이틀과 시작 메시지의 중앙 정렬
    title_rect = title.get_rect(center=(width / 2, height / 2 - 40))
    start_message_rect = start_message.get_rect(center=(width / 2, height / 2 + 40))

    win.blit(title, title_rect)
    win.blit(start_message, start_message_rect)
    pygame.display.update()

#
    
# 게임 변수 초기화 함수
def initialize_game():
    global player_pos, enemy_pos, score, start_time, game_started, game_over
    player_pos = [width / 2, height - 2 * player_size]
    enemy_pos = [random.randint(0, width - enemy_size), 0]
    score = 0
    start_time = 0
    game_started = False
    game_over = False
    pygame.mixer.music.stop() # 이전 게임에서 음악이 재생되고 있다면 중지

# 음악 볼륨 설정 (최대 볼륨)
pygame.mixer.music.set_volume(1.0)


# 시계 설정
clock = pygame.time.Clock()

# 물체의 초기 위치와 방향 설정 함수
def reset_enemy():
    global enemy_pos, enemy_direction, enemy_size
    enemy_size = random.randint(10, 50)  # 물체 크기를 10에서 50 사이의 랜덤한 값으로 설정
    edge = random.choice(['top', 'bottom', 'left', 'right'])
    
    if edge == 'top':
        enemy_pos = [random.randint(0, width - enemy_size), 0]
        enemy_direction = [0, enemy_speed]
    elif edge == 'bottom':
        enemy_pos = [random.randint(0, width - enemy_size), height - enemy_size]
        enemy_direction = [0, -enemy_speed]
    elif edge == 'left':
        enemy_pos = [0, random.randint(0, height - enemy_size)]
        enemy_direction = [enemy_speed, 0]
    else:  # edge == 'right'
        enemy_pos = [width - enemy_size, random.randint(0, height - enemy_size)]
        enemy_direction = [-enemy_speed, 0]


# 게임 변수 초기화 함수
def initialize_game():
    global player_pos, enemy_pos, score, start_time, game_started, game_over
    player_pos = [width / 2, height - 2 * player_size]
    enemy_pos = [random.randint(0, width - enemy_size), 0]
    score = 0
    start_time = 0
    game_started = False
    game_over = False
    reset_enemy() # 물체의 초기 위치와 방향 설정

# 게임 변수 초기화
initialize_game()

# 여러 떨어지는 물체들을 관리하기 위한 리스트 초기화
enemies = []

# 떨어지는 물체 설정
def reset_enemies():
    global enemies
    enemies = [{'pos': [random.randint(0, width - enemy_size), 0], 'direction': [0, enemy_speed], 'size': enemy_size}]

# 게임 변수 초기화 함수 수정
def initialize_game():
    global player_pos, enemies, score, start_time, game_started, game_over
    player_pos = [width / 2, height - 2 * player_size]
    reset_enemies()  # 여러 물체를 관리하기 위한 초기화
    score = 0
    start_time = time.time()
    game_started = False
    game_over = False

# 새로운 물체를 추가하는 함수
def add_enemy():
    global enemies
    enemy_size = random.randint(10, 50)
    edge = random.choice(['top', 'left', 'right'])
    if edge == 'top':
        new_enemy = {'pos': [random.randint(0, width - enemy_size), 0], 'direction': [0, enemy_speed], 'size': enemy_size}
    elif edge == 'left':
        new_enemy = {'pos': [0, random.randint(0, height - enemy_size)], 'direction': [enemy_speed, 0], 'size': enemy_size}
    else:
        new_enemy = {'pos': [width - enemy_size, random.randint(0, height - enemy_size)], 'direction': [-enemy_speed, 0], 'size': enemy_size}
    enemies.append(new_enemy)

# 물체의 속도를 랜덤하게 만드는 함수
def add_enemy():
    global enemies
    enemy_size = random.randint(10, 50)
    enemy_speed = random.randint(10, 30)  # 여기에서 랜덤한 속도를 설정
    edge = random.choice(['top', 'left', 'right'])
    if edge == 'top':
        new_enemy = {'pos': [random.randint(0, width - enemy_size), 0], 'direction': [0, enemy_speed], 'size': enemy_size}
    elif edge == 'left':
        new_enemy = {'pos': [0, random.randint(0, height - enemy_size)], 'direction': [enemy_speed, 0], 'size': enemy_size}
    else:  # edge == 'right'
        new_enemy = {'pos': [width - enemy_size, random.randint(0, height - enemy_size)], 'direction': [-enemy_speed, 0], 'size': enemy_size}
    enemies.append(new_enemy)

# 시계 설정
clock = pygame.time.Clock()

# 플레이어 설정
player_size = 30
player_pos = [width / 2, height - 2 * player_size]
player_speed = 10

# 떨어지는 물체 설정
enemy_size = 50
enemy_pos = [random.randint(0, width - enemy_size), 0]
enemy_speed = 10


clock = pygame.time.Clock()

# 게임 변수
score = 0
game_started = False

# 시작 화면 함수
def show_start_screen():
    win.fill(black)
    title = font.render("Dodge a Red Box", True, white)
    start_message = font.render("Start : Spacebar", True, white)

    # 타이틀과 시작 메시지의 중앙 정렬
    title_rect = title.get_rect(center=(width / 2, height / 2 - 40))
    start_message_rect = start_message.get_rect(center=(width / 2, height / 2 + 40))

    win.blit(title, title_rect)
    win.blit(start_message, start_message_rect)
    pygame.display.update()

# 게임 종료 화면 함수
def show_game_over_screen():
    win.fill(black)
    game_over_message = font.render("Game Over", True, white)
    score_message = font.render(f"Playtime : {end_time - start_time:.2f} seconds", True, white)

    # 게임 오버 메시지와 점수 메시지의 중앙 정렬
    game_over_message_rect = game_over_message.get_rect(center=(width / 2, height / 2 - 40))
    score_message_rect = score_message.get_rect(center=(width / 2, height / 2 + 20))

    win.blit(game_over_message, game_over_message_rect)
    win.blit(score_message, score_message_rect)
    pygame.display.update()
    
# 게임 루프
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if game_over:
        if keys[pygame.K_SPACE]:
            initialize_game()

    elif not game_started:
        if keys[pygame.K_SPACE]:
            game_started = True
            start_time = time.time()

    else:
        # 플레이어 이동 처리 로직을 유지합니다.
        if keys[pygame.K_LEFT] and player_pos[0] > player_speed:
            player_pos[0] -= player_speed
        if keys[pygame.K_RIGHT] and player_pos[0] < width - player_size:
            player_pos[0] += player_speed
        if keys[pygame.K_UP] and player_pos[1] > player_speed:
            player_pos[1] -= player_speed
        if keys[pygame.K_DOWN] and player_pos[1] < height - player_size:
            player_pos[1] += player_speed

        if game_started and not game_over:
            # 시간에 따라 새로운 물체 추가
            elapsed_time = time.time() - start_time
            if len(enemies) < elapsed_time // 10 + 1:
                add_enemy()

            win.fill(black)  # 화면을 먼저 지웁니다.

            # 물체 업데이트 및 충돌 검사 및 그리기
            for enemy in list(enemies):  # 리스트를 복사하여 반복 중 수정을 허용
                enemy['pos'][0] += enemy['direction'][0]
                enemy['pos'][1] += enemy['direction'][1]
                
                pygame.draw.rect(win, red, (enemy['pos'][0], enemy['pos'][1], enemy['size'], enemy['size']))

                # 화면 밖으로 나가면 리셋
                if enemy['pos'][0] < 0 or enemy['pos'][0] > width or enemy['pos'][1] < 0 or enemy['pos'][1] > height:
                    enemies.remove(enemy)
                    score += 1
                # 충돌 검사
                if player_pos[0] < enemy['pos'][0] + enemy['size'] and player_pos[0] + player_size > enemy['pos'][0]:
                    if player_pos[1] < enemy['pos'][1] + enemy['size'] and player_pos[1] + player_size > enemy['pos'][1]:
                        end_time = time.time()
                        game_over = True

            # 플레이어 그리기
            pygame.draw.rect(win, white, (player_pos[0], player_pos[1], player_size, player_size))

            # 게임 진행 시간 표시
            if not game_over:
                elapsed_time = time.time() - start_time
                time_text = font.render(f"Time: {elapsed_time:.2f} seconds", True, white)
                win.blit(time_text, (10, 10))

    # 게임 시작 화면 또는 게임 오버 화면 표시
    if game_over:
        show_game_over_screen()
    elif not game_started:
        show_start_screen()

    pygame.display.update()
    clock.tick(30)

pygame.quit()