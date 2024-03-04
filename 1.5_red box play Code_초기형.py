import pygame
import random
import time

# 게임 초기화
pygame.init()
width, height = 500, 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Dodge the Falling Objects")

# 색상
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

# 플레이어 설정
player_size = 50
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

# 게임 루프
run = True
while run:
    if game_started:
        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # 키 입력 처리
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_pos[0] > player_speed:
            player_pos[0] -= player_speed
        if keys[pygame.K_RIGHT] and player_pos[0] < width - player_size:
            player_pos[0] += player_speed

        # 물체가 떨어짐
        if enemy_pos[1] >= 0 and enemy_pos[1] < height:
            enemy_pos[1] += enemy_speed
        else:
            enemy_pos[0] = random.randint(0, width - enemy_size)
            enemy_pos[1] = 0
            score += 1

        # 충돌 감지
        if player_pos[0] < enemy_pos[0] < player_pos[0] + player_size or player_pos[0] < enemy_pos[0] + enemy_size < player_pos[0] + player_size:
            if player_pos[1] < enemy_pos[1] < player_pos[1] + player_size or player_pos[1] < enemy_pos[1] + enemy_size < player_pos[1] + player_size:
                run = False

        # 화면 업데이트
        win.fill(black)
        pygame.draw.rect(win, white, (player_pos[0], player_pos[1], player_size, player_size))
        pygame.draw.rect(win, red, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))
        pygame.display.update()

        clock.tick(30)
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_started = True
                    start_time = time.time()

# 게임 종료 후 점수 표시
end_time = time.time()
print("Survival Time: {:.2f} seconds".format(end_time - start_time))
pygame.quit()
