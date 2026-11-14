import { formatRupiah, ADMIN_WHATSAPP } from "./shop-utils.js";
const categoryList=document.getElementById("home-categories");
const productGrid=document.getElementById("home-featured-products");
const fallbackImage="assets/logos/dekeku-logo-horizontal.svg";
const el=(tag,className,text)=>{const item=document.createElement(tag);if(className)item.className=className;if(text!==undefined)item.textContent=text;return item;};
function messageFor(product,category,packages){
 const lines=["Halo DEKEKU, saya ingin memesan produk berikut:","",`Produk: ${product.nama}`,`Acara: ${category.acara||"-"}`,`Tema: ${category.tema||"-"}`,"","Mohon informasi pilihan paket dan proses pemesanan selanjutnya. Terima kasih."];
 if(packages.length)lines.splice(5,0,`Pilihan paket tersedia: ${packages.map(x=>x.nama+" ("+formatRupiah(Number(x.harga))+")").join(", ")}`);
 if(product.link_produk&&/^https:\/\//i.test(product.link_produk))lines.splice(lines.length-2,0,`Preview: ${product.link_produk}`);
 return lines.join("\n");
}
function renderCategories(categories){
 categoryList.replaceChildren();
 categories.forEach(category=>{const link=el("a","home-category-link");const params=new URLSearchParams({event:category.acara,theme:category.tema});link.href=`pages/produk.html?${params.toString()}`;link.append(el("strong","",`${category.acara} · ${category.tema}`),el("span","",category.produk));categoryList.append(link);});
}
function renderProducts(products,data){
 productGrid.replaceChildren();
 products.slice(0,6).forEach(product=>{
  const category=data.kategori.find(x=>Number(x.id)===Number(product.kategori))||{};
  const packages=(Array.isArray(product.paket)?product.paket:[]).map(id=>data.paket.find(x=>Number(x.id)===Number(id))).filter(x=>x&&Number.isFinite(Number(x.harga))&&Number(x.harga)>=0);
  const card=el("article","shop-card");const image=el("img","shop-card-image");image.src=/^https:\/\//i.test(product.img||"")?product.img:fallbackImage;image.alt=product.nama;image.loading="lazy";image.decoding="async";image.onerror=()=>{image.onerror=null;image.src=fallbackImage;};
  const body=el("div","shop-card-body");body.append(el("span","shop-card-meta",[category.acara,category.tema].filter(Boolean).join(" · ")),el("h3","",product.nama),el("p","shop-card-price",packages.length?`Mulai ${formatRupiah(Math.min(...packages.map(x=>Number(x.harga))))}`:"Hubungi kami untuk harga"));
  const actions=el("div","shop-card-actions");
  if(product.link_produk&&/^https:\/\//i.test(product.link_produk)){const preview=el("a","","Preview");preview.href=product.link_produk;preview.target="_blank";preview.rel="noopener noreferrer";preview.setAttribute("aria-label",`Lihat preview ${product.nama}`);actions.append(preview);}
  const order=el("a","","Pesan");order.href=`https://wa.me/${ADMIN_WHATSAPP}?text=${encodeURIComponent(messageFor(product,category,packages))}`;order.target="_blank";order.rel="noopener noreferrer";order.setAttribute("aria-label",`Pesan ${product.nama} melalui WhatsApp`);actions.append(order);body.append(actions);card.append(image,body);productGrid.append(card);
 });
}
async function init(){try{const response=await fetch("data/produk.json",{cache:"no-cache"});if(!response.ok)throw new Error(`HTTP ${response.status}`);const data=await response.json();if(!Array.isArray(data.produk)||!Array.isArray(data.kategori)||!Array.isArray(data.paket))throw new Error("Struktur data katalog tidak valid.");renderCategories(data.kategori);renderProducts(data.produk,data);}catch(error){categoryList.replaceChildren(el("p","shop-empty","Kategori belum dapat dimuat."));productGrid.replaceChildren(el("p","shop-empty","Pilihan produk belum dapat dimuat. Silakan buka katalog lengkap."));console.error("DEKEKU featured products:",error);}}
init();
