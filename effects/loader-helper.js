export async function loadModule(url, containerId) {
  try {
    const res = await fetch(url);
    const html = await res.text();
    document.getElementById(containerId).innerHTML = html;
  } catch (err) {
    console.error(`Error loading module ${url}:`, err);
  }
}
