export const CART_KEY = "keranjang";
export const ORDER_KEY = "order";
export const ADMIN_WHATSAPP = "6285161517176";
export const MAX_QUANTITY = 20;

export function readArray(key) {
  try {
    const value = JSON.parse(localStorage.getItem(key) || "[]");
    return Array.isArray(value) ? value : [];
  } catch {
    return [];
  }
}

export function readCart() {
  return readArray(CART_KEY).map((item) => {
    const productId = Number(item.productId ?? item.id);
    const price = Number(item.price ?? item.harga);
    const quantity = Number(item.quantity ?? item.jumlah ?? 1);
    if (!Number.isInteger(productId) || productId <= 0 || !Number.isFinite(price) || price < 0) return null;
    const packageId = Number(item.packageId ?? item.paket_id) || null;
    const packageName = String(item.packageName ?? item.paket ?? "Paket");
    return {
      cartId: String(item.cartId || `${productId}:${packageId || packageName}`),
      productId,
      id: productId,
      name: String(item.name ?? item.nama ?? "Produk DEKEKU"),
      nama: String(item.name ?? item.nama ?? "Produk DEKEKU"),
      image: String(item.image ?? item.img ?? ""),
      img: String(item.image ?? item.img ?? ""),
      productUrl: String(item.productUrl ?? item.link_produk ?? ""),
      link_produk: String(item.productUrl ?? item.link_produk ?? ""),
      category: String(item.category ?? item.kategori ?? ""),
      event: String(item.event ?? item.acara ?? ""),
      theme: String(item.theme ?? item.tema ?? ""),
      packageId,
      packageName,
      paket: packageName,
      price,
      harga: price,
      quantity: Math.min(MAX_QUANTITY, Math.max(1, Number.isInteger(quantity) ? quantity : 1)),
      jumlah: Math.min(MAX_QUANTITY, Math.max(1, Number.isInteger(quantity) ? quantity : 1))
    };
  }).filter(Boolean);
}

export function saveCart(cart) {
  localStorage.setItem(CART_KEY, JSON.stringify(cart));
  updateCartBadge(cart);
}

export function formatRupiah(value) {
  return new Intl.NumberFormat("id-ID", { style: "currency", currency: "IDR", maximumFractionDigits: 0 }).format(value);
}

export function updateCartBadge(cart = readCart()) {
  const count = cart.reduce((sum, item) => sum + item.quantity, 0);
  document.querySelectorAll("[data-cart-count]").forEach((badge) => {
    badge.textContent = String(count);
    badge.hidden = count === 0;
    badge.setAttribute("aria-label", `${count} produk di keranjang`);
  });
}
