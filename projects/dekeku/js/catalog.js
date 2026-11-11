import { formatRupiah, ADMIN_WHATSAPP } from "./shop-utils.js";

const grid = document.getElementById("product-grid");
const searchInput = document.getElementById("catalog-search");
const categoryFilter = document.getElementById("filter-category");
const eventFilter = document.getElementById("filter-event");
const themeFilter = document.getElementById("filter-theme");
const countLabel = document.getElementById("catalog-count");
const pagination = document.getElementById("catalog-pagination");
const status = document.getElementById("catalog-status");
const PER_PAGE = 12;
let products = [];
let filtered = [];
let page = 1;

const node = (tag, className, value) => {
  const element = document.createElement(tag);
  if (className) element.className = className;
  if (value !== undefined) element.textContent = value;
  return element;
};

function packagesFor(product, data) {
  const lookup = new Map(data.paket.map((item) => [Number(item.id), item]));
  return (Array.isArray(product.paket) ? product.paket : [])
    .map((id) => lookup.get(Number(id)))
    .filter((item) => item && Number.isFinite(Number(item.harga)) && Number(item.harga) >= 0);
}

function enrichProduct(product, data) {
  const category = data.kategori.find((item) => Number(item.id) === Number(product.kategori)) || {};
  return {
    ...product,
    category: category.produk || "",
    event: category.acara || "",
    theme: category.tema || "",
    packages: packagesFor(product, data)
  };
}

function fillFilter(select, values, label) {
  const current = select.value;
  select.replaceChildren(new Option(`Semua ${label}`, ""));
  [...new Set(values.filter(Boolean))].sort((a, b) => a.localeCompare(b, "id")).forEach((value) => {
    select.add(new Option(value.charAt(0).toUpperCase() + value.slice(1), value));
  });
  if ([...select.options].some((option) => option.value === current)) select.value = current;
}

function orderMessage(product) {
  const lines = [
    "Halo DEKEKU, saya ingin memesan produk berikut:",
    "",
    `Produk: ${product.nama}`,
    `Kategori: ${product.category || "-"}`,
    `Acara: ${product.event || "-"}`,
    `Tema: ${product.theme || "-"}`,
    "",
    "Pilihan paket:"
  ];
  if (product.packages.length) {
    product.packages.forEach((pack, index) => {
      lines.push(`${index + 1}. ${pack.nama} — ${formatRupiah(Number(pack.harga))}`);
    });
    lines.push("", "Saya ingin memilih paket nomor: ");
  } else {
    lines.push("Mohon informasikan pilihan paket dan harganya.");
  }
  if (product.link_produk && /^https:\/\//i.test(product.link_produk)) {
    lines.push("", `Preview: ${product.link_produk}`);
  }
  lines.push("", "Mohon informasi proses pemesanan selanjutnya. Terima kasih.");
  return lines.join("\n");
}

function iconLink(label, path, className = "shop-icon-action") {
  const link = node("a", className);
  link.setAttribute("aria-label", label);
  link.title = label;
  link.innerHTML = path;
  return link;
}

function applyFilters() {
  const query = searchInput.value.trim().toLocaleLowerCase("id");
  filtered = products.filter((product) => {
    const textMatch = !query || product.nama.toLocaleLowerCase("id").includes(query);
    return textMatch &&
      (!categoryFilter.value || product.category === categoryFilter.value) &&
      (!eventFilter.value || product.event === eventFilter.value) &&
      (!themeFilter.value || product.theme === themeFilter.value);
  });
  page = 1;
  renderProducts();
}

function renderProducts() {
  grid.replaceChildren();
  const start = (page - 1) * PER_PAGE;
  const visible = filtered.slice(start, start + PER_PAGE);
  countLabel.textContent = `Menampilkan ${visible.length} dari ${filtered.length} produk`;

  if (!visible.length) {
    grid.append(node("p", "shop-empty", "Produk tidak ditemukan. Coba ubah kata pencarian atau filter."));
  }

  visible.forEach((product) => {
    const card = node("article", "shop-card");
    const image = node("img", "shop-card-image");
    image.src = /^https:\/\//i.test(product.img || "") ? product.img : "../assets/logos/dekeku-logo-horizontal.svg";
    image.alt = product.nama;
    image.loading = "lazy";
    image.onerror = () => { image.onerror = null; image.src = "../assets/logos/dekeku-logo-horizontal.svg"; };

    const body = node("div", "shop-card-body");
    body.append(node("span", "shop-card-meta", [product.event, product.theme].filter(Boolean).join(" · ") || product.category));
    body.append(node("h3", "", product.nama));
    const prices = product.packages.map((item) => Number(item.harga)).filter(Number.isFinite);
    body.append(node("p", "shop-card-price", prices.length ? `Mulai ${formatRupiah(Math.min(...prices))}` : "Hubungi kami untuk harga"));

    const actions = node("div", "shop-card-actions");
    if (product.link_produk && /^https:\/\//i.test(product.link_produk)) {
      const preview = iconLink("Lihat preview produk", '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12Z"/><circle cx="12" cy="12" r="3"/></svg>');
      preview.href = product.link_produk;
      preview.target = "_blank";
      preview.rel = "noopener noreferrer";
      actions.append(preview);
    }

    const order = iconLink("Pesan produk melalui WhatsApp", '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 3h2l2.2 12.2a2 2 0 0 0 2 1.6h8.9a2 2 0 0 0 1.9-1.4L22 8H6"/><circle cx="10" cy="21" r="1"/><circle cx="18" cy="21" r="1"/></svg>');
    order.href = `https://wa.me/${ADMIN_WHATSAPP}?text=${encodeURIComponent(orderMessage(product))}`;
    order.target = "_blank";
    order.rel = "noopener noreferrer";
    actions.append(order);

    body.append(actions);
    card.append(image, body);
    grid.append(card);
  });

  const pages = Math.ceil(filtered.length / PER_PAGE);
  pagination.replaceChildren();
  if (pages > 1) {
    const previous = node("button", "button button-small", "Sebelumnya");
    previous.type = "button";
    previous.disabled = page === 1;
    previous.addEventListener("click", () => { page -= 1; renderProducts(); });
    const label = node("span", "", `Halaman ${page} dari ${pages}`);
    const next = node("button", "button button-small", "Berikutnya");
    next.type = "button";
    next.disabled = page === pages;
    next.addEventListener("click", () => { page += 1; renderProducts(); });
    pagination.append(previous, label, next);
  }
}

[searchInput, categoryFilter, eventFilter, themeFilter].forEach((control) => {
  control.addEventListener(control === searchInput ? "input" : "change", applyFilters);
});

async function init() {
  try {
    const response = await fetch("../data/produk.json", { cache: "no-cache" });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    if (!Array.isArray(data.produk) || !Array.isArray(data.kategori) || !Array.isArray(data.paket)) {
      throw new Error("Struktur data katalog tidak valid.");
    }
    products = data.produk.map((item) => enrichProduct(item, data));
    fillFilter(categoryFilter, products.map((item) => item.category), "kategori");
    fillFilter(eventFilter, products.map((item) => item.event), "acara");
    fillFilter(themeFilter, products.map((item) => item.theme), "tema");
    applyFilters();
  } catch (error) {
    grid.replaceChildren(node("p", "shop-empty", "Katalog belum dapat dimuat. Silakan muat ulang halaman atau hubungi DEKEKU."));
    countLabel.textContent = "Katalog tidak tersedia";
    console.error("DEKEKU catalogue:", error);
  }
}

init();
