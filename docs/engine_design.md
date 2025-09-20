# 📂 `docs/engine_design.md`

```markdown
# 🏗️ NeoPaquet Game Engine Design
*A blueprint for building a 3D game engine in NeoPaquet.*

This document outlines the architecture of a **NeoPaquet-powered 3D engine**, covering:
- Core runtime  
- Rendering pipeline  
- Input & events  
- Physics & collisions  
- Entity-component system (ECS)  
- Scripting & extensibility  

---

## 1. Engine Goals

- **Execution-Oriented:** minimal runtime overhead, instant AOT execution.  
- **Cross-Platform:** Windows, macOS, Linux, Kali.  
- **Interop-Ready:** OpenGL, Vulkan, DirectX, Unity, Unreal, WASM.  
- **Modular:** each subsystem can be replaced or extended.  
- **Safe:** CIAM-based memory safety, anti-use-after-free built in.  
- **Blazing-Fast Dev:** PGO, loop unrolling, and vectorization intrinsic.  

---

## 2. Core Runtime

### Components
- **Engine Init** (`engine_init`, `engine_shutdown`)  
- **Main Loop** (`engine_run`) → update → physics → render → swap  
- **Resource Manager** → loads assets (meshes, textures, sounds)  
- **Timer System** → delta-time for framerate independent updates  

### Flow
```

engine\_init()
while not exit:
handle\_input()
update\_entities(dt)
run\_physics(dt)
render\_scene()
swap\_buffers()
engine\_shutdown()

````

---

## 3. Rendering Pipeline

### Stages
1. **Setup Context** → create window + graphics API binding.  
2. **Camera & Projection** → `mat4_perspective`, `mat4_lookat`.  
3. **Scene Graph** → hierarchical transforms.  
4. **Draw Calls** → submit meshes, textures, shaders.  
5. **Post-Processing** → bloom, HDR, tone mapping (future).  

### APIs Supported
- OpenGL (default)  
- Vulkan (advanced, planned)  
- DirectX (Windows interop)  
- WebGL/WASM (browser export)  

---

## 4. Input & Events

### Keyboard / Mouse
- Key states: pressed, released, held.  
- Mouse movement: deltaX, deltaY.  
- Mouse buttons: left, right, middle.  

### Gamepad
- Button mappings standardized.  
- Axis values normalized.  

### Event Dispatch
- Callbacks registered per entity or globally.  

---

## 5. Physics & Collisions

### Physics Core
- **Rigid Body Dynamics** → velocity, acceleration, forces.  
- **Collision Detection** → AABB, Sphere, OBB.  
- **Collision Response** → impulses, friction.  

### Optional Extensions
- Soft bodies (cloth, jelly).  
- Raycasting (for bullets, mouse picking).  
- Physics materials (bouncy, slippery, sticky).  

---

## 6. Entity-Component System (ECS)

### Entities
- Lightweight IDs, no behavior by default.  

### Components
- `Transform` (position, rotation, scale)  
- `Mesh` (geometry reference)  
- `Material` (shader + texture)  
- `RigidBody` (mass, velocity)  
- `Script` (user-defined behavior)  

### Systems
- Transform system (apply matrices).  
- Render system (draw meshes).  
- Physics system (simulate bodies).  
- Script system (execute logic).  

---

## 7. Scripting Layer

NeoPaquet scripts control entities directly:

```neopaquet
@func ("update") [entity, dt] go {
    t = get_component(entity, "Transform")
    t.x = t.x + 1.0 * dt
}
````

* Hot-reloadable during runtime.
* Sandbox mode for untrusted scripts.
* CIAM macros can extend syntax (e.g., `@onCollision`).

---

## 8. Asset Pipeline

* **Mesh Formats:** `.obj`, `.fbx`, `.gltf` → converted into engine-native format.
* **Textures:** `.png`, `.jpg`, `.tga`.
* **Audio:** `.wav`, `.ogg`.
* **Shaders:** GLSL/HLSL compiled to backend IR.

---

## 9. Extensibility

* **Modules:** add physics engines, AI, networking.
* **Plugins:** hot-swappable DLLs/so files.
* **Interop:** C API exposed for external bindings.

---

## 10. Roadmap

* [x] Core runtime & 2D graphics
* [x] Linear algebra + 3D transforms
* [ ] Basic 3D cube world (tutorial stage)
* [ ] ECS with Transform + Mesh + Material
* [ ] Physics integration
* [ ] Scripting hooks
* [ ] Editor prototype (visual scene builder)
* [ ] Full game runtime

---

## ✅ Summary

The **NeoPaquet Game Engine** is:

* **Lightweight** but expandable.
* **Execution-Oriented** with instant startup.
* **Safe by design** (CIAM macros prevent memory corruption).
* **Ready for the future** (WASM, Vulkan, Unreal/Unity interop).

This blueprint serves as the **foundation** for a production-grade engine written in NeoPaquet.

---

```

---

## ✅ What This Adds
- Full **engine architecture** blueprint.  
- Defines subsystems: rendering, input, physics, ECS, scripting.  
- Clear **roadmap** from tutorials → real engine.  

---

⚡ 
