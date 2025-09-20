# 📂 `docs/3d_game_tutorial.md`

````markdown
# 🧊 NeoPaquet 3D Game Tutorial
*From 2D arcade to 3D cube worlds with NeoPaquet.*

This tutorial expands [Advanced Game Tutorial](advanced_game_tutorial.md) into **3D**:
- Camera with perspective projection  
- 3D cube rendering  
- Moving and rotating objects  
- Basic camera movement  

---

## 1. Setup

Import libraries:
```neopaquet
import "stdlib/core.np"
import "stdlib/graphics.np"
import "stdlib/linear_algebra.np"
import "stdlib/io.np"
````

We’ll use **matrices** from `linear_algebra.np` for camera + projection.

---

## 2. Game State

```neopaquet
cameraX = 0.0
cameraY = 0.0
cameraZ = 3.0

angle = 0.0
```

---

## 3. Perspective Projection

Set up perspective + look-at:

```neopaquet
@func ("setup_3d") [] go {
    proj = mat4_perspective(60, 800.0/600.0, 0.1, 100.0)
    view = mat4_lookat(cameraX, cameraY, cameraZ, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    gfx_load_matrix4(proj)
    gfx_mult_matrix4(view)
}
```

---

## 4. Drawing a Cube

```neopaquet
@func ("draw_cube") [x, y, z, size] go {
    half = size / 2

    extern ("glBegin") [0x0007]   -- GL_QUADS

    -- Front face
    gfx_set_color(1.0, 0.0, 0.0, 1.0)
    extern ("glVertex3f") [x-half, y-half, z+half]
    extern ("glVertex3f") [x+half, y-half, z+half]
    extern ("glVertex3f") [x+half, y+half, z+half]
    extern ("glVertex3f") [x-half, y+half, z+half]

    -- Back face
    gfx_set_color(0.0, 1.0, 0.0, 1.0)
    extern ("glVertex3f") [x-half, y-half, z-half]
    extern ("glVertex3f") [x+half, y-half, z-half]
    extern ("glVertex3f") [x+half, y+half, z-half]
    extern ("glVertex3f") [x-half, y+half, z-half]

    -- Left face
    gfx_set_color(0.0, 0.0, 1.0, 1.0)
    extern ("glVertex3f") [x-half, y-half, z-half]
    extern ("glVertex3f") [x-half, y-half, z+half]
    extern ("glVertex3f") [x-half, y+half, z+half]
    extern ("glVertex3f") [x-half, y+half, z-half]

    -- Right face
    gfx_set_color(1.0, 1.0, 0.0, 1.0)
    extern ("glVertex3f") [x+half, y-half, z-half]
    extern ("glVertex3f") [x+half, y-half, z+half]
    extern ("glVertex3f") [x+half, y+half, z+half]
    extern ("glVertex3f") [x+half, y+half, z-half]

    -- Top face
    gfx_set_color(0.0, 1.0, 1.0, 1.0)
    extern ("glVertex3f") [x-half, y+half, z-half]
    extern ("glVertex3f") [x-half, y+half, z+half]
    extern ("glVertex3f") [x+half, y+half, z+half]
    extern ("glVertex3f") [x+half, y+half, z-half]

    -- Bottom face
    gfx_set_color(1.0, 0.0, 1.0, 1.0)
    extern ("glVertex3f") [x-half, y-half, z-half]
    extern ("glVertex3f") [x-half, y-half, z+half]
    extern ("glVertex3f") [x+half, y-half, z+half]
    extern ("glVertex3f") [x+half, y-half, z-half]

    extern ("glEnd") []
}
```

---

## 5. Game Loop

```neopaquet
@func ("draw") [] go {
    setup_3d()

    gfx_rotate(angle, 1.0, 1.0, 0.0)
    draw_cube(0.0, 0.0, 0.0, 1.0)

    angle = angle + 1.0
}
```

---

## 6. Camera Movement

```neopaquet
@func ("handle_input") [window] go {
    if extern ("glfwGetKey") [window, 265] == 1 { cameraZ = cameraZ - 0.1 } -- forward
    if extern ("glfwGetKey") [window, 264] == 1 { cameraZ = cameraZ + 0.1 } -- backward
    if extern ("glfwGetKey") [window, 263] == 1 { cameraX = cameraX - 0.1 } -- left
    if extern ("glfwGetKey") [window, 262] == 1 { cameraX = cameraX + 0.1 } -- right
}
```

---

## 7. Main

```neopaquet
src () "stdout" {
    window = gfx_init(800, 600, "NeoPaquet 3D World")
    gfx_run(window, update)
} run

@func ("update") [] go {
    handle_input(window)
    draw()
}
```

---

## ✅ Gameplay Summary

* A **rotating cube** appears at the center.
* Camera moves with arrow keys:

  * ↑ = forward
  * ↓ = backward
  * ← = left
  * → = right
* The cube rotates continuously.

---

## 🎯 Next Steps

* Add **multiple cubes** with different colors and positions.
* Build a **floor grid** for orientation.
* Add **basic lighting** (diffuse shading).
* Create a **first-person camera system** with WASD + mouse look.
* Extend into a **full 3D game engine** with NeoPaquet’s math + graphics stack.

---

```

---

## ✅ What This Adds
- **3D rendering pipeline basics**: perspective, camera, cube geometry.  
- **Matrix math integration** from `linear_algebra.np`.  
- **Camera navigation** with keyboard controls.  
- A foundation for **full 3D games/engines** in NeoPaquet.  

---

⚡
