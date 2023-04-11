from tkinter import *
import random

is_running = False
lvl_slc = 0


def board_setup(map_type):
    global is_running, snake, apple, obstacles, was_changed
    for button in buttons:
        button.place_forget()
    if map_type == 0:
        obstacles = []
        snake = [[17, 17, 1, 1], [17, 18, 0, 1], [17, 19, 2, 1]]
    elif map_type == 1:
        obstacles = []
        for i in range(1,36):
             obstacles.append([i,1])
             obstacles.append([i, 35])
        for i in range(2,35):
             obstacles.append([1,i])
             obstacles.append([35, i])
        snake = [[17, 17, 1, 1], [17, 18, 0, 1], [17, 19, 2, 1]]
    elif map_type == 2:
        obstacles = []
        for i in range(1, 36):
            obstacles.append([i, 1])
            obstacles.append([i, 35])
        for i in range(2, 35):
            obstacles.append([1, i])
            obstacles.append([35, i])
        for i in range(3,34):
            if i!=17:
               obstacles.append([17,i])
        for i in range(3, 34):
            obstacles.append([i, 17])
        snake = [[2, 17, 1, 1], [2, 18, 0, 1], [2, 19, 2, 1]]
    is_running = 1
    was_changed = False
    apple = apple_find()
    field.delete("all")
    field_refresh()
    game_step()
    for i in range(36):
        field.create_line((i - 1) * 20, 0, (i - 1) * 20, 700, tags='field')
    for i in range(36):
        field.create_line(0, (i - 1) * 20, 700, (i - 1) * 20, tags='field')



def lose_screen():
    global is_running
    is_running = False
    field.delete('all')
    field.create_text(350, 350, font="Calibri",
                      text=f"You have scored {(len(snake) - 4)} points. Press Space to restart")
    level_selection()


def game_step():
    global snake, apple, is_running, was_changed
    was_changed = False
    if is_running:
        for element in snake:
            if element[2] == 1:
                head = element.copy()
                element[2] = 0
                if head[3] == 1:
                    head[1] -= 1
                elif head[3] == 0:
                    head[0] -= 1
                elif head[3] == 2:
                    head[0] += 1
                elif head[3] == 3:
                    head[1] += 1
            elif element[2] == 2:
                tail = element.copy()
                to_remove = element
                if tail[3] == 1:
                    tail[1] -= 1
                elif tail[3] == 0:
                    tail[0] -= 1
                elif tail[3] == 2:
                    tail[0] += 1
                elif tail[3] == 3:
                    tail[1] += 1
        snake.append(head)
        bitesitself = False
        iterator = snake.copy()
        iterator.remove(head)
        for segment in iterator:
            if head[:2] == segment[:2]:
                if segment[2] != 2:
                    bitesitself = True
                elif apple[:2] == head[:2]:
                    bitesitself = True
        run_into_wall = head[0] < 1 or head[0] > 35 or head[1] < 1 or head[1] > 35
        obstacle_hit = False
        for obstacle in obstacles:
            if obstacle == head[:2]:
                obstacle_hit = True

        if bitesitself or run_into_wall or obstacle_hit:
            lose_screen()
            return
        if not head[:2] == apple[:2]:
            snake.remove(to_remove)
            for candidate in snake:
                if candidate[0] == tail[0] and candidate[1] == tail[1]:
                    candidate[2] = 2
        else:
            if len(snake) == 1225:
                is_running = False
                field.delete('all')
                field.create_text(350, 350, font="Calibri",
                                  text=f"You have won. Press Space to restart")
            else:
                apple = apple_find()
        field_refresh()
        screen.after(450, lambda: [game_step()])



def apple_find():
    free_place = []
    for i in range(1, 1226):
        free_place.append(i)
    for element in snake:
        free_place.remove(element[0] + (element[1] - 1) * 35)
    for element in obstacles:
        free_place.remove(element[0] + (element[1] - 1) * 35)
    a = free_place[random.randint(0, len(free_place) - 1)]
    return [a % 35 + 1,a // 35 + 1]


def field_refresh():
    field.delete('game')
    for element in snake:
        if element[2] != 1:
            field.create_rectangle((element[0] - 1) * 20, (element[1] - 1) * 20, element[0] * 20, element[1] * 20,
                                   fill="#FF0000", tags='game')
        else:
            field.create_rectangle((element[0] - 1) * 20, (element[1] - 1) * 20, element[0] * 20, element[1] * 20,
                                   fill="#FF5050", tags='game')
    field.create_rectangle((apple[0] - 1) * 20, (apple[1] - 1) * 20, apple[0] * 20, apple[1] * 20,
                           fill="#008800", tags='game')
    for obstacle in obstacles:
        field.create_rectangle((obstacle[0] - 1) * 20, (obstacle[1] - 1) * 20, obstacle[0] * 20, obstacle[1] * 20,
                               fill="#000000", tags='field')



def Next_turn(event):
    global was_changed
    if not was_changed:
        for element in snake:
            if element[2] == 1 and event.keycode - 39 != element[3] and event.keycode - 35 != element[3]:
                element[3] = event.keycode - 37
    was_changed = True


def level_selection():
    global buttons
    lvl0 = Button(master=screen, text="lvl0", width=10, command=lambda :board_setup(0))
    lvl1 = Button(master=screen, text="lvl1", width=10, command=lambda :board_setup(1))
    lvl2 = Button(master=screen, text="lvl2", width=10, command=lambda :board_setup(2))
    buttons = [lvl0, lvl1, lvl2]
    for button in buttons:
        button.place(x=350,y=(buttons.index(button)+1)*50,anchor="center")


if __name__ == "__main__":
    screen = Tk()
    screen.resizable(False, False)
    screen.geometry("700x700")
    screen.title("Snake 1.0")
    screen.bind("<Up>", Next_turn)
    screen.bind("<Right>", Next_turn)
    screen.bind("<Down>", Next_turn)
    screen.bind("<Left>", Next_turn)
    field = Canvas(screen, height=700, width=700)
    field.place(x=0, y=0)
    level_selection()
    screen.mainloop()
