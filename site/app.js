const side = document.querySelector(".side")
document.querySelector(".menu-btn")?.addEventListener("click", () => side.classList.toggle("open"))

const mask = document.querySelector(".mask")
const q = document.querySelector(".modal input")
const hits = document.querySelector(".hits")
let index = null
const siteRoot = window.SITE_ROOT || "/"

function localUrl(url) {
  if (!url || !url.startsWith("/")) return url
  return siteRoot + url.slice(1)
}

function openSearch() {
  mask.hidden = false
  q.focus()
  if (!index) {
    fetch(`${siteRoot}search.json`)
      .then((r) => r.json())
      .then((data) => { index = data })
  }
}
function closeSearch() { mask.hidden = true }

document.querySelector(".search-btn")?.addEventListener("click", openSearch)
mask?.addEventListener("click", (e) => { if (e.target === mask) closeSearch() })
document.addEventListener("keydown", (e) => {
  if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k") {
    e.preventDefault()
    openSearch()
  }
  if (e.key === "Escape") closeSearch()
})

q?.addEventListener("input", () => {
  const term = q.value.trim().toLowerCase()
  if (!index || term.length < 1) {
    hits.innerHTML = ""
    return
  }
  const found = index.filter((item) => (item.title + item.text).toLowerCase().includes(term)).slice(0, 12)
  hits.innerHTML = found.map((item) =>
    `<a href="${localUrl(item.url)}"><b>${item.title}</b><small>${item.url}</small></a>`
  ).join("") || `<a>没有匹配「${term}」</a>`
})
