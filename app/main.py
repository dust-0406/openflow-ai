
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(
    title="OpenFlow AI",
    description="An open-source AI automation platform",
    version="0.1.0",
)

tasks = []
next_id = 1


class TaskInput(BaseModel):
    title: str


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>OpenFlow AI</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 700px;
                margin: 60px auto;
                padding: 20px;
                background: #f4f6f8;
                color: #222;
            }
            .card {
                background: white;
                padding: 24px;
                border-radius: 12px;
                box-shadow: 0 4px 16px #0001;
            }
            input, button {
                padding: 10px;
                font-size: 15px;
            }
            input { width: 65%; }
            button {
                cursor: pointer;
                background: #2563eb;
                color: white;
                border: 0;
                border-radius: 5px;
            }
            li { margin: 12px 0; }
            .done { text-decoration: line-through; color: gray; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>OpenFlow AI 🚀</h1>
            <p>你的开源 AI 自动化平台，从这里开始。</p>
            <h2>任务管理器</h2>
            <form id="task-form">
                <input id="task-input" placeholder="输入一个任务..." required>
                <button type="submit">添加</button>
            </form>
            <ul id="tasks"></ul>
            <p id="status"></p>
        </div>
        <script>
            const form = document.getElementById("task-form");
            const input = document.getElementById("task-input");
            const list = document.getElementById("tasks");
            const status = document.getElementById("status");

            async function loadTasks() {
                const response = await fetch("/api/tasks");
                const tasks = await response.json();
                list.replaceChildren();

                tasks.forEach(task => {
                    const li = document.createElement("li");
                    const label = document.createElement("span");
                    label.textContent = task.title;
                    if (task.done) label.className = "done";

                    const toggle = document.createElement("button");
                    toggle.textContent = task.done ? "撤销" : "完成";
                    toggle.style.marginLeft = "10px";
                    toggle.onclick = async () => {
                        await fetch(`/api/tasks/${task.id}`, {
                            method: "PATCH"
                        });
                        loadTasks();
                    };

                    const remove = document.createElement("button");
                    remove.textContent = "删除";
                    remove.style.marginLeft = "6px";
                    remove.onclick = async () => {
                        await fetch(`/api/tasks/${task.id}`, {
                            method: "DELETE"
                        });
                        loadTasks();
                    };

                    li.append(label, toggle, remove);
                    list.appendChild(li);
                });

                status.textContent = `共 ${tasks.length} 个任务`;
            }

            form.addEventListener("submit", async event => {
                event.preventDefault();
                const title = input.value.trim();
                if (!title) return;

                const response = await fetch("/api/tasks", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({title})
                });

                if (response.ok) {
                    input.value = "";
                    loadTasks();
                } else {
                    status.textContent = "添加失败，请重试。";
                }
            });

            loadTasks();
        </script>
    </body>
    </html>
    """


@app.get("/api/health")
def health():
    return {"status": "healthy", "project": "OpenFlow AI"}


@app.get("/api/tasks")
def get_tasks():
    return tasks


@app.post("/api/tasks", status_code=201)
def create_task(task: TaskInput):
    global next_id

    item = {
        "id": next_id,
        "title": task.title.strip(),
        "done": False,
    }
    next_id += 1
    tasks.append(item)
    return item


@app.patch("/api/tasks/{task_id}")
def toggle_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = not task["done"]
            return task

    from fastapi import HTTPException
    raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/api/tasks/{task_id}")
def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            return tasks.pop(index)

    from fastapi import HTTPException
    raise HTTPException(status_code=404, detail="Task not found")
