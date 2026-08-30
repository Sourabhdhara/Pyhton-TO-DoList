# To-Do List Manager — Full Documentation

**A colorful, pure-Python desktop task manager built with Tkinter.**

---

## Table of Contents

1. [Overview](#1-overview)
2. [Features](#2-features)
3. [Tech Stack](#3-tech-stack)
4. [Project Structure](#4-project-structure)
5. [Installation & Setup](#5-installation--setup)
6. [How to Use the App](#6-how-to-use-the-app)
7. [Architecture & Data Flow](#7-architecture--data-flow)
8. [Code Walkthrough (Function by Function)](#8-code-walkthrough-function-by-function)
9. [UI Design System](#9-ui-design-system)
10. [Error Handling](#10-error-handling)
11. [Customization Guide](#11-customization-guide)
12. [Known Limitations](#12-known-limitations)
13. [Possible Future Enhancements](#13-possible-future-enhancements)
14. [Troubleshooting](#14-troubleshooting)

---

## 1. Overview

The To-Do List Manager is a **single-window desktop application** written entirely in
Python using **Tkinter**, the GUI toolkit built into the standard Python installation.
It runs completely offline — no internet connection, no external services, and no
third-party packages are required.

The app lets a user type in tasks, add them to a running list, mark tasks as completed,
and remove tasks they no longer need — all through a colorful, simple interface.

This app also serves as the **visual style reference** for other Tkinter apps in this
project family (e.g. the WeatherWise and BMI Calculator apps), which reuse its color
palette, fonts, and button layout conventions.

---

## 2. Features

| Feature | Description |
|---|---|
| ➕ Add task | Type a task into the entry box and click **Add** to append it to the list. |
| ❌ Delete task | Select any task in the list and click **Delete** to remove it. |
| ✔ Mark as completed | Select a task and click **Mark Completed** to prefix it with a ✔ checkmark, without removing it from the list. |
| 🚪 Exit | Closes the application window. |
| 🖼️ Custom window icon | Uses a custom to-do-list icon (`todo.png`), also shown inline in the title bar text of the app itself. |
| 🎨 Colorful UI | Light-blue background, blue title banner, pale-yellow entry box and task list, and bold colorful buttons — all in Comic Sans MS. |
| ↔️ Resizable window | The window can be resized between a minimum of 500×500 and a maximum of 750×630. |
| ✅ Input validation | Warns the user if they try to add an empty task, or delete/complete a task without selecting one first. |

---

## 3. Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3 |
| GUI toolkit | `tkinter` (built into Python — no install needed) |
| Dialogs | `tkinter.messagebox` (warning pop-ups) |

**This app has zero third-party dependencies** — everything it imports ships with a
standard Python installation. No `pip install` is required at all.

---

## 4. Project Structure

```
ToDOList/
├── todolist.py   ← the entire application
└── todo.png      ← window icon / logo image (shown in the title bar and window icon)
```

`todo.png` must stay in the **same folder** as `todolist.py` — the code loads it using a
relative path (`file="todo.png"`), so if the image is moved elsewhere, the app will fail
to start.

---

## 5. Installation & Setup

### Requirements
- Python 3.8 or newer (Tkinter ships with the standard installer on Windows/macOS; on
  some Linux distributions you may need `sudo apt install python3-tk`)
- The `todo.png` file, kept alongside `todolist.py`

### Steps

```bash
# No pip install needed — everything used is part of the Python standard library.
python todolist.py
```

A window titled **"To Do List Manager"** will open, starting at 500×500 and resizable up
to 750×630.

---

## 6. How to Use the App

1. **Type a task** into the "Enter Task" box.
2. Click **➕ Add** to add it to the list below. The entry box clears automatically so
   you can type the next task right away.
3. **To mark a task done:** click once on it in the list to select it, then click
   **✔ Mark Completed**. A ✔ is added in front of the task text — the task stays in the
   list, just visually marked.
4. **To remove a task entirely:** select it, then click **❌ Delete**.
5. Click **Exit ➜]** to close the app.

---

## 7. Architecture & Data Flow

```
        ┌─────────────────────────┐
        │  User types a task and   │
        │  clicks "➕ Add"          │
        └────────────┬─────────────┘
                      ▼
             ┌──────────────────┐
             │    add_task()      │
             │ - read entry text  │
             │ - validate non-empty│
             │ - insert into listbox│
             │ - clear entry box   │
             └──────────────────┘

        ┌─────────────────────────┐
        │  User selects a task and │
        │  clicks "❌ Delete"       │
        └────────────┬─────────────┘
                      ▼
             ┌──────────────────┐
             │   delete_task()    │
             │ - get selected index│
             │ - remove from listbox│
             └──────────────────┘

        ┌─────────────────────────┐
        │  User selects a task and │
        │  clicks "✔ Mark Completed"│
        └────────────┬─────────────┘
                      ▼
             ┌───────────────────────┐
             │  mark_completed()       │
             │ - get selected task text │
             │ - skip if already marked │
             │ - remove + re-insert with│
             │   a ✔ prefix, same position│
             └───────────────────────┘
```

There is no database, file, or network involved anywhere — the `Listbox` widget itself
**is** the storage. All task data lives only in memory for as long as the window is open
(see [Known Limitations](#12-known-limitations)).

---

## 8. Code Walkthrough (Function by Function)

### `add_task()`
1. Reads the current text from `task_entry` and strips leading/trailing whitespace.
2. If the text is non-empty, inserts it at the end of `list_box` (`tk.END`) and clears
   the entry box so the user can immediately type another task.
3. If the text is empty (or just whitespace), shows a warning popup instead of adding a
   blank row.

### `delete_task()`
1. Reads `list_box.curselection()` — a tuple of the indices of currently selected list
   items (Tkinter's `Listbox` allows multi-select, but this app treats it as single-select
   by only ever using `[0]`, the first selected index).
2. Deletes that index from the listbox.
3. If nothing was selected, `curselection()` returns an empty tuple, so indexing `[0]`
   raises an `IndexError` — the function catches that and shows a warning popup instead
   of crashing.

### `mark_completed()`
1. Gets the selected index the same way as `delete_task()`.
2. Reads the task's current text with `list_box.get(selected_index)`.
3. Checks whether the text already starts with `"✔"` — this prevents double-marking a
   task that's already completed.
4. If not yet marked, deletes the original entry and re-inserts the same text with a
   `"✔ "` prefix **at the same index**, so the task's position in the list doesn't
   change.
5. Also wrapped in a `try/except IndexError` for the same reason as `delete_task()`.

### GUI Setup (bottom section of the file)
This part of the script (not wrapped in a function) builds the window once, in this
order:
1. Creates the main `window`, sets its title, size (with `minsize`/`maxsize` bounds),
   background color, and icon.
2. Builds the title banner (`title_label`) — a label that also displays the `todo.png`
   image inline next to the text, using `compound="left"`.
3. Builds the entry row (`entry_frame`) with a label, a text entry box, and the
   **➕ Add** button, wired to `add_task` via `command=`.
4. Builds the button row (`button_frame`) with **❌ Delete**, **✔ Mark Completed**, and
   **Exit ➜]** buttons, each wired to their respective function.
5. Builds the `list_frame` containing the `Listbox` widget itself, where all tasks are
   displayed.
6. Calls `window.mainloop()` to start the event loop and keep the window open.

---

## 9. UI Design System

| Element | Color / Style | Notes |
|---|---|---|
| Window background | `#d2dff7` (light blue) | Applied to the window and both frames |
| Title banner background | `#5c8fed` (medium blue) | White bold text, Comic Sans MS 30pt, with the to-do icon shown inline |
| Task entry field background | `#fdf2b3` (pale yellow) | Sunken 2px border (`relief="sunken"`) |
| Task list (Listbox) background | `#fdf2b3` (pale yellow) | Sunken 5px border, matches the entry field |
| Add button | `green` background, white text | |
| Delete button | `red` background, white text | |
| Mark Completed button | `#1e90ff` (blue) background, white text | |
| Exit button | `#717274` (gray) background, white text | |
| Font | `"Comic Sans MS"`, bold, throughout | Falls back to a system default if not installed |
| Window size | Starts at 500×500; resizable between 500×500 and 750×630 | |

All widgets are plain `tk` widgets (no `ttk`), which is why every color can be set
directly with `bg=`/`fg=` — there's no theming layer to work around. This exact palette
and button-color convention (green = add/positive, red = delete/negative, blue = neutral
action, gray = exit) is reused across the other apps in this project family.

---

## 10. Error Handling

| Situation | What happens |
|---|---|
| Clicking Add with an empty entry box | Warning popup: *"⚠️ Task cannot be empty."* |
| Clicking Delete with no task selected | Warning popup: *"📭 No task selected to delete."* |
| Clicking Mark Completed with no task selected | Warning popup: *"📭 No task selected to mark as completed."* |
| Clicking Mark Completed on an already-completed task | Silently does nothing — the `✔` prefix check prevents a duplicate checkmark |

All three interactive functions (`add_task`, `delete_task`, `mark_completed`) are
defensive: they never assume a selection exists, and they catch the specific error
(`IndexError`) that Tkinter raises when nothing is selected, rather than letting the app
crash.

---

## 11. Customization Guide

- **Change the color scheme:** the app doesn't use named constants — colors are written
  directly into each widget's `bg=`/`fg=` arguments, so search-and-replace hex codes like
  `#d2dff7`, `#5c8fed`, `#fdf2b3`, `green`, `red`, `#1e90ff`, and `#717274` throughout the
  file.
- **Change the window icon:** replace `todo.png` with another PNG of the same name, or
  update the filename in both `tk.PhotoImage(file=...)` calls.
- **Change the completed-task marker:** edit the `"✔ "` prefix string inside
  `mark_completed()` (and the `.startswith("✔")` check just above it, so they stay in
  sync).
- **Allow un-marking a completed task:** currently `mark_completed()` only adds the
  checkmark; add an `else` branch that strips the `"✔ "` prefix if the task is clicked
  again.
- **Change window size limits:** edit the `window.minsize(...)` / `window.maxsize(...)`
  calls.

---

## 12. Known Limitations

- **No persistence:** all tasks live only in the `Listbox` widget's memory. Closing the
  app (or it crashing) loses the entire list — there is no file, database, or
  auto-save of any kind.
- **Single selection only:** although Tkinter's `Listbox` supports selecting multiple
  items, `delete_task()` and `mark_completed()` only ever act on the first selected
  index (`curselection()[0]`), so multi-select doesn't do anything useful here.
- **No task editing:** there's no way to edit a task's text after adding it — only
  delete-and-re-add.
- **No due dates, priorities, or categories** — tasks are plain text only.
- `todo.png` must exist in the same directory as `todolist.py`, or the app will crash on
  startup with a `TclError`.

---

## 13. Possible Future Enhancements

- **Save/load tasks** to a local file (e.g. JSON or plain text) so the list survives
  restarting the app
- **Double-click to edit** a task's text in place
- **Un-mark** a completed task back to incomplete
- **Reorder tasks** (move up/down) or drag-and-drop
- **Due dates and priority levels**, shown with color-coded tags in the listbox
- **Search/filter** box to quickly find a task in a long list
- **Keyboard shortcuts** (e.g. Enter to add, Delete key to remove selected)
- Package the app with PyInstaller into a standalone `.exe`/`.app` so `todo.png` is
  bundled automatically and Python doesn't need to be installed separately

---

## 14. Troubleshooting

| Problem | Likely cause | Fix |
|---|---|---|
| `_tkinter.TclError: couldn't open "todo.png"` | The image file isn't in the same folder as `todolist.py`, or was renamed | Make sure `todo.png` sits next to `todolist.py` in the same directory |
| "No task selected" warning even though a task is visible | The task wasn't actually clicked/selected (a single click is required before Delete/Mark Completed) | Click directly on the task text in the list first, then click the button |
| Clicking Add does nothing | The entry box only contained spaces, which get stripped to an empty string | Type an actual task with visible characters |
| All tasks disappear after closing and reopening the app | Expected — the app has no save/load feature (see [Known Limitations](#12-known-limitations)) | None currently; would require the "Save/load tasks" enhancement above |
| Fonts look different than expected | `Comic Sans MS` isn't installed on the OS | Install the font, or edit the font family in the code to one available on your system |
