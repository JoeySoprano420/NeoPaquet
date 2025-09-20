# 📂 `docs/advanced_game_tutorial.md`

````markdown
# 🕹️ NeoPaquet Advanced Game Tutorial
*A step beyond: building a small arcade game in NeoPaquet.*

This tutorial expands the [basic game tutorial](game_tutorial.md) with:
- Enemies that chase the player  
- Health system (game over if 0)  
- Multiple levels (each harder than the last)  
- UI overlay for score and health  

---

## 1. Setup

We’ll need the same imports:

```neopaquet
import "stdlib/core.np"
import "stdlib/graphics.np"
import "stdlib/io.np"
import "stdlib/math.np"
````

---

## 2. Game State

```neopaquet
playerX = 0.0
playerY = 0.0
playerSize = 0.08
playerHealth = 3

coinX = 0.5
coinY = 0.0
coinSize = 0.05

score = 0
level = 1

-- enemies: array of [x, y]
enemies = [[-0.5, 0.5], [0.5, -0.5]]
enemySpeed = 0.01
```

---

## 3. Input

```neopaquet
@func ("handle_input") [window] go {
    if extern ("glfwGetKey") [window, 265] == 1 { playerY = playerY + 0.05 }
    if extern ("glfwGetKey") [window, 264] == 1 { playerY = playerY - 0.05 }
    if extern ("glfwGetKey") [window, 263] == 1 { playerX = playerX - 0.05 }
    if extern ("glfwGetKey") [window, 262] == 1 { playerX = playerX + 0.05 }
}
```

---

## 4. Enemy Movement

Enemies move toward the player:

```neopaquet
@func ("update_enemies") [] go {
    for e in enemies {
        dx = playerX - e[0]
        dy = playerY - e[1]
        mag = sqrt(dx*dx + dy*dy)
        if mag > 0 {
            e[0] = e[0] + (dx/mag) * enemySpeed
            e[1] = e[1] + (dy/mag) * enemySpeed
        }
    }
}
```

---

## 5. Collisions

```neopaquet
@func ("check_coin_collision") [] go {
    dx = abs(playerX - coinX)
    dy = abs(playerY - coinY)
    if dx < (playerSize + coinSize) and dy < (playerSize + coinSize) {
        return 1
    }
    return 0
}

@func ("check_enemy_collisions") [] go {
    for e in enemies {
        dx = abs(playerX - e[0])
        dy = abs(playerY - e[1])
        if dx < (playerSize + 0.08) and dy < (playerSize + 0.08) {
            return 1
        }
    }
    return 0
}
```

---

## 6. Drawing

```neopaquet
@func ("draw") [] go {
    -- background
    gfx_set_color(0.0, 0.0, 0.0, 1.0)
    gfx_draw_rect(-1.0, -1.0, 2.0, 2.0)

    -- player (cyan)
    gfx_set_color(0.0, 1.0, 1.0, 1.0)
    gfx_draw_rect(playerX, playerY, playerSize, playerSize)

    -- coin (yellow)
    gfx_set_color(1.0, 1.0, 0.0, 1.0)
    gfx_draw_rect(coinX, coinY, coinSize, coinSize)

    -- enemies (red)
    gfx_set_color(1.0, 0.0, 0.0, 1.0)
    for e in enemies {
        gfx_draw_rect(e[0], e[1], 0.08, 0.08)
    }

    -- UI: health and score
    println("Score: ", score, "  Health: ", playerHealth, "  Level: ", level)
}
```

---

## 7. Game Logic

```neopaquet
@func ("update") [] go {
    handle_input(window)
    update_enemies()

    if check_coin_collision() == 1 {
        score = score + 1
        coinX = randf(-0.9, 0.9)
        coinY = randf(-0.9, 0.9)

        if score % 5 == 0 {
            level = level + 1
            enemySpeed = enemySpeed + 0.005
            enemies.append([randf(-0.9,0.9), randf(-0.9,0.9)])
        }
    }

    if check_enemy_collisions() == 1 {
        playerHealth = playerHealth - 1
        if playerHealth <= 0 {
            println("GAME OVER! Final Score: ", score)
            extern ("exit") [0]
        }
    }

    draw()
}
```

---

## 8. Main Loop

```neopaquet
src () "stdout" {
    window = gfx_init(800, 600, "NeoPaquet Arcade Game")
    gfx_run(window, update)
} run
```

---

## ✅ Gameplay Summary

* Move the **cyan player square** with arrow keys.
* Collect **yellow coins** to increase score.
* Every **5 coins** → new level, faster enemies, and one more enemy spawns.
* Avoid **red enemies** → each hit reduces health.
* Lose all health → **Game Over**.

---

## 🎯 Next Steps

* Replace squares with **sprites** (textures).
* Add **sound effects** on coin collect / hit.
* Display **UI overlays in-game** instead of stdout.
* Add **menu screens** (start, pause, game over).
* Expand to **3D arcade gameplay** with `linear_algebra.np`.

---

```

---

## ✅ What This Adds
- Full **arcade loop**: health, levels, difficulty progression.  
- Multiple enemies with **chasing AI**.  
- **Game over condition**.  
- Roadmap for **graphics, sound, and UI improvements**.  

---

⚡ 
