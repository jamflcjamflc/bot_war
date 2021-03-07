   

        

                
    # colision checks
    # computing lucas target
    lucas_target = v_add(lucas.pos, v_divide(lucas.size, 2))
    # colision  beween robots and shots
    kill_all = False
    for i in range(len(robots)):
        robot_target = v_add(robots[i].pos, v_divide(robots[i].size, 2))
        for j in range(len(shots)):
            if v_module(v_substract(robot_target, shots[j].pos)) < robots[i].size[0] * 0.5:
                if robots[i].r_type == 'coward':
                    kill_all = True
                else:
                    robots[i].active = False
                    score += robots[i].score
                    robots_killed += 1
                    break
    if kill_all:
        for i in range(len(robots)):
            robots[i].active = False
            score += robots[i].score
            robots_killed += 1          
    for i in range(len(robots)):
        if not robots[i].active:
            bomb_sound.play(fade_ms = 500)
            explosion.append([derbis(v_add(robots[i].pos, v_divide(robots[i].size, 2))) for j in range(20)])
    if kill_all:
        new_robot_pos = (rnd.randint(0, max_limit[0] -50), rnd.randint(0, max_limit[1] - 50))
        while v_module(v_substract(lucas_target, new_robot_pos)) <= screen_width / 2:
            new_robot_pos = (rnd.randint(0, max_limit[0] -50), rnd.randint(0, max_limit[1] - 50))
        rnd_number = rnd.random()
        if rnd_number < coward_freq:
            robots.append(robot(new_robot_pos, 'coward'))
        elif rnd_number < smart_freq:
            robots.append(robot(new_robot_pos, 'smart'))
        else:
            robots.append(robot(new_robot_pos, 'dumb'))
        game_t = 0
    else:    
        for i in range(len(robots)):
            if not robots[i].active:    
                new_robot_pos = (rnd.randint(0, max_limit[0] -50), rnd.randint(0, max_limit[1] - 50))
                while v_module(v_substract(lucas_target, new_robot_pos)) <= screen_width / 2:
                    new_robot_pos = (rnd.randint(0, max_limit[0] -50), rnd.randint(0, max_limit[1] - 50))
                rnd_number = rnd.random()
                if rnd_number < coward_freq:
                    robots.append(robot(new_robot_pos, 'coward'))
                elif rnd_number < smart_freq:
                    robots.append(robot(new_robot_pos, 'smart'))
                else:
                    robots.append(robot(new_robot_pos, 'dumb'))
                game_t = 0

    
    # colisions between gun and lucas
    for i in range(len(guns)):
        gun_target = v_add(guns[i].pos, v_divide(guns[i].size, 2))
        if v_module(v_substract(lucas_target, gun_target)) <= lucas.size[0]:
            pick_coffin.play()
            current_gun = guns[i].tipo
            score += guns[i].score
            guns[i].active = False
    
    # colisiona bewteen robots and lucas
    for i in range(len(robots)):
        robot_target = v_add(robots[i].pos, v_divide(robots[i].size, 2)) 
        if v_module(v_substract(lucas_target, robot_target)) <= (robots[i].size[0] + lucas.size[0]) * 0.4:
            print lucas_target
            print robot_target
            print v_module(v_substract(lucas_target, robot_target))
            print robots[i].size[0]
            print lucas.size[0]
            
            lucas.active = False
            background_sound.stop()
            lose_sound.play()
    if not lucas.active:
        time.sleep(5)
        highest_scores.append(score)
        highest_scores.sort(reverse = True)
        highest_scores = highest_scores[:3]
        if menu('you have been killed',['your score is ' + str(score),'highest scores:', str(highest_scores[0]), str(highest_scores[1]), str(highest_scores[2]), ''],['Quit', 'Play again'], music = menu_sound) == 0:
            game_exit = True
        else:
            robots_killed = 0
            robots_per_level = 12
            bonus_t = 1500
            gun_time = rnd.randint(0, 1000)
            score = 0
            level = 1
            game_t = 0
            level_t = 0
            current_gun = 0
            old_speed = 0
            default_speed = 5
            explosion = []
            shots = []
            robots = []
            guns = []
            announcements = []
            robots.append(robot((10, 10), 'dumb'))
            lucas = player((screen_width / 2, screen_height / 2))
            smart_freq = 0.0
            coward_freq = 0.0
            new_robot_time = 240 - (200 * level / float(5 * level))
            background_sound.play(loops = -1)
        f = open('DATA\highest_scores.pic', 'wb')
        pic.dump(highest_scores, f)
        print highest_scores
        print 'dumped to file'
        
        f.close()

    # cleanup
    robots = [robots[i] for i in range(len(robots)) if robots[i].active] #cleans robots
    guns = [guns[i] for i in range(len(guns)) if guns[i].active] # clean guns
    explosion = [explosion[i] for i in range(len(explosion)) if len(explosion[i]) >0] # clean explossions
    shots = [shots[i] for i in range(len(shots)) if shots[i].active]  # clean shots
    announcements = [announcements[i] for i in range(len(announcements)) if announcements[i].active]  # clean announcements
    
    #level check
    game_t += 1
    level_t += 1
    if robots_killed >= level * robots_per_level:
        bonus = max(0, level * (bonus_t - level_t))
        score += bonus
        level += 1
        announcements.append(announcement(['CONGRATULATIONS! ', 'You have reached level ' + str(level), 'bonus: ' + str(bonus)], 100))
        gun_time = rnd.randint(100, 1000)
        new_robot_time = 240.0 - (200.0 * level / (5.0 * float(level)))
        smart_freq = 5.0 * level / 100.0
        
        if level <4:
            coward_freq = 0.0
        else:
            coward_freq = level / 100.0
        game_t = 0
        level_t = 0
        current_gun = 0
        old_speed = 0
        lucas.speed = 0
        guns = []
        if len(robots) > 1:
            robots = [robots[i] for i in range(1)]
    if level_t == gun_time:
        new_gun_pos = (rnd.randint(0, max_limit[0] -100), rnd.randint(0, max_limit[1] - 100))
        while v_module(v_substract(lucas_target, new_gun_pos)) <= screen_width / 2:
            new_gun_pos = (rnd.randint(0, max_limit[0] -100), rnd.randint(0, max_limit[1] - 100))
        random_number = rnd.randint(1, 4)
        guns.append(gun(new_gun_pos, random_number))
    if game_t > new_robot_time:
        new_robot_pos = (rnd.randint(0, max_limit[0] -50), rnd.randint(0, max_limit[1] - 50))
        while v_module(v_substract(lucas_target, new_robot_pos)) <= screen_width / 2:
            new_robot_pos = (rnd.randint(0, max_limit[0] -50), rnd.randint(0, max_limit[1] - 50))
        rnd_number = rnd.random()
        if rnd_number < coward_freq:
            robots.append(robot(new_robot_pos, 'coward'))
        elif rnd_number < smart_freq:
            robots.append(robot(new_robot_pos, 'smart'))
        else:
            robots.append(robot(new_robot_pos, 'dumb'))
        game_t = 0
        
    # draw the different elements on the screen
    screen.fill(terrain)
    draw_grid()
    
    for i in range(len(explosion)):
        for j in range(len(explosion[i])):
            explosion[i][j].update_pos()
        explosion[i] = [explosion[i][j] for j in range(len(explosion[i])) if explosion[i][j].active]
    
    for i in range(len(shots)):
        shots[i].update_pos()
      
    for i in range(len(robots)):
        robots[i].move(lucas.pos)
        robots[i].draw()
    for i in range(len(guns)):
        guns[i].update()
        guns[i].draw()           
    lucas.move()
    lucas.draw()
    for i in range(len(announcements)):
        announcements[i].update()
