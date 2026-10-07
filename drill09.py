from pico2d import *


TUK_WIDTH, TUK_HEIGHT = 1024, 768
FRAME_SIZE = 100
FRAME_COUNT = 8
SPEED = 5
# 머리와 발이 화면 밖으로 나가지 않도록 위아래 경계에 여유를 더 준다
MARGIN_X = FRAME_SIZE // 2
MARGIN_Y = FRAME_SIZE // 2 + 20

# animation_sheet.png 각 행의 y 좌표 (pico2d는 아래쪽이 0)
IDLE_RIGHT, IDLE_LEFT, RUN_RIGHT, RUN_LEFT = 300, 200, 100, 0

open_canvas(TUK_WIDTH, TUK_HEIGHT)
tuk_ground = load_image('TUK_GROUND.png')
character = load_image('animation_sheet.png')


def handle_events():
    global running, dir_x, dir_y, face

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False
            elif event.key == SDLK_RIGHT:
                dir_x += 1
            elif event.key == SDLK_LEFT:
                dir_x -= 1
            elif event.key == SDLK_UP:
                dir_y += 1
            elif event.key == SDLK_DOWN:
                dir_y -= 1
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                dir_x -= 1
            elif event.key == SDLK_LEFT:
                dir_x += 1
            elif event.key == SDLK_UP:
                dir_y -= 1
            elif event.key == SDLK_DOWN:
                dir_y += 1

    # 좌우로 움직일 때만 바라보는 방향을 바꾸고, 상하 이동은 기존 방향을 유지한다
    if dir_x > 0:
        face = 1
    elif dir_x < 0:
        face = -1


def get_sprite_row():
    # 멈춰 있으면 idle, 움직이면 달리기. 좌우는 바라보는 방향으로 고른다
    if dir_x == 0 and dir_y == 0:
        return IDLE_RIGHT if face == 1 else IDLE_LEFT
    return RUN_RIGHT if face == 1 else RUN_LEFT


running = True
x, y = TUK_WIDTH // 2, TUK_HEIGHT // 2
frame = 0
dir_x, dir_y = 0, 0
face = 1

while running:
    clear_canvas()
    tuk_ground.draw(TUK_WIDTH // 2, TUK_HEIGHT // 2, TUK_WIDTH, TUK_HEIGHT)
    character.clip_draw(frame * FRAME_SIZE, get_sprite_row(), FRAME_SIZE, FRAME_SIZE, x, y)
    update_canvas()
    handle_events()
    if not running:
        break

    x = clamp(MARGIN_X, x + dir_x * SPEED, TUK_WIDTH - MARGIN_X)
    y = clamp(MARGIN_Y, y + dir_y * SPEED, TUK_HEIGHT - MARGIN_Y)
    frame = (frame + 1) % FRAME_COUNT
    delay(0.05)

close_canvas()
