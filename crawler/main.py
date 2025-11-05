import random
import sys

# ----- CONFIG -----
WIDTH, HEIGHT = 5, 5
ENCOUNTER_CHANCE = 0.35  # 35% per step
START_HP = 20

ENEMIES = [
    {"name": "Rat", "hp": (4, 7), "dmg": (1, 3)},
    {"name": "Ghoul", "hp": (6,10), "dmg": (2, 4)},
    {"name": "Vampire Thrall", "hp": (8,12), "dmg": (2, 5)},
    {"name": "Skeleton", "hp": (2,3), "dmg": (1, 2)},
    {"name": "Big Troll", "hp": (12,18), "dmg": (3, 7)},
    {"name": "Dragon", "hp": (15, 20), "dmg": (4, 8)},
]

# ----- GAME STATE -----
player = {"hp": START_HP, "dmg": (2, 5), "pos": [0, 0]}  # (x, y)
exit_pos = [WIDTH - 1, HEIGHT - 1]

# simple fog-of-war map ('.' unknown, 'S' start, 'E' exit, ' ' seen)
fog = [["." for _ in range(WIDTH)] for _ in range(HEIGHT)]
fog[player["pos"][1]][player["pos"][0]] = "S"
fog[exit_pos[1]][exit_pos[0]] = "E"

# ----- UTILS -----
def clamp(v, lo, hi): return max(lo, min(hi, v))

def draw_map():
    lines = []
    for y in range(HEIGHT):
        row = []
        for x in range(WIDTH):
            if [x, y] == player["pos"]:
                row.append("@")
            else:
                row.append(fog[y][x])
        lines.append(" ".join(row))
    print("\n".join(lines))

def roll_damage(dmg_range):
    return random.randint(dmg_range[0], dmg_range[1])

def spawn_enemy():
    roll = random.random()
    if roll < 0.5:
        enemy_template = ENEMIES[0]  # Rat
    elif roll < 0.75:
        enemy_template = ENEMIES[1]  # Ghoul
    elif roll < 0.9:
        enemy_template = ENEMIES[2]  # Vampire Thrall
    elif roll < 0.97:
        enemy_template = ENEMIES[3]  # Skeleton
    elif roll < 0.995:
        enemy_template = ENEMIES[4]  # Big Troll
    else:
        enemy_template = ENEMIES[5]  # Dragon   
    # instantiate with randomized HP
    enemy = {
        "name": enemy_template["name"],
        "hp": random.randint(*enemy_template["hp"]),
        "dmg": enemy_template["dmg"],
    }
    return enemy

# ----- COMBAT -----
def combat(enemy):
    print(f"\n!!! A {enemy['name']} appears (HP {enemy['hp']}) !!!")
    while enemy["hp"] > 0 and player["hp"] > 0:
        cmd = input("[A]ttack  [H]eal(+1-3)  [R]un: ").strip().lower()
        if cmd.startswith("a"):
            dmg = roll_damage(player["dmg"])
            enemy["hp"] -= dmg
            print(f"You hit {enemy['name']} for {dmg}. ({max(enemy['hp'],0)} HP left)")
        elif cmd.startswith("h"):
            heal = random.randint(1, 3)
            player["hp"] += heal
            print(f"You patch yourself for +{heal}. (You: {player['hp']} HP)")
        elif cmd.startswith("r") and random.random() < 0.5:
            print("You slip away into the shadows…")
            return True  # escaped
        else:
            print("You hesitate…")

        if enemy["hp"] > 0:
            edmg = roll_damage(enemy["dmg"])
            player["hp"] -= edmg
            print(f"{enemy['name']} strikes for {edmg}! (You: {player['hp']} HP)")

    if player["hp"] <= 0:
        print("You collapse. The dungeon claims another soul…")
        sys.exit(0)
    else:
        print(f"You defeated the {enemy['name']}!")
        # tiny reward
        if random.random() < 0.4:
            player["hp"] += 1
            print("You find a crusty bandage (+1 HP).")
            print(f"(You have survived encounters {len(ENEMIES)} times so far.)")
        return False

# ----- MAIN LOOP -----
def step(dx, dy):
    x, y = player["pos"]
    nx = clamp(x + dx, 0, WIDTH - 1)
    ny = clamp(y + dy, 0, HEIGHT - 1)
    if [nx, ny] == [x, y]:
        print("A wall blocks your way.")
        return
    player["pos"] = [nx, ny]
    # reveal fog
    if fog[ny][nx] == ".":
        fog[ny][nx] = " "
    print(f"You move to ({nx},{ny}).")
    # encounter?
    if random.random() < ENCOUNTER_CHANCE and [nx, ny] != exit_pos:
        enemy = spawn_enemy()
        combat(enemy)

def main():
    print("=== MINI DUNGEON ===")
    print("Goal: reach the exit 'E' without dying. You are '@'.")
    print("Commands: n/s/e/w, map, stats, quit")
    while True:
        if player["pos"] == exit_pos:
            print("\nYou touch the cold iron door. It creaks open—FREEDOM!")
            print("GG. Thanks for playing.")
            break

        cmd = input("\n> ").strip().lower()
        if cmd in ("n","s","e","w"):
            dx, dy = {"n":(0,-1),"s":(0,1),"e":(1,0),"w":(-1,0)}[cmd]
            step(dx, dy)
        elif cmd == "map":
            draw_map()
        elif cmd == "stats":
            print(f"HP: {player['hp']}  DMG: {player['dmg'][0]}-{player['dmg'][1]}  Pos: {tuple(player['pos'])}")
        elif cmd in ("q","quit","exit"):
            print("You abandon the quest…")
            break
        else:
            print("Try: n/s/e/w, map, stats, quit")

if __name__ == "__main__":
    main()