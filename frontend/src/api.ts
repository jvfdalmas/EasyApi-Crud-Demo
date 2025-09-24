/** Base URL for the backend API. Override with Vite env var `VITE_API_BASE`. */
const API_BASE = (import.meta as any).env?.VITE_API_BASE || "http://localhost:8000";

/** Item entity as returned by the backend. */
export type Item = { id: number; name: string };

/**
 * Fetch all items from the backend.
 * @returns Promise resolving to the list of items.
 */
export async function listItems(): Promise<Item[]> {
  const res = await fetch(`${API_BASE}/items/`);
  if (!res.ok) throw new Error(`Failed to list items: ${res.status}`);
  return res.json();
}

/**
 * Create a new item.
 * @param name - The item name to create.
 * @returns Promise resolving to the created item.
 */
export async function createItem(name: string): Promise<Item> {
  const res = await fetch(`${API_BASE}/items/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name }),
  });
  if (!res.ok) throw new Error(`Failed to create item: ${res.status}`);
  return res.json();
}

/**
 * Delete an item by id.
 * @param id - The identifier of the item to delete.
 */
export async function deleteItem(id: number): Promise<void> {
  const res = await fetch(`${API_BASE}/items/${id}`, { method: "DELETE" });
  if (!res.ok) throw new Error(`Failed to delete item: ${res.status}`);
}


