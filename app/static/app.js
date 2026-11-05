// RF-01 a RF-05 / US-01 a US-05: apresentação e chamadas à API.
const list = document.querySelector('#task-list');
const message = document.querySelector('#message');
const count = document.querySelector('#count');
const form = document.querySelector('#task-form');
function notice(text, error = false) {
  message.textContent = text;
  message.classList.toggle('error', error);
}
async function request(url, options = {}) {
  let response;
  try { response = await fetch(url, options); }
  catch { throw new Error('Não foi possível comunicar com a aplicação.'); }
  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    const detail = data.detail;
    const explanation = typeof detail === 'string' ? detail :
      Array.isArray(detail) ? detail.map(x => x.msg || 'Dados inválidos').join('; ') : 'Pedido inválido.';
    throw new Error(explanation);
  }
  return data;
}
function taskRow(task) {
  const li = document.createElement('li');
  li.className = task.status === 'Concluída' ? 'done' : '';
  const info = document.createElement('div'); info.className = 'task-text';
  const title = document.createElement('strong'); title.textContent = task.title;
  const state = document.createElement('small'); state.textContent = task.status;
  info.append(title, state);
  if (task.description) { const description = document.createElement('p'); description.textContent = task.description; info.append(description); }
  const actions = document.createElement('div'); actions.className = 'task-actions';
  const button = document.createElement('button');
  const done = task.status === 'Concluída';
  button.textContent = done ? 'Reabrir' : 'Concluir';
  button.addEventListener('click', async () => {
    button.disabled = true;
    try {
      await request(`/api/tasks/${task.id}/${done ? 'reopen' : 'complete'}`, {method: 'PATCH'});
      await refresh(); notice(done ? 'Tarefa reaberta.' : 'Tarefa concluída.');
    } catch (error) { notice(error.message, true); button.disabled = false; }
  });
  actions.append(button); li.append(info, actions); return li;
}
async function refresh() {
  const tasks = await request('/api/tasks');
  list.replaceChildren(...tasks.map(taskRow));
  count.textContent = `${tasks.length} ${tasks.length === 1 ? 'tarefa' : 'tarefas'}`;
  if (!tasks.length) notice('Ainda não existem tarefas. Cria a primeira!');
  else notice('');
}
form.addEventListener('submit', async event => {
  event.preventDefault();
  const submit = form.querySelector('button[type="submit"]');
  submit.disabled = true;
  try {
    await request('/api/tasks', {method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({title:form.querySelector('#title').value,description:form.querySelector('#description').value || null})});
    form.reset(); await refresh(); notice('Tarefa criada com sucesso.');
  } catch (error) { notice(error.message, true); }
  finally { submit.disabled = false; }
});
refresh().catch(error => notice(error.message, true));
