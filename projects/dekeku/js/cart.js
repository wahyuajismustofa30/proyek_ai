import {
  readCart, saveCart, formatRupiah, updateCartBadge, MAX_QUANTITY,
  loadCatalogData, resolveCart, getCartReadIssues, hasStoredPriceMismatch
} from "./shop-utils.js";

const list = document.getElementById("cart-list");
const layout = document.getElementById("cart-layout");
const empty = document.getElementById("cart-empty");
const status = document.getElementById("cart-status");
const checkout = document.getElementById("checkout-link");
let catalog = null;
let cartItems = [];

const el = (tag, cls, text) => {
  const item = document.createElement(tag);
  if (cls) item.className = cls;
  if (text !== undefined) item.textContent = text;
  return item;
};

function render() {
  list.replaceChildren();
  empty.hidden = cartItems.length !== 0;
  layout.hidden = cartItems.length === 0;
  updateCartBadge(readCart());

  let total = 0;
  cartItems.forEach((item) => {
    const subtotal = item.price * item.quantity;
    total += subtotal;
    const card = el("article", "shop-cart-item");
    const image = el("img");
    image.src = /^https:\/\//i.test(item.image) ? item.image : "../assets/logos/dekeku-logo-horizontal.svg";
    image.alt = item.name;
    image.loading = "lazy";
    image.onerror = () => { image.onerror = null; image.src = "../assets/logos/dekeku-logo-horizontal.svg"; };
    const details = el("div");
    details.append(el("h3", "", item.name));
    details.append(el("p", "", `Paket: ${item.packageName}`));
    details.append(el("p", "", [item.event, item.theme].filter(Boolean).join(" · ") || "Produk DEKEKU"));
    details.append(el("p", "", `${formatRupiah(item.price)} per item`));
    const actions = el("div");
    const label = el("label", "", "Jumlah");
    const quantity = el("input");
    quantity.type = "number";
    quantity.min = "1";
    quantity.max = String(MAX_QUANTITY);
    quantity.step = "1";
    quantity.value = String(item.quantity);
    quantity.setAttribute("aria-label", `Jumlah ${item.name}`);
    quantity.dataset.cartQuantity = item.cartId;
    label.append(quantity);
    const remove = el("button", "button button-small", "Hapus");
    remove.type = "button";
    remove.dataset.removeCartItem = item.cartId;
    actions.append(label, remove);
    card.append(image, details, actions, el("strong", "shop-cart-price", formatRupiah(subtotal)));
    list.append(card);
  });

  const count = cartItems.reduce((sum, item) => sum + item.quantity, 0);
  document.getElementById("cart-item-count").textContent = String(count);
  document.getElementById("cart-subtotal").textContent = formatRupiah(total);
  document.getElementById("cart-total").textContent = formatRupiah(total);
  checkout.setAttribute("aria-disabled", String(cartItems.length === 0));
  checkout.href = cartItems.length ? "order.html" : "#";
}

function persist(nextCart) {
  if (!saveCart(nextCart)) {
    status.textContent = "Perubahan keranjang tidak dapat disimpan. Periksa ruang penyimpanan browser.";
    return false;
  }
  return true;
}

list.addEventListener("change", (event) => {
  const input = event.target.closest("[data-cart-quantity]");
  if (!input) return;
  const quantity = Number(input.value);
  if (!Number.isInteger(quantity) || quantity < 1 || quantity > MAX_QUANTITY) {
    status.textContent = `Jumlah harus berupa bilangan bulat antara 1 dan ${MAX_QUANTITY}.`;
    render();
    return;
  }
  const cart = readCart();
  const item = cart.find((entry) => entry.cartId === input.dataset.cartQuantity);
  if (!item) return;
  item.quantity = quantity;
  if (persist(cart)) {
    status.textContent = "Jumlah produk diperbarui.";
    cartItems = resolveCart(cart, catalog).items;
    render();
  }
});

list.addEventListener("click", (event) => {
  const button = event.target.closest("[data-remove-cart-item]");
  if (!button) return;
  const cart = readCart().filter((item) => item.cartId !== button.dataset.removeCartItem);
  if (persist(cart)) {
    cartItems = resolveCart(cart, catalog).items;
    status.textContent = "Produk dihapus dari keranjang.";
    render();
  }
});

async function init() {
  try {
    catalog = await loadCatalogData();
    const rawCart = readCart();
    const issues = getCartReadIssues();
    const { items, invalid } = resolveCart(rawCart, catalog);
    cartItems = items;
    if (issues || invalid) status.textContent = `${issues + invalid} item tidak valid atau sudah tidak tersedia dan tidak ditampilkan. Item yang masih valid tetap dipertahankan.`;
    else if (hasStoredPriceMismatch(rawCart, catalog)) status.textContent = "Harga keranjang diperbarui mengikuti harga katalog terbaru.";
    render();
  } catch (error) {
    empty.hidden = true;
    layout.hidden = true;
    status.textContent = "Harga katalog tidak dapat diverifikasi. Keranjang sementara tidak dapat digunakan; muat ulang halaman setelah katalog tersedia.";
    console.error("DEKEKU cart:", error);
  }
}

init();
