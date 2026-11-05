const PAGE_SIZE = 10;
let page = 1;

const $ = (id) => document.getElementById(id);

async function load() {
  const status = $("filter").value;
  let url = `/api/tasks?page=${page}&page_size=${PAGE_SIZE}`;
  if (status) url += `&status=${status}`;

  const res = await fetch(url);
  const data = await res.json();

  const list = $("list");
  list.innerHTML = "";
  for (const t of data.items) {
    const li = document.createElement("li");
    li.className = t.status;
    li.innerHTML = `
      <input type="checkbox" ${t.status === "done" ? "checked" : ""}>
      <span class="title">${t.title}</span>
      <button class="del">Borrar</button>
    `;
    li.querySelector("input").onchange = () => toggle(t.id);
    li.querySelector(".del").onclick = () => remove(t.id);
    list.appendChild(li);
  }

  const pages = Math.max(1, Math.ceil(data.total / PAGE_SIZE));
  $("page-info").textContent = `Página ${page} de ${pages}`;
  $("prev").disabled = page <= 1;
  $("next").disabled = page >= pages;
}

async function toggle(id) {
  await fetch(`/api/tasks/${id}/toggle`, { method: "PATCH" });
  load();
}

async function remove(id) {
  await fetch(`/api/tasks/${id}`, { method: "DELETE" });
  load();
}

$("add").onclick = async () => {
  const title = $("new-title").value;
  await fetch("/api/tasks", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title }),
  });
  $("new-title").value = "";
  page = 1;
  load();
};

$("filter").onchange = () => { page = 1; load(); };
$("prev").onclick = () => { page--; load(); };
$("next").onclick = () => { page++; load(); };

load();
