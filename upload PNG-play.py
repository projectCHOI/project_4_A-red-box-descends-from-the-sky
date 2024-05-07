# upload PNG-play

import pygame
import random
import time

# 게임 초기화 및 설정
pygame.init()
width, height = 1000, 600
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Dodge a Box")

# 색상 설정
black = (0, 0, 0)
white = (255, 255, 255)

# 폰트 설정
pygame.font.init()
font = pygame.font.SysFont("comicsans", 40)

# 플레이어 설정
player_size = 50
player_speed = 40
player_pos = [width / 2, height - 2 * player_size]

# 이미지 로드 및 크기 조정
images = []
for image_name in ['A.png', 'B.png', 'C.png', 'D.png']:
    img = pygame.image.load(image_name)
    img = pygame.transform.scale(img, (50, 50))  # 이미지 크기를 50x50으로 조정
    images.append(img)

# 떨어지는 물체 설정
enemy_size = 50
enemy_speed = 40
enemies = []

# 게임 변수
score = 0
game_started = False
game_over = False
start_time = None

# 시계 설정
clock = pygame.time.Clock()

def add_enemy():
    enemy_img = random.choice(images)
    pos = [random.randint(0, width - enemy_size), 0]  # 모든 물체가 위에서 떨어짐
    direction = [0, enemy_speed]
    enemies.append({'pos': pos, 'direction': direction, 'image': enemy_img})

def initialize_game():
    global player_pos, enemies, score, start_time, game_started, game_over
    player_pos = [width / 2, height - 2 * player_size]
    enemies = []
    score = 0
    start_time = time.time()
    game_started = True
    game_over = False

# 게임 루프
run = True
initialize_game()
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if game_over:
        if keys[pygame.K_SPACE]:
            initialize_game()

    if not game_started:
        if keys[pygame.K_SPACE]:
            game_started = True
            start_time = time.time()

    if game_started and not game_over:
        if keys[pygame.K_LEFT] and player_pos[0] > player_speed:
            player_pos[0] -= player_speed
        if keys[pygame.K_RIGHT] and player_pos[0] < width - player_size:
            player_pos[0] += player_speed
        if keys[pygame.K_UP] and player_pos[1] > player_speed:
            player_pos[1] -= player_speed
        if keys[pygame.K_DOWN] and player_pos[1] < height - player_size:
            player_pos[1] += player_speed

        # 새로운 물체 추가
        if time.time() - start_time > 1:  # 1초마다 새로운 물체 추가
            add_enemy()
            start_time = time.time()

        win.fill(black)  # 화면을 먼저 지웁니다.

        # 물체 업데이트 및 그리기
        for enemy in list(enemies):  # 리스트를 복사하여 반복 중 수정을 허용
            enemy['pos'][1] += enemy['direction'][1]
            win.blit(enemy['image'], enemy['pos'])

            # 화면 밖으로 나가면 리셋
            if enemy['pos'][1] > height:
                enemies.remove(enemy)
                score += 1

            # 충돌 검사
            enemy_rect = pygame.Rect(enemy['pos'][0], enemy['pos'][1], enemy_size, enemy_size)
            player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size, player_size)
            if player_rect.colliderect(enemy_rect):
                game_over = True

        # 플레이어 그리기
        pygame.draw.rect(win, white, player_rect)

        # 점수 표시
        score_text = font.render(f"Score: {score}", True, white)
        win.blit(score_text, (10, 10))

    pygame.display.update()
    clock.tick(30)

pygame.quit()
