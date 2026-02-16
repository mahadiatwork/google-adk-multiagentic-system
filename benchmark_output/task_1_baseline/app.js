function addTodo() {
    const todoInput = document.getElementById('todo-input');
    const todoText = todoInput.value.trim();

    if (todoText === '') {
        alert('Please enter a task.');
        return;
    }

    const todoList = document.getElementById('todo-list');
    const todoItem = document.createElement('li');
    todoItem.className = 'todo-item';

    const taskText = document.createElement('span');
    taskText.textContent = todoText;

    const removeButton = document.createElement('button');
    removeButton.className = 'remove-button';
    removeButton.textContent = 'Remove';
    removeButton.onclick = function() {
        todoList.removeChild(todoItem);
    };

    todoItem.appendChild(taskText);
    todoItem.appendChild(removeButton);
    todoList.appendChild(todoItem);

    todoInput.value = '';
}