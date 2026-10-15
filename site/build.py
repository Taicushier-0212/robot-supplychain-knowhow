"""把仓库 Markdown 生成静态文档站到 site/dist。"""

from __future__ import annotations

import base64
import html
import json
import mimetypes
import re
import shutil
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "site" / "dist"
ASSETS = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"}
SKIP_DIRS = {".git", "node_modules", "site", ".vitepress"}

J = "/knowhow/01-joint-modules"
S = "/knowhow/02-structure"
E = "/knowhow/03-electronics"

NAV = [
    ("开始", [
        ("引言", "/index.html"),
        ("分类树", "/knowhow/index.html"),
        ("G0–G5", "/docs/gates.html"),
    ]),
    ("关节模组", [
        ("总览", f"{J}/index.html"),
        ("减速机", [
            ("总览", f"{J}/reducer/index.html"),
            ("其它路径", f"{J}/reducer/other.html"),
            ("谐波", [
                ("总览", f"{J}/reducer/harmonic/index.html"),
                ("结构", f"{J}/reducer/harmonic/structure.html"),
                ("额定与寿命", f"{J}/reducer/harmonic/ratings.html"),
                ("装配与润滑", f"{J}/reducer/harmonic/assembly.html"),
            ]),
            ("行星", [
                ("总览", f"{J}/reducer/planetary/index.html"),
                ("NGW / NW", f"{J}/reducer/planetary/types.html"),
                ("齿轮与齿系", f"{J}/reducer/planetary/gears.html"),
                ("行星架", f"{J}/reducer/planetary/carrier.html"),
            ]),
            ("摆线 / RV", [
                ("总览", f"{J}/reducer/cycloidal/index.html"),
                ("结构", f"{J}/reducer/cycloidal/structure.html"),
                ("额定与刚度", f"{J}/reducer/cycloidal/ratings.html"),
                ("装配与润滑", f"{J}/reducer/cycloidal/assembly.html"),
            ]),
        ]),
        ("无框力矩电机", [
            ("总览", f"{J}/frameless-motor/index.html"),
            ("内转子", f"{J}/frameless-motor/inner-rotor.html"),
            ("外转子", f"{J}/frameless-motor/outer-rotor.html"),
            ("槽极", f"{J}/frameless-motor/slot-pole.html"),
            ("绕线", f"{J}/frameless-motor/winding.html"),
            ("磁钢", f"{J}/frameless-motor/magnet.html"),
            ("叠片 / 分瓣", f"{J}/frameless-motor/core.html"),
            ("装配", f"{J}/frameless-motor/assembly.html"),
            ("并联", f"{J}/frameless-motor/parallel.html"),
            ("霍尔", f"{J}/frameless-motor/hall.html"),
            ("温度", f"{J}/frameless-motor/thermal.html"),
        ]),
        ("编码器", f"{J}/encoder.html"),
        ("驱动器", f"{J}/driver.html"),
        ("制动器", f"{J}/brake.html"),
        ("一体化关节", f"{J}/integrated-joint.html"),
    ]),
    ("结构件", [
        ("总览", f"{S}/index.html"),
        ("CNC 机加", f"{S}/cnc.html"),
        ("机加材料", [
            ("总览", f"{S}/materials/index.html"),
            ("铝", f"{S}/materials/aluminum.html"),
            ("镁", f"{S}/materials/magnesium.html"),
            ("钢", f"{S}/materials/steel.html"),
        ]),
        ("钣金", [
            ("总览", f"{S}/sheet-metal/index.html"),
            ("折弯与展开", f"{S}/sheet-metal/bend.html"),
            ("板材", f"{S}/sheet-metal/material.html"),
            ("连接", f"{S}/sheet-metal/joining.html"),
        ]),
        ("型材", f"{S}/extrusion.html"),
        ("压铸", f"{S}/die-cast.html"),
        ("注塑", f"{S}/injection.html"),
        ("3D 打印", f"{S}/3d-print.html"),
        ("表面处理", [
            ("总览", f"{S}/surface/index.html"),
            ("阳极氧化", f"{S}/surface/anodize.html"),
            ("发黑", f"{S}/surface/black-oxide.html"),
            ("喷涂", f"{S}/surface/coating.html"),
            ("微弧氧化", f"{S}/surface/mao.html"),
        ]),
    ]),
    ("电子器件", [
        ("总览", f"{E}/index.html"),
        ("PCB / SMT", f"{E}/pcb.html"),
        ("线束", f"{E}/harness.html"),
        ("线材", [
            ("总览", f"{E}/wire/index.html"),
            ("AWG", f"{E}/wire/awg.html"),
            ("绝缘与镀层", f"{E}/wire/insulation.html"),
        ]),
        ("接插件", [
            ("总览", f"{E}/connectors/index.html"),
            ("XT30（2+2）", f"{E}/connectors/xt30.html"),
        ]),
        ("算力 / 主控", f"{E}/compute.html"),
        ("电源模块", f"{E}/power.html"),
    ]),
    ("传感器", [
        ("总览", "/knowhow/04-sensors/index.html"),
        ("力 / 力矩", "/knowhow/04-sensors/force-torque.html"),
        ("触觉", "/knowhow/04-sensors/tactile.html"),
        ("IMU", "/knowhow/04-sensors/imu.html"),
        ("视觉", "/knowhow/04-sensors/vision.html"),
    ]),
    ("能源", [
        ("总览", "/knowhow/05-energy/index.html"),
        ("电芯", "/knowhow/05-energy/cell.html"),
        ("PACK / BMS", "/knowhow/05-energy/pack.html"),
    ]),
    ("末端", [
        ("总览", "/knowhow/06-end-effector/index.html"),
        ("灵巧手", "/knowhow/06-end-effector/dexterous-hand.html"),
        ("选型对照", "/knowhow/06-end-effector/selection.html"),
    ]),
    ("标准件", [
        ("总览", "/knowhow/07-standard-parts/index.html"),
        ("轴承", "/knowhow/07-standard-parts/bearings.html"),
        ("紧固件", "/knowhow/07-standard-parts/fasteners.html"),
    ]),
    ("流程", [
        ("总览", "/docs/index.html"),
        ("铁律", "/docs/principles.html"),
        ("G0–G5", "/docs/gates.html"),
        ("自制 vs 外购", "/docs/make-vs-buy.html"),
        ("RACI", "/docs/raci.html"),
        ("质量", "/docs/quality.html"),
        ("成本与交期", "/docs/cost-leadtime.html"),
        ("风险", "/docs/risk.html"),
        ("入库纪律", "/docs/security.html"),
    ]),
    ("作业手册", [
        ("总览", "/playbooks/index.html"),
        ("寻源", "/playbooks/sourcing.html"),
        ("询价", "/playbooks/rfq.html"),
        ("供应商准入", "/playbooks/supplier-qualification.html"),
        ("首件", "/playbooks/first-article.html"),
        ("来料检验", "/playbooks/incoming-inspection.html"),
        ("不合格闭环", "/playbooks/ncr.html"),
    ]),
    ("模板", [
        ("元器件页", "/templates/component.html"),
        ("复盘卡片", "/templates/knowhow-card.html"),
    ]),
]

PAGE = """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#0b1220">
  <title>{title} · 机器人供应链</title>
  <link rel="icon" href="/logo.svg">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="/style.css">
</head>
<body>
  <header class="top">
    <button class="menu-btn" type="button">目录</button>
    <a class="brand" href="/index.html">机器人供应链</a>
    <nav>
      <a href="/knowhow/index.html">知识库</a>
      <a href="/docs/gates.html">放行门</a>
      <a href="/playbooks/index.html">作业手册</a>
    </nav>
    <div class="spacer"></div>
    <button class="search-btn" type="button">搜索 ⌘K</button>
  </header>
  <div class="shell">
    <aside class="side">{sidebar}</aside>
    <main class="content">
      <div class="crumb">{crumb}</div>
      <article class="doc">{body}</article>
      <div class="pager">{pager}</div>
    </main>
    <aside class="toc">{toc}</aside>
  </div>
  <div class="mask" hidden>
    <div class="modal">
      <input placeholder="搜索牌号、工艺、坑…" aria-label="搜索">
      <div class="hits"></div>
    </div>
  </div>
  <script src="/app.js"></script>
</body>
</html>
"""


def map_url(url: str, src: Path) -> str:
    raw = url.strip()
    if not raw or raw.startswith(("http://", "https://", "mailto:", "#")):
        return raw
    path, _, anchor = raw.partition("#")
    suffix = f"#{anchor}" if anchor else ""
    if path in ("", "/"):
        return "/index.html" + suffix
    if path.startswith("/"):
        rel = Path(path.lstrip("/"))
    else:
        try:
            rel = (src.parent / path).resolve().relative_to(ROOT)
        except ValueError:
            return raw
    s = rel.as_posix()
    ext = Path(s).suffix.lower()
    if s.endswith("README.md") or s.endswith("index.md"):
        s = s.rsplit("/", 1)[0] + "/index.html" if "/" in s else "index.html"
    elif s.endswith(".md"):
        s = s[:-3] + ".html"
    elif ext in ASSETS or s.endswith(".html"):
        pass
    elif (ROOT / s).is_dir() or (ROOT / s / "README.md").exists():
        s = s.rstrip("/") + "/index.html"
    else:
        s = s + ".html"
    return "/" + s.lstrip("/") + suffix


def rewrite(text: str, src: Path) -> str:
    def md_link(m: re.Match) -> str:
        return f"{m.group(1)}({map_url(m.group(2), src)})"

    text = re.sub(r"(\!\[[^\]]*\]|\[[^\]]*\])\(([^)\s]+)\)", md_link, text)

    def href(m: re.Match) -> str:
        url = m.group(2)
        if url.startswith(("http://", "https://", "mailto:", "#")):
            return m.group(0)
        return f"href={m.group(1)}{map_url(url, src)}{m.group(1)}"

    return re.sub(r"href=(['\"])([^'\"]+)\1", href, text)


def split_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---"):
        return "", text
    end = text.find("\n---", 3)
    if end < 0:
        return "", text
    return text[3:end], text[end + 4 :]


def slug(text: str, used: dict[str, int]) -> str:
    base = re.sub(r"\s+", "-", re.sub(r"[^\w\u4e00-\u9fff\- ]+", "", text)).strip("-").lower() or "section"
    n = used.get(base, 0)
    used[base] = n + 1
    return base if n == 0 else f"{base}-{n}"


def add_ids(body: str) -> tuple[str, list[tuple[str, str, str]]]:
    used: dict[str, int] = {}
    toc: list[tuple[str, str, str]] = []

    def repl(m: re.Match) -> str:
        level, inner = m.group(1), m.group(2)
        if " id=" in inner:
            return m.group(0)
        plain = re.sub(r"<[^>]+>", "", inner).strip()
        sid = slug(plain, used)
        if level in {"2", "3"}:
            toc.append((level, sid, plain))
        return f'<h{level} id="{sid}">{inner}</h{level}>'

    return re.sub(r"<h([1-3])>(.*?)</h\1>", repl, body, flags=re.S), toc


def out_path(md: Path) -> Path:
    rel = md.relative_to(ROOT)
    if md.name in {"README.md", "index.md"}:
        return rel.parent / "index.html"
    return rel.with_suffix(".html")


def iter_markdown() -> list[Path]:
    files = []
    for path in ROOT.rglob("*.md"):
        if any(part in SKIP_DIRS for part in path.relative_to(ROOT).parts):
            continue
        if path == ROOT / "README.md":
            continue
        files.append(path)
    return files


def flatten(nodes, crumbs=None):
    crumbs = crumbs or []
    rows = []
    for node in nodes:
        if isinstance(node[1], str):
            rows.append((node[0], node[1], crumbs))
        else:
            rows.extend(flatten(node[1], crumbs + [node[0]]))
    return rows


def render_nav(active: str) -> str:
    parts = []
    for title, items in NAV:
        open_attr = " open" if active_in(items, active) or title == "开始" else ""
        parts.append(f'<details class="group"{open_attr}><summary>{html.escape(title)}</summary><div class="nest">{render_items(items, active)}</div></details>')
    return "\n".join(parts)


def active_in(items, active: str) -> bool:
    for node in items:
        if isinstance(node[1], str):
            if node[1] == active:
                return True
        elif active_in(node[1], active):
            return True
    return False


def render_items(items, active: str) -> str:
    chunks = []
    for node in items:
        label, payload = node
        if isinstance(payload, str):
            cls = "item active" if payload == active else "item"
            chunks.append(f'<a class="{cls}" href="{payload}">{html.escape(label)}</a>')
        else:
            opened = " open" if active_in(payload, active) else ""
            chunks.append(
                f'<details class="group"{opened}><summary>{html.escape(label)}</summary>'
                f'<div class="nest">{render_items(payload, active)}</div></details>'
            )
    return "".join(chunks)


def crumb_for(active: str) -> str:
    for label, url, crumbs in flatten(NAV):
        if url == active:
            bits = ['<a href="/index.html">知识库</a>'] + [html.escape(c) for c in crumbs] + [html.escape(label)]
            return " / ".join(bits)
    return '<a href="/index.html">知识库</a>'


def toc_html(toc: list[tuple[str, str, str]]) -> str:
    if not toc:
        return ""
    links = []
    for level, sid, text in toc:
        cls = "h3" if level == "3" else "h2"
        links.append(f'<a class="{cls}" href="#{sid}">{html.escape(text)}</a>')
    return '<p class="toc-title">本页目录</p>' + "".join(links)


def data_uri(path: Path) -> str:
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode('ascii')}"


def standalone_href(url: str) -> str:
    raw = url.strip()
    if not raw or raw.startswith(("http://", "https://", "mailto:", "#", "?", "data:")):
        return raw
    path, _, anchor = raw.partition("#")
    if path.startswith("/"):
        out = f"?p={path}"
        return f"{out}#{anchor}" if anchor else out
    return raw


def standalone_html(text: str) -> str:
    def href(m: re.Match) -> str:
        return f"href={m.group(1)}{standalone_href(m.group(2))}{m.group(1)}"

    def src(m: re.Match) -> str:
        url = m.group(2)
        if url.startswith(("http://", "https://", "data:")):
            return m.group(0)
        rel = url.lstrip("/")
        candidates = [ROOT / rel, ROOT / "site" / Path(rel).name, OUT / rel]
        for file in candidates:
            if file.is_file():
                return f"src={m.group(1)}{data_uri(file)}{m.group(1)}"
        return m.group(0)

    text = re.sub(r"href=(['\"])([^'\"]+)\1", href, text)
    return re.sub(r"src=(['\"])([^'\"]+)\1", src, text)


def write_standalone(pages: dict[str, dict], search: list[dict]) -> Path:
    css = (ROOT / "site" / "style.css").read_text(encoding="utf-8")
    packed = {}
    for url, page in pages.items():
        packed[url] = {
            "title": page["title"],
            "crumb": standalone_html(page["crumb"]),
            "body": standalone_html(page["body"]),
            "pager": standalone_html(page["pager"]),
            "toc": standalone_html(page["toc"]),
            "sidebar": standalone_html(page["sidebar"]),
        }
    for item in search:
        item["url"] = standalone_href(item["url"])
    dest = ROOT / "knowhow.html"
    dest.write_text(
        STANDALONE.replace("%%CSS%%", css)
        .replace("%%PAGES%%", json.dumps(packed, ensure_ascii=False).replace("</", "<\\/"))
        .replace("%%SEARCH%%", json.dumps(search, ensure_ascii=False).replace("</", "<\\/")),
        encoding="utf-8",
    )
    return dest


STANDALONE = """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#0b1220">
  <title>机器人供应链</title>
  <style>%%CSS%%</style>
</head>
<body>
  <header class="top">
    <button class="menu-btn" type="button">目录</button>
    <a class="brand" href="?p=/index.html">机器人供应链</a>
    <nav>
      <a href="?p=/knowhow/index.html">知识库</a>
      <a href="?p=/docs/gates.html">放行门</a>
      <a href="?p=/playbooks/index.html">作业手册</a>
    </nav>
    <div class="spacer"></div>
    <button class="search-btn" type="button">搜索 Ctrl K</button>
  </header>
  <div class="shell">
    <aside class="side" id="side"></aside>
    <main class="content">
      <div class="crumb" id="crumb"></div>
      <article class="doc" id="doc"></article>
      <div class="pager" id="pager"></div>
    </main>
    <aside class="toc" id="toc"></aside>
  </div>
  <div class="mask" hidden>
    <div class="modal">
      <input placeholder="搜索牌号、工艺、坑…" aria-label="搜索">
      <div class="hits"></div>
    </div>
  </div>
  <script id="pages-data" type="application/json">%%PAGES%%</script>
  <script id="search-data" type="application/json">%%SEARCH%%</script>
  <script>
    const PAGES = JSON.parse(document.getElementById("pages-data").textContent)
    const SEARCH = JSON.parse(document.getElementById("search-data").textContent)
    const side = document.getElementById("side")
    const crumb = document.getElementById("crumb")
    const doc = document.getElementById("doc")
    const pager = document.getElementById("pager")
    const toc = document.getElementById("toc")

    function currentPath() {
      return new URLSearchParams(location.search).get("p") || "/index.html"
    }

    function render() {
      const path = currentPath()
      const page = PAGES[path] || PAGES["/index.html"]
      if (!page) return
      document.title = page.title + " · 机器人供应链"
      side.innerHTML = page.sidebar
      crumb.innerHTML = page.crumb
      doc.innerHTML = page.body
      pager.innerHTML = page.pager
      toc.innerHTML = page.toc
      window.scrollTo(0, 0)
      if (location.hash) {
        const el = document.getElementById(decodeURIComponent(location.hash.slice(1)))
        if (el) el.scrollIntoView()
      }
    }

    document.querySelector(".menu-btn").addEventListener("click", () => side.classList.toggle("open"))
    window.addEventListener("popstate", render)

    document.body.addEventListener("click", (e) => {
      const a = e.target.closest("a[href]")
      if (!a) return
      const href = a.getAttribute("href") || ""
      if (!href.startsWith("?p=")) return
      e.preventDefault()
      history.pushState(null, "", href)
      render()
    })

    const mask = document.querySelector(".mask")
    const q = document.querySelector(".modal input")
    const hits = document.querySelector(".hits")
    function openSearch() { mask.hidden = false; q.focus() }
    function closeSearch() { mask.hidden = true }
    document.querySelector(".search-btn").addEventListener("click", openSearch)
    mask.addEventListener("click", (e) => { if (e.target === mask) closeSearch() })
    document.addEventListener("keydown", (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k") {
        e.preventDefault(); openSearch()
      }
      if (e.key === "Escape") closeSearch()
    })
    q.addEventListener("input", () => {
      const term = q.value.trim().toLowerCase()
      if (term.length < 1) { hits.innerHTML = ""; return }
      const found = SEARCH.filter((item) => (item.title + item.text).toLowerCase().includes(term)).slice(0, 12)
      hits.innerHTML = found.map((item) =>
        `<a href="${item.url}"><b>${item.title}</b><small>${item.url}</small></a>`
      ).join("") || `<a>没有匹配「${term}」</a>`
    })

    render()
  </script>
</body>
</html>
"""


def pager(active: str) -> str:
    rows = flatten(NAV)
    urls = [row[1] for row in rows]
    if active not in urls:
        return ""
    i = urls.index(active)
    chunks = []
    if i > 0:
        label, url, _ = rows[i - 1]
        chunks.append(f'<a href="{url}"><small>上一页</small>{html.escape(label)}</a>')
    else:
        chunks.append("<span></span>")
    if i + 1 < len(rows):
        label, url, _ = rows[i + 1]
        chunks.append(f'<a class="next" href="{url}"><small>下一页</small>{html.escape(label)}</a>')
    return "".join(chunks)


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    shutil.copy(ROOT / "site" / "style.css", OUT / "style.css")
    shutil.copy(ROOT / "site" / "app.js", OUT / "app.js")
    shutil.copy(ROOT / "site" / "logo.svg", OUT / "logo.svg")

    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in ASSETS:
            continue
        if any(part in SKIP_DIRS for part in path.relative_to(ROOT).parts):
            continue
        dest = OUT / path.relative_to(ROOT)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(path, dest)

    md = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists"])
    search = []
    collected = {}
    pages = flatten(NAV)
    known = {url for _, url, _ in pages}

    for src in iter_markdown():
        raw = src.read_text(encoding="utf-8")
        _fm, body_md = split_frontmatter(raw)
        body_md = rewrite(body_md, src)
        md.reset()
        rendered = md.convert(body_md)
        rendered, toc = add_ids(rendered)
        title_match = re.search(r"<h1[^>]*>(.*?)</h1>", rendered, flags=re.S)
        title = re.sub(r"<[^>]+>", "", title_match.group(1)).strip() if title_match else src.stem
        rel = out_path(src).as_posix()
        url = "/" + rel
        plain = re.sub(r"<[^>]+>", " ", rendered)
        plain = re.sub(r"\s+", " ", plain).strip()
        search.append({"title": title, "url": url, "text": plain[:1200]})
        dest = OUT / out_path(src)
        dest.parent.mkdir(parents=True, exist_ok=True)
        nav_url = url if url in known else "/index.html"
        page = PAGE.format(
            title=html.escape(title),
            sidebar=render_nav(nav_url),
            crumb=crumb_for(url),
            body=rendered,
            pager=pager(url),
            toc=toc_html(toc),
        )
        dest.write_text(page, encoding="utf-8")
        collected[url] = {
            "title": title,
            "sidebar": render_nav(nav_url),
            "crumb": crumb_for(url),
            "body": rendered,
            "pager": pager(url),
            "toc": toc_html(toc),
        }

    (OUT / "search.json").write_text(json.dumps(search, ensure_ascii=False), encoding="utf-8")
    standalone = write_standalone(collected, json.loads(json.dumps(search)))
    missing = [url for url in known if not (OUT / url.lstrip("/")).exists()]
    print(f"pages {len(search)} -> {OUT}")
    print(f"standalone -> {standalone}")
    if missing:
        print("sidebar targets missing:")
        for url in missing:
            print(" ", url)


if __name__ == "__main__":
    main()
