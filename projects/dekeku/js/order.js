import {
  readCart, saveCart, readArray, formatRupiah, updateCartBadge,
  ORDER_KEY, ADMIN_WHATSAPP, loadCatalogData, resolveCart,
  getCartReadIssues, getArrayReadIssues, hasStoredPriceMismatch
} from "./shop-utils.js";

const form = document.getElementById("checkout-form");
const empty = document.getElementById("order-empty");
const checkout = document.getElementById("checkout-content");
const summary = document.getElementById("order-summary");
const result = document.getElementById("checkout-result");
const sendLink = document.getElementById("whatsapp-link");
const status = document.getElementById("order-status");
const history = document.getElementById("order-history");
const clearCartButton = document.getElementById("clear-cart-after-send");
const submitButton = form.querySelector('[type="submit"]');

const el = (tag, cls, text) => {
  const item = document.createElement(tag);
  if (cls) item.className = cls;
  if (text !== undefined) item.textContent = text;
  return item;
};

let catalog = null;
let currentOrderId = null;
let submitting = false;
let resolvedItems = [];
let invalidHistoryRecords = 0;

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

function validHistoryOrder(order) {
  return order && typeof order === "object" && !Array.isArray(order) &&
    typeof order.order_id === "string" && order.order_id.length > 0 &&
    Array.isArray(order.items) && order.items.length > 0 &&
    Number.isFinite(Number(order.total)) && Number(order.total) >= 0 &&
    order.customer && typeof order.customer === "object" &&
    typeof order.customer.name === "string" &&
    typeof order.customer.phone === "string";
}

function getHistory() {
  const unique = new Map();
  invalidHistoryRecords = 0;
  readArray(ORDER_KEY).forEach((order) => {
    const validItems = validHistoryOrder(order) && order.items.every((item) =>
      item && typeof item === "object" && typeof item.name === "string" &&
      typeof item.packageName === "string" && Number.isInteger(Number(item.quantity)) &&
      Number(item.quantity) >= 1 && Number(item.quantity) <= 20 &&
      Number.isFinite(Number(item.price)) && Number(item.price) >= 0
    );
    if (validItems) unique.set(order.order_id, order);
    else invalidHistoryRecords += 1;
  });
  return [...unique.values()];
}

function saveHistory(orders) {
  try {
    localStorage.setItem(ORDER_KEY, JSON.stringify(orders));
    return true;
  } catch {
    return false;
  }
}

function renderHistory() {
  history.replaceChildren();
  const orders = getHistory().slice(-5).reverse();
  const historyIssues = getArrayReadIssues() + invalidHistoryRecords;
  if (historyIssues) history.append(el("p", "shop-notice", `${historyIssues} data riwayat tidak valid dilewati. Riwayat valid tetap dipertahankan.`));
  if (!orders.length) {
    history.append(el("p", "shop-notice", "Belum ada permintaan pesanan yang tersimpan di perangkat ini."));
    return;
  }
  orders.forEach((order) => {
    const card = el("article", "shop-order-card");
    card.append(el("strong", "", order.order_id));
    const date = new Date(order.waktu);
    card.append(el("p", "", Number.isNaN(date.getTime()) ? "Waktu tidak tersedia" : date.toLocaleString("id-ID")));
    card.append(el("p", "", `${order.items.length} jenis produk · ${formatRupiah(Number(order.total))}`));
    card.append(el("p", "", "Status lokal: menunggu konfirmasi. Ini bukan bukti pesan WhatsApp telah terkirim atau diterima DEKEKU."));
    const link = el("a", "button button-small", "Buka ulang pesan WhatsApp");
    link.href = `https://wa.me/${ADMIN_WHATSAPP}?text=${encodeURIComponent(makeMessage(order))}`;
    link.target = "_blank";
    link.rel = "noopener noreferrer";
    card.append(link);
    history.append(card);
  });
}

function renderResolvedCart() {
  const rawCart = readCart();
  const issues = getCartReadIssues();
  const resolved = resolveCart(rawCart, catalog);
  resolvedItems = resolved.items;
  updateCartBadge(rawCart);
  empty.hidden = resolvedItems.length !== 0;
  checkout.hidden = resolvedItems.length === 0;
  if (resolvedItems.length) buildSummary(resolvedItems);
  if (issues || resolved.invalid) {
    status.textContent = `${issues + resolved.invalid} item tidak valid atau sudah tidak tersedia. Item valid tetap dipertahankan.`;
  } else if (hasStoredPriceMismatch(rawCart, catalog)) {
    status.textContent = "Harga diperbarui mengikuti katalog terbaru. Periksa kembali ringkasan sebelum melanjutkan.";
  }
}

async function init() {
  try {
    catalog = await loadCatalogData();
    renderResolvedCart();
    renderHistory();
  } catch (error) {
    empty.hidden = true;
    checkout.hidden = true;
    status.textContent = "Katalog tidak dapat dimuat sehingga harga pesanan belum bisa diverifikasi. Coba muat ulang halaman.";
    console.error("DEKEKU checkout:", error);
  }
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  if (submitting) return;
  if (currentOrderId) {
    status.textContent = `Pesanan ${currentOrderId} sudah disiapkan. Gunakan tautan WhatsApp yang tersedia agar tidak membuat pesanan duplikat.`;
    return;
  }
  if (!catalog) {
    status.textContent = "Katalog belum siap. Muat ulang halaman sebelum membuat pesanan.";
    return;
  }
  if (!form.reportValidity()) return;

  const rawCart = readCart();
  const resolved = resolveCart(rawCart, catalog);
  if (!resolved.items.length || resolved.invalid || getCartReadIssues()) {
    status.textContent = "Keranjang berisi item tidak valid atau tidak tersedia. Periksa keranjang sebelum melanjutkan.";
    return;
  }
  const name = document.getElementById("customer-name").value.trim();
  const phoneRaw = document.getElementById("customer-phone").value.trim();
  const phone = phoneRaw.replace(/[^0-9+]/g, "");
  const digits = phone.replace(/\D/g, "");
  const notes = document.getElementById("customer-notes").value.trim();
  if (name.length < 2 || name.length > 100 || digits.length < 8 || digits.length > 15 || notes.length > 1000) {
    status.textContent = "Periksa kembali nama, nomor WhatsApp (8–15 digit), dan catatan pesanan.";
    return;
  }

  const previousOrder = getHistory().find((entry) => {
    const age = Date.now() - new Date(entry.waktu).getTime();
    if (!Number.isFinite(age) || age < 0 || age > 30 * 60 * 1000 ||
        entry.customer.name !== name || entry.customer.phone !== phone || entry.customer.notes !== notes ||
        !Array.isArray(entry.items) || entry.items.length !== resolved.items.length) return false;
    return resolved.items.every((item) => entry.items.some((old) =>
      Number(old.productId) === item.productId &&
      Number(old.packageId) === item.packageId &&
      Number(old.quantity) === item.quantity &&
      Number(old.price) === item.price
    ));
  });
  if (previousOrder) {
    currentOrderId = previousOrder.order_id;
    sendLink.href = `https://wa.me/${ADMIN_WHATSAPP}?text=${encodeURIComponent(makeMessage(previousOrder))}`;
    sendLink.hidden = false;
    result.hidden = false;
    status.textContent = `Pesanan ${currentOrderId} yang sama sudah disiapkan dalam 30 menit terakhir. Tautan sebelumnya digunakan kembali agar tidak membuat pesanan duplikat.`;
    return;
  }

  submitting = true;
  submitButton.disabled = true;
  try {
    const orderId = `DK-${Date.now()}-${Math.random().toString(36).slice(2, 8).toUpperCase()}`;
    const items = resolved.items.map((item) => ({ ...item }));
    const order = {
      order_id: orderId,
      items,
      total: totalOf(items),
      customer: { name, phone, notes },
      status: "menunggu_konfirmasi",
      waktu: new Date().toISOString()
    };
    const orders = getHistory();
    if (orders.some((entry) => entry.order_id === orderId)) throw new Error("ID pesanan sudah digunakan. Silakan coba lagi.");
    if (!saveHistory([...orders, order])) throw new Error("Riwayat pesanan tidak dapat disimpan. Periksa ruang penyimpanan browser.");

    currentOrderId = orderId;
    sendLink.href = `https://wa.me/${ADMIN_WHATSAPP}?text=${encodeURIComponent(makeMessage(order))}`;
    sendLink.hidden = false;
    result.hidden = false;
    clearCartButton.hidden = true;
    status.textContent = `Pesanan ${orderId} disiapkan. Buka WhatsApp lalu tekan Kirim. Pesanan belum dianggap terkirim atau diterima.`;
    renderHistory();
  } catch (error) {
    status.textContent = error.message || "Pesanan tidak dapat disiapkan.";
  } finally {
    submitting = false;
    submitButton.disabled = false;
  }
});

sendLink.addEventListener("click", () => {
  if (!currentOrderId) return;
  status.textContent = "WhatsApp dibuka. Pesan baru terkirim setelah kamu menekan tombol Kirim di WhatsApp. Setelah mengirimnya, kamu dapat mengosongkan keranjang.";
  clearCartButton.hidden = false;
});

clearCartButton.addEventListener("click", () => {
  if (!saveCart([])) {
    status.textContent = "Keranjang tidak dapat dikosongkan karena penyimpanan browser gagal.";
    return;
  }
  currentOrderId = null;
  result.hidden = true;
  sendLink.hidden = true;
  clearCartButton.hidden = true;
  status.textContent = "Keranjang dikosongkan. Status pengiriman pesan tetap belum diverifikasi oleh DEKEKU.";
  renderResolvedCart();
  renderHistory();
});

init();
