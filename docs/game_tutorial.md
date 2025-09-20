# 📂 `docs/game_tutorial.md`

````markdown
# 🎮 NeoPaquet Game Tutorial
*A beginner’s guide to making a simple 2D game with NeoPaquet.*

This tutorial extends [Graphics Tutorial](graphics_tutorial.md) and adds:
- Player movement with arrow keys  
- Collision detection  
- A score counter  

---

## 1. Setup

Import required libraries:

```neopaquet
import "stdlib/core.np"
import "stdlib/graphics.np"
import "stdlib/io.np"
import "stdlib/math.np"
````

We’ll create:

* A **player square** controlled by arrow keys
* A **coin** that moves randomly when collected
* A **score counter**

---

## 2. Player + Coin State

```neopaquet
playerX = 0.0
playerY = 0.0
playerSize = 0.1

coinX = 0.5
coinY = 0.0
coinSize = 0.05

score = 0
```

---

## 3. Input Handling

We use GLFW key input through externs:

```neopaquet
@func ("handle_input") [window] go {
    if extern ("glfwGetKey") [window, 265] == 1 { playerY = playerY + 0.05 } -- up
    if extern ("glfwGetKey") [window, 264] == 1 { playerY = playerY - 0.05 } -- down
    if extern ("glfwGetKey") [window, 263] == 1 { playerX = playerX - 0.05 } -- left
    if extern ("glfwGetKey") [window, 262] == 1 { playerX = playerX + 0.05 } -- right
}
```

---

## 4. Collision Detection

```neopaquet
@func ("check_collision") [] go {
    dx = abs(playerX - coinX)
    dy = abs(playerY - coinY)
    if dx < (playerSize + coinSize) and dy < (playerSize + coinSize) {
        return 1
    }
    return 0
}
```

---

## 5. Game Drawing

```neopaquet
@func ("draw") [] go {
    -- clear background
    gfx_set_color(0.1, 0.1, 0.1, 1.0)
    gfx_draw_rect(-1.0, -1.0, 2.0, 2.0)

    -- draw player (blue square)
    gfx_set_color(0.2, 0.6, 1.0, 1.0)
    gfx_draw_rect(playerX, playerY, playerSize, playerSize)

    -- draw coin (yellow square)
    gfx_set_color(1.0, 1.0, 0.0, 1.0)
    gfx_draw_rect(coinX, coinY, coinSize, coinSize)

    -- draw score (print to stdout for now)
    println("Score: ", score)
}
```

---

## 6. Game Loop

```neopaquet
src () "stdout" {
    window = gfx_init(800, 600, "NeoPaquet Game")
    gfx_run(window, update)
} run

@func ("update") [] go {
    handle_input(window)

    if check_collision() == 1 {
        score = score + 1
        -- respawn coin randomly
        coinX = randf(-0.9, 0.9)
        coinY = randf(-0.9, 0.9)
    }

    draw()
}
```

---

## 7. Run It

```bash
$ npaquetc game.np -o game.exe
$ ./game.exe
```

➡️ A window opens.

* Move the **blue player square** with arrow keys.
* Collect the **yellow coin** to increase score.
* Coin respawns at random positions.

---

## ✅ Next Steps

* Add walls + collision so the player can’t leave screen bounds.
* Display score **on-screen** with text rendering (instead of stdout).
* Add enemies (red squares) that reduce score or end the game.
* Extend to 3D using `linear_algebra.np` projection matrices.

---

```

---

## ✅ What This Adds
- A **step-by-step game tutorial**.  
- Teaches **input, state, collisions, score, respawn mechanics**.  
- Produces a **working 2D coin-collect game** in NeoPaquet.  

---

⚡
