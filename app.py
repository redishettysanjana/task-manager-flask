from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Initialize DB
def init_db():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  task TEXT,
                  status TEXT,
                  priority TEXT)''')
    conn.commit()
    conn.close()

init_db()

# Home
@app.route('/')
def index():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()

    c.execute("SELECT * FROM tasks")
    tasks = c.fetchall()

    # Dashboard counts
    c.execute("SELECT COUNT(*) FROM tasks")
    total = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM tasks WHERE status='Completed'")
    completed = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM tasks WHERE status='Pending'")
    pending = c.fetchone()[0]

    conn.close()
    return render_template('index.html', tasks=tasks,
                           total=total, completed=completed, pending=pending)

# Add task
@app.route('/add', methods=['POST'])
def add():
    task = request.form['task']
    priority = request.form['priority']

    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("INSERT INTO tasks (task, status, priority) VALUES (?, ?, ?)",
              (task, "Pending", priority))
    conn.commit()
    conn.close()
    return redirect('/')

# Complete
@app.route('/complete/<int:id>')
def complete(id):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("UPDATE tasks SET status='Completed' WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

# Delete
@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

# Filter
@app.route('/filter/<status>')
def filter_tasks(status):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("SELECT * FROM tasks WHERE status=?", (status,))
    tasks = c.fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

# Search
@app.route('/search', methods=['POST'])
def search():
    keyword = request.form['keyword']

    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("SELECT * FROM tasks WHERE task LIKE ?", ('%' + keyword + '%',))
    tasks = c.fetchall()
    conn.close()

    return render_template('index.html', tasks=tasks)

# Edit
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()

    if request.method == 'POST':
        task = request.form['task']
        priority = request.form['priority']

        c.execute("UPDATE tasks SET task=?, priority=? WHERE id=?",
                  (task, priority, id))
        conn.commit()
        conn.close()
        return redirect('/')

    c.execute("SELECT * FROM tasks WHERE id=?", (id,))
    task = c.fetchone()
    conn.close()
    return render_template('edit.html', task=task)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)