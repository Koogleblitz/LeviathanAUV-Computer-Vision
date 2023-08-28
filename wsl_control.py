import pygame
pygame.init()

#----------------Joystick&KB_init-----------------------\
js_connected= False
pygame.joystick.init()
if pygame.joystick.get_count() == 0:
    print("No joystick connected.")
    # quit()
else:
    is_connected= True
    print("Connected. Writing to joystick_data.txt")
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

# js_file = "joystick_data.txt"
relay_Path = r"\\wsl.localhost\Ubuntu-18.04\home\koogleblitz\LeviathanAUV\catkin_ws\src\WSL_comm\src\relay_data.txt"
#----------------------------------------------------/

#----------------GUI_init----------------------------\
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("WSL --> ROS")
font = pygame.font.Font(None, 36)
text = ""
#----------------------------------------------------/

while True:
    text= ''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

        #----------------Keyboard_cap-----------------------\
        # elif event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_RETURN:
        #         with open("keyboard_data.txt", "a") as f:
        #             f.write(text + "\n")
        #         text = ""
        #     elif event.key == pygame.K_BACKSPACE:
        #         text = text[:-1]
        #     else:
        #         text += event.unicode



        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            text= '  <<[A] '
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            text= '    [D]>> '
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            text= '     ^\n     ^\n    [W]        '
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            text= '    [S]\n     v\n     v        '
        else: text = text[:-1]

        if event.type == pygame.KEYDOWN and text!= '':
            if keys[pygame.K_LEFT]:
                text= ("    ←")
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                text= ("    →")
            elif keys[pygame.K_UP] or keys[pygame.K_w]:
                text= ("    ↑")
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                text= ("    ↓")
            else: text += event.unicode
            # screen.fill((0,0, 0))
            # text_surface = font.render(text, True, (200, 200, 200))
            # screen.blit(text_surface, (50, 50))
            
        #--------------------------------------------------/

    #----------------------------------------------------\----------------Joystick_cap----------------------\----------------------------------------------------\\
    if(js_connected):
        left_x_axis = '%.3f'%(joystick.get_axis(0))
        left_y_axis = '%.3f'%(joystick.get_axis(1))
        right_x_axis = '%.3f'%(joystick.get_axis(2))
        right_y_axis = '%.3f'%(joystick.get_axis(3))
        left_trigger = '%.3f'%(joystick.get_axis(4))
        right_trigger = '%.3f'%(joystick.get_axis(5))
        a_button = joystick.get_button(0)
        b_button = joystick.get_button(1)
        x_button = joystick.get_button(2)
        y_button = joystick.get_button(3)
        left_bumper_button = joystick.get_button(4)
        right_bumper_button = joystick.get_button(5)
        hat_x = joystick.get_hat(0)[0]
        hat_y = joystick.get_hat(0)[1]
        # with open(js_file, "w") as f:
        #     f.write(f"{left_x_axis} {left_y_axis} {right_x_axis} {right_y_axis} {left_trigger} {right_trigger} {a_button} {b_button} {x_button} {y_button} {left_bumper_button} {right_bumper_button} {hat_x} {hat_y}\n")
        
        
        if(float(left_x_axis)<0.000): text= ("    ←")
    #----------------------------------------------------/----------------------------------------------------/----------------------------------------------------//

    if text!= '':
    #     print(text)
    #     screen.fill((0,0, 0))
    #     text_surface = font.render(text, True, (200, 200, 200))
    #     screen.blit(text_surface, (50, 50))
        print(text)
        with open(relay_Path, "w") as f:
                f.write(text)
        with open(relay_Path, 'r') as f:  
            line = f.readline().strip()
            line1 = f.readline().strip()
            line2 = f.readline().strip()
            values = line.split()
            text= line+line1+line2
        textRender = font.render(text, True, (255, 255, 255))
        text_rect = textRender.get_rect()
        text_rect.center = screen.get_rect().center
        screen.blit(textRender, text_rect)
    else: screen.fill((0, 0, 0))
    pygame.display.update()
    pygame.time.wait(100)