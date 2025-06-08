import pygame
import random
import time
import os

# 초기 설정
pygame.init()
pygame.mixer.init()
width, height = 1000, 600
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Dodge a Red Box")

# 색상
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

# 폰트
pygame.font.init()
font = pygame.font.SysFont("comicsans", 40)

# 플레이어 설정
player_size = 30
player_pos = [width / 2, height - 2 * player_size]
player_speed = 10

# 음악 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MUSIC_PATH = os.path.join(BASE_DIR, "240211_red box_music.wav")

pygame.mixer.music.load(MUSIC_PATH)
pygame.mixer.music.set_volume(1.0)

# 시계
clock = pygame.time.Clock()

# 게임 변수
score = 0
start_time = 0
game_started = False
game_over = False
enemies = []

# 물체 초기화
def reset_enemies():
    global enemies
    enemies = []
    add_enemy()

# 새로운 적 추가
def add_enemy():
    global enemies
    size = random.randint(10, 50)
    speed = random.randint(10, 30)
    edge = random.choice(['top', 'left', 'right'])

    if edge == 'top':
        pos = [random.randint(0, width - size), 0]
        direction = [0, speed]
    elif edge == 'left':
        pos = [0, random.randint(0, height - size)]
        direction = [speed, 0]
    else:  # right
        pos = [width - size, random.randint(0, height - size)]
        direction = [-speed, 0]

    enemies.append({'pos': pos, 'direction': direction, 'size': size})

# 게임 초기화
def initialize_game():
    global player_pos, enemies, score, start_time, game_started, game_over
    player_pos = [width / 2, height - 2 * player_size]
    reset_enemies()
    score = 0
    start_time = time.time()
    game_started = False
    game_over = False

# 시작 화면
def show_start_screen():
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.play(-1)

    win.fill(black)
    title = font.render("Dodge a Red Box", True, white)
    start_msg = font.render("Start : Spacebar", True, white)

    win.blit(title, title.get_rect(center=(width / 2, height / 2 - 40)))
    win.blit(start_msg, start_msg.get_rect(center=(width / 2, height / 2 + 40)))
    pygame.display.update()

# 게임 오버 화면
def show_game_over_screen():
    win.fill(black)
    over_msg = font.render("Game Over", True, white)
    score_msg = font.render(f"Playtime : {end_time - start_time:.2f} seconds", True, white)

    win.blit(over_msg, over_msg.get_rect(center=(width / 2, height / 2 - 40)))
    win.blit(score_msg, score_msg.get_rect(center=(width / 2, height / 2 + 20)))
    pygame.display.update()

# 게임 루프
initialize_game()
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
        # 플레이어 이동
        if keys[pygame.K_LEFT] and player_pos[0] > player_speed:
            player_pos[0] -= player_speed
        if keys[pygame.K_RIGHT] and player_pos[0] < width - player_size:
            player_pos[0] += player_speed
        if keys[pygame.K_UP] and player_pos[1] > player_speed:
            player_pos[1] -= player_speed
        if keys[pygame.K_DOWN] and player_pos[1] < height - player_size:
            player_pos[1] += player_speed

        # 난이도 증가에 따라 적 추가
        elapsed = time.time() - start_time
        if len(enemies) < int(elapsed // 5) + 1:  # 적 개수 증가 속도 조절
            add_enemy()

        win.fill(black)

        # 적 처리
        for enemy in list(enemies):
            enemy['pos'][0] += enemy['direction'][0]
            enemy['pos'][1] += enemy['direction'][1]

            pygame.draw.rect(win, red, (enemy['pos'][0], enemy['pos'][1], enemy['size'], enemy['size']))

            # 화면 밖이면 제거 및 점수 증가
            if (enemy['pos'][0] < 0 or enemy['pos'][0] > width or
                enemy['pos'][1] < 0 or enemy['pos'][1] > height):
                enemies.remove(enemy)
                score += 1

            # 충돌 체크
            if (player_pos[0] < enemy['pos'][0] + enemy['size'] and
                player_pos[0] + player_size > enemy['pos'][0] and
                player_pos[1] < enemy['pos'][1] + enemy['size'] and
                player_pos[1] + player_size > enemy['pos'][1]):
                end_time = time.time()
                game_over = True
                pygame.mixer.music.stop()

        # 플레이어 그리기
        pygame.draw.rect(win, white, (player_pos[0], player_pos[1], player_size, player_size))

        # 시간 표시
        time_text = font.render(f"Time: {elapsed:.2f} seconds", True, white)
        win.blit(time_text, (10, 10))

    # 상태 화면 표시
    if game_over:
        show_game_over_screen()
    elif not game_started:
        show_start_screen()

    pygame.display.update()
    clock.tick(30)

pygame.quit()
