import { readCart, saveCart, formatRupiah, updateCartBadge, MAX_QUANTITY } from "./shop-utils.js";

const grid = document.getElementById("product-grid");
const searchInput = document.getElementById("catalog-search");
const categoryFilter = document.getElementById("filter-category");
const eventFilter = document.getElementById("filter-event");
const themeFilter = document.getElementById("filter-theme");
const countLabel = document.getElementById("catalog-count");
const pagination = document.getElementById("catalog-pagination");
const dialog = document.getElementById("product-dialog");
const dialogContent = document.getElementById("product-dialog-content");
const status = document.getElementById("catalog-status");
const PER_PAGE = 12;
let products = [];
let filtered = [];
let page = 1;
let selectedProduct = null;

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
    const choose = node("button", "button button-dark button-small", "Detail & pilih paket");
    choose.type = "button";
    choose.dataset.productId = String(product.id);
    actions.append(choose);
    if (product.link_produk && /^https:\/\//i.test(product.link_produk)) {
      const preview = node("a", "button button-small", "Lihat contoh");
      preview.href = product.link_produk;
      preview.target = "_blank";
      preview.rel = "noopener noreferrer";
      actions.append(preview);
    }
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

function openProduct(product) {
  selectedProduct = product;
  dialogContent.replaceChildren();
  const close = node("button", "button button-small shop-dialog-close", "Tutup");
  close.type = "button";
  close.addEventListener("click", () => dialog.close());
  const image = node("img", "shop-dialog-image");
  image.src = /^https:\/\//i.test(product.img || "") ? product.img : "../assets/logos/dekeku-logo-horizontal.svg";
  image.alt = product.nama;
  image.onerror = () => { image.onerror = null; image.src = "../assets/logos/dekeku-logo-horizontal.svg"; };
  dialogContent.append(close, image, node("h2", "", product.nama));
  dialogContent.append(node("p", "", `Kategori: ${product.category || "-"} · Acara: ${product.event || "-"} · Tema: ${product.theme || "-"}`));
  if (product.link_produk && /^https:\/\//i.test(product.link_produk)) {
    const sample = node("a", "arrow-link", "Buka contoh produk ↗");
    sample.href = product.link_produk;
    sample.target = "_blank";
    sample.rel = "noopener noreferrer";
    dialogContent.append(sample);
  }
  if (!product.packages.length) {
    dialogContent.append(node("p", "shop-notice", "Paket untuk produk ini belum tersedia. Silakan hubungi DEKEKU."));
    dialog.showModal();
    return;
  }
  const field = node("div", "shop-field");
  const label = node("label", "", "Pilih paket");
  label.htmlFor = "selected-package";
  const select = node("select", "shop-control");
  select.id = "selected-package";
  product.packages.forEach((item) => select.add(new Option(`${item.nama} — ${formatRupiah(Number(item.harga))}`, String(item.id))));
  field.append(label, select);
  const quantityField = node("div", "shop-field");
  const quantityLabel = node("label", "", "Jumlah");
  quantityLabel.htmlFor = "selected-quantity";
  const quantity = node("input", "shop-control");
  quantity.type = "number";
  quantity.id = "selected-quantity";
  quantity.min = "1";
  quantity.max = String(MAX_QUANTITY);
  quantity.value = "1";
  quantityField.append(quantityLabel, quantity);
  const add = node("button", "button button-dark", "Tambah ke keranjang");
  add.type = "button";
  add.addEventListener("click", () => {
    const pack = product.packages.find((item) => String(item.id) === select.value);
    const qty = Number(quantity.value);
    if (!pack || !Number.isInteger(qty) || qty < 1 || qty > MAX_QUANTITY) {
      status.textContent = `Pilih paket dan jumlah 1–${MAX_QUANTITY} yang valid.`;
      return;
    }
    const cart = readCart();
    const cartId = `${product.id}:${pack.id}`;
    const existing = cart.find((item) => item.cartId === cartId);
    if (existing) existing.quantity = Math.min(MAX_QUANTITY, existing.quantity + qty);
    else cart.push({
      cartId, id: Number(product.id), productId: Number(product.id),
      nama: product.nama, name: product.nama, img: product.img || "",
      image: product.img || "", link_produk: product.link_produk || "",
      productUrl: product.link_produk || "", kategori: product.category,
      category: product.category, acara: product.event, event: product.event,
      tema: product.theme, theme: product.theme, paket_id: Number(pack.id),
      packageId: Number(pack.id), paket: pack.nama, packageName: pack.nama,
      harga: Number(pack.harga), price: Number(pack.harga), jumlah: qty, quantity: qty
    });
    saveCart(cart);
    status.textContent = `${product.nama} ditambahkan ke keranjang.`;
    dialog.close();
  });
  dialogContent.append(field, quantityField, add);
  dialog.showModal();
}

grid.addEventListener("click", (event) => {
  const button = event.target.closest("[data-product-id]");
  if (!button) return;
  const product = products.find((item) => String(item.id) === button.dataset.productId);
  if (product) openProduct(product);
});

[searchInput, categoryFilter, eventFilter, themeFilter].forEach((control) => {
  control.addEventListener(control === searchInput ? "input" : "change", applyFilters);
});

async function init() {
  updateCartBadge();
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
