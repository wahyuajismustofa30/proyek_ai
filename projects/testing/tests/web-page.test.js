import assert from "node:assert/strict";
import { existsSync, readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import test from "node:test";

import { isValidEmail } from "../src/app.js";

const projectRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const html = readFileSync(resolve(projectRoot, "src/index.html"), "utf8");
const css = readFileSync(resolve(projectRoot, "src/styles.css"), "utf8");

test("halaman memiliki metadata bahasa, viewport, dan judul", () => {
  assert.match(html, /<html lang="id">/);
  assert.match(html, /<meta name="viewport" content="width=device-width, initial-scale=1">/);
  assert.match(html, /<title>Testing — Web Page Lab<\/title>/);
});

test("halaman menyediakan landmark dan skip link", () => {
  assert.match(html, /<header[\s>]/);
  assert.match(html, /<main id="main-content">/);
  assert.match(html, /<footer[\s>]/);
  assert.match(html, /class="skip-link" href="#main-content"/);
});

test("semua referensi aset lokal yang dipakai halaman tersedia", () => {
  const localReferences = [...html.matchAll(/(?:src|href)="([^"]+)"/g)]
    .map((match) => match[1])
    .filter((reference) => !reference.startsWith("#") && !/^[a-z]+:/i.test(reference));

  for (const reference of localReferences) {
    assert.equal(existsSync(resolve(projectRoot, "src", reference)), true, `Aset tidak ditemukan: ${reference}`);
  }
});

test("stylesheet menyediakan breakpoint untuk layar kecil", () => {
  assert.match(css, /@media\s*\(max-width:\s*760px\)/);
  assert.match(css, /@media\s*\(max-width:\s*420px\)/);
});

test("validasi email menerima format wajar dan menolak format salah", () => {
  assert.equal(isValidEmail("nama@contoh.com"), true);
  assert.equal(isValidEmail("  nama@contoh.id  "), true);
  assert.equal(isValidEmail("bukan-email"), false);
  assert.equal(isValidEmail("nama@"), false);
  assert.equal(isValidEmail(""), false);
});
