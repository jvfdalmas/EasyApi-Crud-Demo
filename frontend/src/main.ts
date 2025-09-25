import './style.css'
import { listItems, createItem, deleteItem, type Item } from './api'

// Root application container
const app = document.querySelector<HTMLDivElement>('#app')!

app.innerHTML = `
  <div>
    <h1>Items</h1>
    <form id="item-form">
      <input id="item-input" type="text" placeholder="Enter name" required />
      <button type="submit">Add</button>
    </form>
    <table class="items-table">
      <thead>
        <tr>
          <th>Data</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody id="items-body"></tbody>
    </table>
  </div>
`

const tableBodyEl = document.querySelector<HTMLTableSectionElement>('#items-body')!
const formEl = document.querySelector<HTMLFormElement>('#item-form')!
const inputEl = document.querySelector<HTMLInputElement>('#item-input')!

/**
 * Render the item list into the DOM.
 * @param items - Items to display.
 */
function render(items: Item[]) {
  tableBodyEl.innerHTML = ''
  for (const item of items) {
    const tr = document.createElement('tr')

    const dataTd = document.createElement('td')
    dataTd.textContent = `${item.id} · ${item.name}`

    const actionTd = document.createElement('td')
    actionTd.className = 'actions'
    const del = document.createElement('button')
    del.textContent = 'Delete'
    del.onclick = async () => {
      await deleteItem(item.id)
      load()
    }
    actionTd.appendChild(del)

    tr.appendChild(dataTd)
    tr.appendChild(actionTd)
    tableBodyEl.appendChild(tr)
  }
}

/** Load and render items from the API. */
async function load() {
  const items = await listItems()
  render(items)
}

// Handle create form submit
formEl.addEventListener('submit', async (e) => {
  e.preventDefault()
  const name = inputEl.value.trim()
  if (!name) return
  await createItem(name)
  inputEl.value = ''
  load()
})

// Initial load
load()
