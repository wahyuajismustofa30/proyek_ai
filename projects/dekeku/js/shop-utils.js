export const CART_KEY = "keranjang";
export const ORDER_KEY = "order";
export const ADMIN_WHATSAPP = "6285161517176";
export const MAX_QUANTITY = 20;

let invalidCartItems = 0;
let invalidArrayItems = 0;

export function readArray(key) {
  invalidArrayItems = 0;
  try {
    const value = JSON.parse(localStorage.getItem(key) || "[]");
    if (!Array.isArray(value)) {
      invalidArrayItems = 1;
      return [];
    }
    return value.filter((item) => {
      const valid = item && typeof item === "object" && !Array.isArray(item);
      if (!valid) invalidArrayItems += 1;
      return valid;
    });
  } catch {
    invalidArrayItems = 1;
    return [];
  }
}

export function getArrayReadIssues() {
  return invalidArrayItems;
}

export function getCartReadIssues() {
  return invalidCartItems;
}

export function readCart() {
  invalidCartItems = 0;
  let stored;
  try {
    stored = JSON.parse(localStorage.getItem(CART_KEY) || "[]");
  } catch {
    invalidCartItems = 1;
    return [];
  }
  if (!Array.isArray(stored)) {
    invalidCartItems = 1;
    return [];
  }

  const cart = [];
  stored.forEach((item) => {
    if (!item || typeof item !== "object" || Array.isArray(item)) {
      invalidCartItems += 1;
      return;
    }
    const productId = Number(item.productId ?? item.id);
    const packageId = Number(item.packageId ?? item.paket_id);
    const quantity = Number(item.quantity ?? item.jumlah);
    if (!Number.isInteger(productId) || productId <= 0 ||
        !Number.isInteger(packageId) || packageId <= 0 ||
        !Number.isInteger(quantity) || quantity < 1 || quantity > MAX_QUANTITY) {
      invalidCartItems += 1;
      return;
    }
    const cartId = `${productId}:${packageId}`;
    const existing = cart.find((entry) => entry.cartId === cartId);
    if (existing) {
      const combined = existing.quantity + quantity;
      if (combined > MAX_QUANTITY) {
        existing.quantity = MAX_QUANTITY;
        invalidCartItems += 1;
      } else {
        existing.quantity = combined;
      }
      return;
    }
    const storedPrice = Number(item.priceSnapshot ?? item.price ?? item.harga);
    cart.push({
      cartId, productId, packageId, quantity,
      ...(Number.isFinite(storedPrice) && storedPrice >= 0 ? { priceSnapshot: storedPrice } : {})
    });
  });
  return cart;
}

export function saveCart(cart) {
  const clean = Array.isArray(cart) ? cart
    .filter((item) => item && Number.isInteger(Number(item.productId ?? item.id)) &&
      Number(item.productId ?? item.id) > 0 &&
      Number.isInteger(Number(item.packageId ?? item.paket_id)) &&
      Number(item.packageId ?? item.paket_id) > 0 &&
      Number.isInteger(Number(item.quantity ?? item.jumlah)) &&
      Number(item.quantity ?? item.jumlah) >= 1 &&
      Number(item.quantity ?? item.jumlah) <= MAX_QUANTITY)
    .map((item) => ({
      productId: Number(item.productId ?? item.id),
      packageId: Number(item.packageId ?? item.paket_id),
      quantity: Number(item.quantity ?? item.jumlah),
      ...(Number.isFinite(Number(item.priceSnapshot ?? item.price ?? item.harga)) &&
        Number(item.priceSnapshot ?? item.price ?? item.harga) >= 0
        ? { priceSnapshot: Number(item.priceSnapshot ?? item.price ?? item.harga) } : {})
    })) : [];
  try {
    localStorage.setItem(CART_KEY, JSON.stringify(clean));
    updateCartBadge(clean);
    return true;
  } catch {
    return false;
  }
}

export async function loadCatalogData() {
  const response = await fetch("../data/produk.json", { cache: "no-cache" });
  if (!response.ok) throw new Error(`Katalog tidak dapat dimuat (HTTP ${response.status}).`);
  const data = await response.json();
  if (!data || !Array.isArray(data.produk) || !Array.isArray(data.kategori) || !Array.isArray(data.paket)) {
    throw new Error("Struktur data katalog tidak valid.");
  }
  return data;
}

export function resolveCart(cart, data) {
  const products = new Map(data.produk.map((item) => [Number(item.id), item]));
  const packages = new Map(data.paket.map((item) => [Number(item.id), item]));
  const resolved = [];
  let invalid = 0;
  cart.forEach((entry) => {
    const product = products.get(entry.productId);
    const pack = packages.get(entry.packageId);
    if (!product || !Array.isArray(product.paket) ||
        !product.paket.some((id) => Number(id) === entry.packageId) ||
        !pack || !Number.isFinite(Number(pack.harga)) || Number(pack.harga) < 0) {
      invalid += 1;
      return;
    }
    const category = data.kategori.find((item) => Number(item.id) === Number(product.kategori)) || {};
    resolved.push({
      cartId: entry.cartId,
      productId: entry.productId,
      packageId: entry.packageId,
      quantity: entry.quantity,
      name: String(product.nama || "Produk DEKEKU"),
      image: String(product.img || ""),
      productUrl: String(product.link_produk || ""),
      category: String(category.produk || ""),
      event: String(category.acara || ""),
      theme: String(category.tema || ""),
      packageName: String(pack.nama || "Paket"),
      price: Number(pack.harga)
    });
  });
  return { items: resolved, invalid };
}

export function hasStoredPriceMismatch(cart, data) {
  try {
    const stored = JSON.parse(localStorage.getItem(CART_KEY) || "[]");
    if (!Array.isArray(stored)) return false;
    const packagePrices = new Map(data.paket.map((item) => [Number(item.id), Number(item.harga)]));
    return stored.some((item) => {
      if (!item || typeof item !== "object") return false;
      const id = Number(item.packageId ?? item.paket_id);
      const oldPrice = item.priceSnapshot ?? item.price ?? item.harga;
      return oldPrice !== undefined && Number(oldPrice) !== packagePrices.get(id);
    });
  } catch {
    return false;
  }
}

export function formatRupiah(value) {
  return new Intl.NumberFormat("id-ID", { style: "currency", currency: "IDR", maximumFractionDigits: 0 }).format(value);
}

export function updateCartBadge(cart = readCart()) {
  const count = cart.reduce((sum, item) => sum + Number(item.quantity || 0), 0);
  document.querySelectorAll("[data-cart-count]").forEach((badge) => {
    badge.textContent = String(count);
    badge.hidden = count === 0;
    badge.setAttribute("aria-label", `${count} produk di keranjang`);
  });
}
