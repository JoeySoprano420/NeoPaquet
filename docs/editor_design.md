# 📂 `docs/editor_design.md`

```markdown
# 🖥️ NeoPaquet Scene Editor Design
*A blueprint for a drag-and-drop visual editor for NeoPaquet.*

This document describes the design of a **visual scene editor** that integrates with the [NeoPaquet Engine](engine_design.md).  
It will allow developers to:
- Build levels visually  
- Inspect and modify entities/components  
- Attach scripts live  
- Export to NeoPaquet source or directly to binaries  

---

## 1. Editor Goals

- **User-Friendly:** graphical interface, no coding required for basic scenes.  
- **Live Editing:** change entity properties at runtime.  
- **Synchronized:** changes update both scene graph and NeoPaquet code.  
- **Cross-Platform:** desktop builds for Windows, macOS, Linux.  
- **Extensible:** plugins for new components, materials, and workflows.  

---

## 2. Core Features

### Scene Graph
- Tree view of all entities in the scene.  
- Drag-and-drop reordering.  
- Parenting (entity → child relationships).  

### Entity Inspector
- Transform: position, rotation, scale.  
- Components: Mesh, Material, RigidBody, Script.  
- Custom user components.  

### Hierarchy Panel
- Add/remove entities.  
- Search/filter entities by name, type, or tag.  

### Asset Browser
- Import meshes, textures, audio.  
- Drag-and-drop assets into the scene.  
- Preview thumbnails.  

### Script Editor
- Live NeoPaquet scripting with syntax highlighting.  
- Hot-reload scripts while the scene is running.  
- Inline CIAM macro suggestions.  

### Viewport
- 3D perspective navigation (WASD + mouse look).  
- Gizmos for move, rotate, scale.  
- Play mode toggle: edit → play → edit.  

---

## 3. Architecture

- **Frontend:** Electron + WebGL/Three.js (fast prototyping) or Qt (native).  
- **Backend:** NeoPaquet Engine runtime.  
- **Bridge:** JSON/IPC protocol between UI and engine.  

### Flow
```

Editor UI (scene.graph) <-> Engine Runtime (entities/components)

````

---

## 4. Scene Format

Scenes stored as `.npscene` files (NeoPaquet Scene):

```json
{
  "entities": [
    {
      "id": "player",
      "components": {
        "Transform": { "x": 0, "y": 0, "z": 0 },
        "Mesh": "models/player.obj",
        "Script": "scripts/player.np"
      }
    }
  ]
}
````

* JSON-like for portability.
* Export to `.np` source or compiled binary.

---

## 5. Live Scripting

Attach scripts in the editor:

```neopaquet
@onUpdate ("player") [dt] go {
    t = get_component("player", "Transform")
    t.x = t.x + 1.0 * dt
}
```

* Changes reflected immediately in the running game.
* Errors caught with try/catch/isolate macros.

---

## 6. Advanced Features (Future)

* Shader Editor: node-based material graph.
* Physics Debugger: visualize collision shapes.
* Animation Editor: keyframes + timeline.
* Networking Preview: simulate multiplayer locally.
* VR/AR Integration: edit in immersive mode.

---

## 7. Roadmap

* [x] Scene Graph Prototype
* [ ] Entity Inspector UI
* [ ] Asset Browser Integration
* [ ] Script Hot-Reloading
* [ ] Viewport Camera Controls
* [ ] Export/Import `.npscene`
* [ ] Advanced Editors (shaders, animations)

---

## ✅ Summary

The **NeoPaquet Scene Editor** will:

* Provide a **drag-and-drop workflow** for game developers.
* Let coders and non-coders collaborate.
* Serve as a **front-end to the NeoPaquet Engine**.
* Enable **rapid iteration** of 2D/3D games.

This editor + engine combo makes NeoPaquet a **full development ecosystem**.

```

---

## ✅ What This Adds
- A **visual editor plan** to complement the engine.  
- Defines **scene graph, inspector, asset browser, live scripting**.  
- Explains **scene format and architecture**.  
- Provides a clear **roadmap**.  

---

⚡ 
