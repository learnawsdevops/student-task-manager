const form = document.getElementById("taskForm");
const input = document.getElementById("taskInput");
const list = document.getElementById("taskList");
const message = document.getElementById("message");

async function api(path, options = {}) {
  const response = await fetch(path, {
    ...options,
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
  });
  if (response.status === 204) return null;
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || "Request failed");
  return data;
}

async function loadTasks() {
  try {
    const tasks = await api("/api/tasks");
    list.replaceChildren();
    if (!tasks.length) {
      const empty = document.createElement("li");
      empty.className = "empty";
      empty.textContent = "No tasks yet.";
      list.appendChild(empty);
      return;
    }
    tasks.forEach(addTaskRow);
  } catch (error) {
    message.textContent = error.message;
  }
}

function addTaskRow(task) {
  const item = document.createElement("li");
  item.className = task.completed ? "completed" : "";

  const title = document.createElement("span");
  title.className = "task-title";
  title.textContent = task.title;

  const complete = document.createElement("button");
  complete.type = "button";
  complete.className = "complete-btn";
  complete.textContent = task.completed ? "Mark pending" : "Complete";
  complete.addEventListener("click", () => toggleTask(task));

  const remove = document.createElement("button");
  remove.type = "button";
  remove.className = "delete-btn";
  remove.textContent = "Delete";
  remove.addEventListener("click", () => deleteTask(task.id));

  item.append(title, complete, remove);
  list.appendChild(item);
}

async function toggleTask(task) {
  try {
    await api(`/api/tasks/${task.id}`, {
      method: "PATCH",
      body: JSON.stringify({ completed: !task.completed }),
    });
    await loadTasks();
  } catch (error) {
    message.textContent = error.message;
  }
}

async function deleteTask(id) {
  try {
    await api(`/api/tasks/${id}`, { method: "DELETE" });
    await loadTasks();
  } catch (error) {
    message.textContent = error.message;
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  try {
    await api("/api/tasks", {
      method: "POST",
      body: JSON.stringify({ title: input.value }),
    });
    input.value = "";
    message.textContent = "";
    await loadTasks();
  } catch (error) {
    message.textContent = error.message;
  }
});

loadTasks();
