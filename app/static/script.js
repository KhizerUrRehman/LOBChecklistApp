const gamedaySelect = document.getElementById("gameday");
const checklistEl = document.getElementById("checklist");

const tasks = ["Cameras", "Stream", "Referees", "Table Team", "Scoreboard"];

async function populateGamedays() {
    const options = [...document.querySelectorAll("option")];
    if (options.length > 0) return; // already filled
    const days = Array.from(document.querySelectorAll("option")).map(o => o.value);
    fetch("/").then(() => {
        const matches = document.body.innerHTML.match(/value=\"(20[0-9]{2}-[0-9]{2}-[0-9]{2})\"/g);
        const dates = [...new Set(matches?.map(m => m.slice(7, 17)))];
        for (const date of dates) {
            const option = document.createElement("option");
            option.value = date;
            option.textContent = date;
            gamedaySelect.appendChild(option);
        }
        loadChecklist();
    });
}

async function loadChecklist() {
    const date = gamedaySelect.value;
    const res = await fetch(`/get/${date}`);
    const data = await res.json();
    checklistEl.innerHTML = "";
    tasks.forEach((task, i) => {
        const li = document.createElement("li");
        const cb = document.createElement("input");
        cb.type = "checkbox";
        cb.checked = data[i];
        cb.onchange = () => saveChecklist();
        li.appendChild(cb);
        li.append(" " + task);
        checklistEl.appendChild(li);
    });
}

async function saveChecklist() {
    const date = gamedaySelect.value;
    const states = Array.from(document.querySelectorAll("#checklist input")).map(cb => cb.checked);
    await fetch(`/update/${date}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ items: states })
    });
}

gamedaySelect.onchange = loadChecklist;

document.addEventListener("DOMContentLoaded", () => {
    populateGamedays();
});
