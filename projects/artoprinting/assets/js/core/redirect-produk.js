// redirect-produk.js — dipakai /produk.html (alamat lama detail produk).
// /produk.html?p=Mug&id=3  ->  /laman/produk/?p=Mug&id=3
location.replace('/laman/produk/' + location.search + location.hash);
