import { readCart, saveCart, readArray, formatRupiah, updateCartBadge, ORDER_KEY, ADMIN_WHATSAPP } from "./shop-utils.js";

const form = document.getElementById("checkout-form");
const empty = document.getElementById("order-empty");
const checkout = document.getElementById("checkout-content");
const summary = document.getElementById("order-summary");
const result = document.getElementById("checkout-result");
const sendLink = document.getElementById("whatsapp-link");
const status = document.getElementById("order-status");
const history = document.getElementById("order-history");

const el = (tag, cls, text) => {
  const item = document.createElement(tag);
  if (cls) item.className = cls;
  if (text !== undefined) item.textContent = text;
  return item;
};

let currentOrderId = null;

function totalOf(items) {
  return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
}

function makeMessage(order) {
  const lines = [
    "*PERMINTAAN PESANAN DEKEKU*",
    `ID Pesanan: ${order.order_id}`,
    "",
    `Nama: ${order.customer.name}`,
    `WhatsApp pelanggan: ${order.customer.phone}`,
    order.customer.notes ? `Catatan: ${order.customer.notes}` : "",
    "",
    "*RINCIAN PRODUK*"
  ];
  order.items.forEach((item, index) => {
    lines.push(
      `${index + 1}. ${item.name}`,
      `   Paket: ${item.packageName}`,
      `   Jumlah: ${item.quantity}`,
      `   Harga: ${formatRupiah(item.price)}`,
      `   Subtotal: ${formatRupiah(item.price * item.quantity)}`
    );
    if (item.productUrl) lines.push(`   Contoh: ${item.productUrl}`);
  });
  lines.push("", `*TOTAL: ${formatRupiah(order.total)}*`, "", "Mohon konfirmasi ketersediaan dan langkah pemesanan berikutnya. Terima kasih.");
  return lines.filter(Boolean).join("\n");
}

function buildSummary(items) {
  summary.replaceChildren();
  items.forEach((item) => {
    const row = el("div", "shop-summary-line");
    row.append(el("span", "", `${item.name} · ${item.packageName} × ${item.quantity}`));
    row.append(el("strong", "", formatRupiah(item.price * item.quantity)));
    summary.append(row);
  });
  const total = el("div", "shop-summary-line shop-summary-total");
  total.append(el("span", "", "Total"));
  total.append(el("strong", "", formatRupiah(totalOf(items))));
  summary.append(total);
}

function renderHistory() {
  history.replaceChildren();
  const orders = readArray(ORDER_KEY).slice(-5).reverse();
  if (!orders.length) {
    history.append(el("p", "shop-notice", "Belum ada permintaan pesanan yang disimpan di perangkat ini."));
    return;
  }
  orders.forEach((order) => {
    const card = el("article", "shop-order-card");
    card.append(el("strong", "", order.order_id));
    card.append(el("p", "", new Date(order.waktu).toLocaleString("id-ID")));
    card.append(el("p", "", `${order.items.length} jenis produk · ${formatRupiah(order.total)}`));
    card.append(el("p", "", "Status lokal: menunggu konfirmasi. Status ini bukan bukti bahwa pesan WhatsApp telah terkirim atau pembayaran telah diterima."));
    const link = el("a", "button button-small", "Buka ulang pesan WhatsApp");
    link.href = `https://wa.me/${ADMIN_WHATSAPP}?text=${encodeURIComponent(makeMessage(order))}`;
    link.target = "_blank";
    link.rel = "noopener noreferrer";
    card.append(link);
    history.append(card);
  });
}

function init() {
  const cart = readCart();
  updateCartBadge(cart);
  empty.hidden = cart.length !== 0;
  checkout.hidden = cart.length === 0;
  if (cart.length) buildSummary(cart);
  renderHistory();
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const cart = readCart();
  if (!cart.length) {
    status.textContent = "Keranjang kosong. Pilih produk sebelum membuat pesanan.";
    init();
    return;
  }
  if (!form.reportValidity()) return;

  const name = document.getElementById("customer-name").value.trim();
  const phoneRaw = document.getElementById("customer-phone").value.trim();
  const phone = phoneRaw.replace(/[^0-9+]/g, "");
  const digits = phone.replace(/\D/g, "");
  const notes = document.getElementById("customer-notes").value.trim();
  if (name.length < 2 || digits.length < 8 || digits.length > 15) {
    status.textContent = "Periksa kembali nama dan nomor WhatsApp (8–15 digit).";
    return;
  }

  const order = {
    order_id: `DK-${Date.now()}`,
    items: cart,
    total: totalOf(cart),
    customer: { name, phone, notes },
    status: "menunggu_konfirmasi",
    waktu: new Date().toISOString()
  };
  const orders = readArray(ORDER_KEY);
  orders.push(order);
  try {
    localStorage.setItem(ORDER_KEY, JSON.stringify(orders));
  } catch {
    status.textContent = "Pesanan tidak dapat disimpan di perangkat. Periksa ruang penyimpanan browser.";
    return;
  }
  currentOrderId = order.order_id;
  sendLink.href = `https://wa.me/${ADMIN_WHATSAPP}?text=${encodeURIComponent(makeMessage(order))}`;
  sendLink.hidden = false;
  result.hidden = false;
  status.textContent = `Ringkasan ${order.order_id} siap. Lanjutkan dengan membuka WhatsApp dan menekan tombol Kirim.`;
  renderHistory();
});

sendLink.addEventListener("click", () => {
  if (!currentOrderId) return;
  const orders = readArray(ORDER_KEY);
  const order = orders.find((item) => item.order_id === currentOrderId);
  if (order) {
    order.whatsapp_opened_at = new Date().toISOString();
    order.status = "menunggu_konfirmasi";
    localStorage.setItem(ORDER_KEY, JSON.stringify(orders));
  }
  saveCart([]);
  currentOrderId = null;
  status.textContent = "WhatsApp dibuka. Pesan baru terkirim setelah kamu menekan tombol Kirim di aplikasi WhatsApp.";
  sendLink.hidden = true;
  renderHistory();
});

init();
