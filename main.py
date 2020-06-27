import pgzrun
from random import randint as rnd
from time import sleep

WIDTH = 1280
HEIGHT = 720

x = 10
y = 10

hero = Actor("hero", (x, y))
bullet = Actor("bullet3", (hero.pos))

mouse_pos = (x, y)
pers_v = 2
v = 2

hero_dirx = v
hero_diry = v

slot1 = [Actor("knife", (1175, 640)), "weapon_knife", "-", "-"]
slot2 = ""
slot3 = [Actor("weapon_ak-47", (1175, 640)), "weapon_ak-47", 30 , 90]
slots = [slot1, slot2, slot3]

active_slot = slot1
active_slot_draw = Actor("active_slot", (active_slot[0].pos[0] - 100, active_slot[0].pos[1]))

mouse_pos = (WIDTH // 2, HEIGHT // 2)

weapon_damage = 0
weapon_ammo = 0
weapon_ammo_all = 0
weapon_fast = 1
weapon_v = 1

def game_start():
	global enemies, walls, slots, weapons, bullet
	weapons = (open("data/weapons.txt").read()).split("\n")
	for i in range(len(weapons)):
		weapons[i] = weapons[i].split(" ")
		print(weapons)
	# Hero
	hero = Actor("hero", (x, y))

	# Enemies
	enemies = [Actor("enemy", (640, 360)), 100]


	# Walls
	walls = [Actor("block", (100, 100))]

game_start()

def update():
	global x, y, pers_v, vx, vy, enemies, hero, walls, bullet, active_slot, bullet_animate, weapon_damage, weapon_name, weapon_ammo, weapon_ammo_all, weapon_fast, weapon_v
	# Hero
	hero_dirx = 0
	hero_diry = 0
	v = pers_v * weapon_v
	if keyboard.a:
		x -= v
		hero_dirx = v
		sounds.footsteps.play()
		
	if keyboard.d:
		x += v
		hero_dirx = -v
		sounds.footsteps.play()
		
	if keyboard.w:
		y -= v
		hero_diry = v
		sounds.footsteps.play()
		
	if keyboard.s:
		y += v
		hero_diry = -v
		sounds.footsteps.play()

	if keyboard.r:
		try:
			active_slot[3] = active_slot[3] - (weapon_ammo - active_slot[2])
			active_slot[2] = weapon_ammo
		except TypeError:
			pass

	if keyboard.k_1:
		if slot1 != "":
			active_slot = slot1
	if keyboard.k_2:
		if slot2 != "":
			active_slot = slot2
	if keyboard.k_3:
		if slot3 != "":
			active_slot = slot3
	for w in weapons:
		if w[0] == active_slot[1]:
			weapon_name = w[0]
			weapon_damage = int(w[1])
			weapon_fast = int(w[3])
			weapon_v = float(w[4])
			try:
				weapon_ammo = int(w[2])
			except ValueError:
				weapon_ammo = "-"

	for z in walls:
		if hero.colliderect(z):
			if hero.pos[0] > z.pos[0] + 25:
				x += v
			elif hero.pos[0] < z.pos[0] - 25:
				x += -v
			elif hero.pos[1] > z.pos[1] + 25:
				y += v
			elif hero.pos[1] < z.pos[1] - 25:
				y += -v

	hero.pos = (x, y)

	# Bullet
	try:
		for i in range(len(walls)):
			if bullet.colliderect(walls[i]):
				bullet_animate.stop(complete = True)
				fire()
		for q in range(0, len(enemies), 2):
			if bullet.colliderect(enemies[q]):
				print(weapon_damage)
				enemies[q+1] -= weapon_damage
				bullet_animate.stop(complete = True)
				fire()
				print(enemies[q+1])
	except ValueError:
		pass

	# Enemies
	for i in range (1, len(enemies), 2):
		if enemies[i] <= 0:
			enemies[i-1].pos = (rnd(0, 1280), rnd(0, 720))
			enemies[i] = 100



def draw():
	global enemies, walls, slots, bullet, mouse_pos, weapon_ammo, weapon_ammo_all
	screen.clear()

	# Map
	screen.fill((145, 130, 89))

	# Hero
	hero.draw()

	# Walls
	for z in walls:
		z.draw()

	# Enemyes
	for i in range(0, len(enemies), 2):
		enemies[i].draw()

	# Items
	now_pos_x = slots[0][0].pos[0]
	now_pos_y = slots[0][0].pos[1]

	screen.draw.text("1", topright=(1275, now_pos_y - 25))
	slots[0][0].draw()

	for q in range(1, len(slots)):
		if slots[q] != "":
			now_pos_y = now_pos_y - 55
			slots[q][0].pos = (now_pos_x, now_pos_y)
			screen.draw.text(str(q+1), topright=(1275, now_pos_y - 25))
			slots[q][0].draw()
	screen.draw.line((1280, 670), (1000, 670), (255, 255, 255))
	active_slot_draw.pos = (active_slot[0].pos[0] - 35, active_slot[0].pos[1])
	active_slot_draw.draw()

	# Bullet
	screen.draw.line(mouse_pos, hero.pos, (0, 255, 0))
	bullet.draw()

	# Ammo
	screen.draw.text(str(active_slot[2])+"/"+str(active_slot[3]), bottomright = (1250, 720), fontsize = 70)

def on_mouse_move(pos):
	global hero, mouse_pos
	mouse_pos = pos
	hero.angle = hero.angle_to(pos)

def fire():
	global hero, bullet
	bullet.pos = hero.pos

def on_mouse_down(pos):
	global weapons, active_slot, bullet, bullet_animate, weapon_name, weapon_fast, weapon_ammo
	hero.angle = hero.angle_to(pos)
	if active_slot[2] != 0:
		sounds.footsteps.stop()
		sounds.weapon_fire_3.play()
		bullet = Actor("bullet3", (hero.pos))
		bullet_animate = animate(bullet, pos=pos, on_finished = fire(), duration=bullet.distance_to(pos) / weapon_fast)
		print(bullet.distance_to(pos))
		try:
			active_slot[2] -= 1
		except TypeError:
			pass

pgzrun.go()