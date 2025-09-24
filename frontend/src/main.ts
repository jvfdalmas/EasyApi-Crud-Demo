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
    <ul id="items"></ul>
  </div>
`

const listEl = document.querySelector<HTMLUListElement>('#items')!
const formEl = document.querySelector<HTMLFormElement>('#item-form')!
const inputEl = document.querySelector<HTMLInputElement>('#item-input')!

/**
 * Render the item list into the DOM.
 * @param items - Items to display.
 */
function render(items: Item[]) {
  listEl.innerHTML = ''
  for (const item of items) {
    const li = document.createElement('li')
    li.textContent = `${item.id} · ${item.name} `
    const del = document.createElement('button')
    del.textContent = 'Delete'
    del.onclick = async () => {
      await deleteItem(item.id)
      load()
    }
    li.appendChild(del)
    listEl.appendChild(li)
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
