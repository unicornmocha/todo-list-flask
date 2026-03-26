from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

todos = [
    {'id': 1, 'name': "Learn about CORS", 'checked': False},
    {'id': 2, 'name': "Learn about middleware", 'checked': False}
]

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        task = request.form.get('task', '').strip()
        if task:
            todos.append({
                'id': len(todos) + 1,
                'name': task,
                'checked': False
            })
        return redirect(url_for('home'))

    return render_template('index.html', items=todos)

@app.route('/checked/<int:task_id>', methods=['POST'])
def toggle_checked(task_id):
    for todo in todos:
        if todo['id'] == task_id:
            todo['checked'] = not todo['checked']
            break
    return redirect(url_for('home'))

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    global todos
    for todo in todos:
        if todo['id'] == task_id:
            todos.remove(todo)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)