import { readCart, saveCart, formatRupiah, updateCartBadge, MAX_QUANTITY } from "./shop-utils.js";

const list = document.getElementById("cart-list");
const layout = document.getElementById("cart-layout");
const empty = document.getElementById("cart-empty");
const status = document.getElementById("cart-status");
const checkout = document.getElementById("checkout-link");

const el = (tag, cls, text) => {
  const item = document.createElement(tag);
  if (cls) item.className = cls;
  if (text !== undefined) item.textContent = text;
  return item;
};

function render() {
  const cart = readCart();
  list.replaceChildren();
  empty.hidden = cart.length !== 0;
  layout.hidden = cart.length === 0;
  updateCartBadge(cart);

  let total = 0;
  cart.forEach((item) => {
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
    const price = el("strong", "shop-cart-price", formatRupiah(subtotal));
    card.append(image, details, actions, price);
    list.append(card);
  });

  const count = cart.reduce((sum, item) => sum + item.quantity, 0);
  document.getElementById("cart-item-count").textContent = String(count);
  document.getElementById("cart-subtotal").textContent = formatRupiah(total);
  document.getElementById("cart-total").textContent = formatRupiah(total);
  checkout.setAttribute("aria-disabled", String(cart.length === 0));
}

list.addEventListener("change", (event) => {
  const input = event.target.closest("[data-cart-quantity]");
  if (!input) return;
  const quantity = Number(input.value);
  if (!Number.isInteger(quantity) || quantity < 1 || quantity > MAX_QUANTITY) {
    status.textContent = `Jumlah harus antara 1 dan ${MAX_QUANTITY}.`;
    render();
    return;
  }
  const cart = readCart();
  const item = cart.find((entry) => entry.cartId === input.dataset.cartQuantity);
  if (!item) return;
  item.quantity = quantity;
  item.jumlah = quantity;
  saveCart(cart);
  status.textContent = "Jumlah produk diperbarui.";
  render();
});

list.addEventListener("click", (event) => {
  const button = event.target.closest("[data-remove-cart-item]");
  if (!button) return;
  saveCart(readCart().filter((item) => item.cartId !== button.dataset.removeCartItem));
  status.textContent = "Produk dihapus dari keranjang.";
  render();
});

render();
