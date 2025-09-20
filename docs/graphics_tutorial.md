# 🎨 NeoPaquet Graphics Tutorial
*A beginner’s guide to drawing with `stdlib/graphics.np`.*

This tutorial shows you how to use NeoPaquet’s graphics library to:
- Create a window  
- Draw points, lines, triangles, and rectangles  
- Use colors and transformations  
- Animate with a main loop  

---

## 1. Setup

Make sure you have:
- NeoPaquet installed (`npaquetc`)  
- OpenGL and GLFW available on your system  

Import the graphics library in your program:
```neopaquet
import "stdlib/core.np"
import "stdlib/graphics.np"

# 📂 `docs/graphics_tutorial.md`

````markdown
# 🎨 NeoPaquet Graphics Tutorial
*A beginner’s guide to drawing with `stdlib/graphics.np`.*

This tutorial shows you how to use NeoPaquet’s graphics library to:
- Create a window  
- Draw points, lines, triangles, and rectangles  
- Use colors and transformations  
- Animate with a main loop  

---

## 1. Setup

Make sure you have:
- NeoPaquet installed (`npaquetc`)  
- OpenGL and GLFW available on your system  

Import the graphics library in your program:
```neopaquet
import "stdlib/core.np"
import "stdlib/graphics.np"
````

---

## 2. Create a Window

```neopaquet
src () "stdout" {
  window = gfx_init(800, 600, "NeoPaquet Graphics")
  gfx_run(window, draw)
} run

@func ("draw") [] go {
  gfx_set_color(1.0, 1.0, 1.0, 1.0)   -- white
  gfx_draw_point(0.0, 0.0)
}
```

➡️ Opens a window and draws a white point at the center.

---

## 3. Drawing Shapes

### Line

```neopaquet
gfx_set_color(1.0, 0.0, 0.0, 1.0)     -- red
gfx_draw_line(-0.5, -0.5, 0.5, 0.5)
```

### Triangle

```neopaquet
gfx_set_color(0.0, 1.0, 0.0, 1.0)     -- green
gfx_draw_triangle(-0.5, -0.5, 0.5, -0.5, 0.0, 0.5)
```

### Rectangle

```neopaquet
gfx_set_color(0.0, 0.0, 1.0, 1.0)     -- blue
gfx_draw_rect(-0.5, -0.5, 1.0, 1.0)
```

---

## 4. Colors

Colors are **RGBA floats** (`0.0` to `1.0`):

```neopaquet
gfx_set_color(1.0, 0.5, 0.0, 1.0)     -- orange
gfx_draw_point(0.2, 0.2)
```

---

## 5. Transformations

Translate, scale, and rotate shapes:

```neopaquet
gfx_translate(0.5, 0.0, 0.0)          -- move right
gfx_scale(0.5, 0.5, 1.0)              -- shrink
gfx_rotate(45, 0.0, 0.0, 1.0)         -- rotate around Z
```

---

## 6. Animation

Use `gfx_run` with a callback that changes state each frame:

```neopaquet
angle = 0

@func ("draw") [] go {
  gfx_set_color(1.0, 1.0, 0.0, 1.0)   -- yellow
  gfx_rotate(angle, 0.0, 0.0, 1.0)
  gfx_draw_triangle(-0.5, -0.5, 0.5, -0.5, 0.0, 0.5)
  angle = angle + 1
}
```

➡️ Draws a spinning yellow triangle.

---

## 7. Full Example

```neopaquet
import "stdlib/core.np"
import "stdlib/graphics.np"

angle = 0

src () "stdout" {
  window = gfx_init(800, 600, "NeoPaquet Graphics")
  gfx_run(window, draw)
} run

@func ("draw") [] go {
  gfx_set_color(0.2, 0.6, 1.0, 1.0)   -- sky blue
  gfx_draw_rect(-0.5, -0.5, 1.0, 1.0)

  gfx_set_color(1.0, 1.0, 0.0, 1.0)   -- yellow
  gfx_rotate(angle, 0.0, 0.0, 1.0)
  gfx_draw_triangle(-0.3, -0.3, 0.3, -0.3, 0.0, 0.4)

  angle = angle + 1
}
```

➡️ Opens a window with:

* A blue square background
* A spinning yellow triangle

---

## ✅ Next Steps

* Explore `stdlib/linear_algebra.np` for building transformation + projection matrices.
* Combine graphics with input handling (`glfwGetKey`) to make interactive programs.
* Try exporting matrices with `gfx_load_matrix4` for 3D rendering.

---

```

---

## ✅ What This Adds
- A **step-by-step tutorial** to graphics basics in NeoPaquet.  
- Covers **window creation → drawing → colors → transformations → animation**.  
- Includes a **full spinning triangle demo** as a capstone.  

---

⚡ 
