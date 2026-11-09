import assert from "node:assert/strict";
import { existsSync, readFileSync } from "node:fs";
import { dirname, resolve, sep } from "node:path";
import { fileURLToPath } from "node:url";
import test from "node:test";

import { initializePage, isValidEmail } from "../src/app.js";

const projectRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const sourceRoot = resolve(projectRoot, "src");
const html = readFileSync(resolve(sourceRoot, "index.html"), "utf8");
const css = readFileSync(resolve(sourceRoot, "styles.css"), "utf8");

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

test("URL aset lokal dipetakan ke file di bawah document root src", () => {
  const localReferences = [...html.matchAll(/(?:src|href)="([^"]+)"/g)]
    .map((match) => match[1])
    .filter((reference) => !reference.startsWith("#") && !/^[a-z]+:/i.test(reference));

  for (const reference of localReferences) {
    const requestUrl = new URL(reference, "http://localhost/");
    assert.equal(requestUrl.origin, "http://localhost", `Referensi bukan aset lokal: ${reference}`);
    const pathname = decodeURIComponent(requestUrl.pathname);
    const assetPath = resolve(sourceRoot, `.${pathname}`);
    assert.ok(assetPath.startsWith(sourceRoot + sep), `Path keluar dari document root: ${reference}`);
    assert.equal(existsSync(assetPath), true, `File tidak ditemukan pada document root: ${reference} -> ${pathname}`);
  }
});

test("stylesheet menyediakan breakpoint mobile dan progressive enhancement", () => {
  assert.match(css, /@media\s*\(max-width:\s*760px\)/);
  assert.match(css, /@media\s*\(max-width:\s*420px\)/);
  assert.match(css, /\.js \.primary-nav\s*\{\s*display:\s*none;/);
  assert.match(css, /\.js \.menu-toggle\s*\{\s*display:\s*inline-flex;/);
});

test("validasi email menerima format wajar dan menolak domain yang rusak", () => {
  assert.equal(isValidEmail("nama@contoh.com"), true);
  assert.equal(isValidEmail("  nama@sub.contoh.id  "), true);
  for (const value of ["bukan-email", "nama@", "", "a@.com", "a@b..com", "a..b@example.com", "@example.com", "a b@example.com"]) {
    assert.equal(isValidEmail(value), false, `Seharusnya ditolak: ${value}`);
  }
});

function makeElement() {
  const listeners = new Map();
  const attributes = new Map([["aria-expanded", "false"]]);
  const classes = new Set();
  return {
    value: "",
    textContent: "",
    dataset: {},
    focused: false,
    resetCalled: false,
    addEventListener(type, callback) { listeners.set(type, callback); },
    dispatch(type, event = {}) {
      let defaultPrevented = false;
      listeners.get(type)?.({ preventDefault() { defaultPrevented = true; }, ...event });
      this.lastDefaultPrevented = defaultPrevented;
    },
    getAttribute(name) { return attributes.get(name) ?? null; },
    setAttribute(name, value) { attributes.set(name, value); },
    focus() { this.focused = true; },
    reset() { this.resetCalled = true; },
    classList: {
      add(name) { classes.add(name); },
      remove(name) { classes.delete(name); },
      toggle(name, force) {
        const shouldAdd = force ?? !classes.has(name);
        if (shouldAdd) classes.add(name);
        else classes.delete(name);
        return shouldAdd;
      },
      contains(name) { return classes.has(name); },
    },
    listeners,
  };
}

function makePage() {
  const menuButton = makeElement();
  const navigation = makeElement();
  const navLink = makeElement();
  navigation.querySelectorAll = () => [navLink];
  const form = makeElement();
  const submitButton = makeElement();
  submitButton.disabled = true;
  form.querySelector = () => submitButton;
  const emailInput = makeElement();
  const message = makeElement();
  const documentRef = {
    documentElement: makeElement(),
    querySelector(selector) {
      return ({
        ".menu-toggle": menuButton,
        "#primary-nav": navigation,
        "#demo-form": form,
        "#email": emailInput,
        "#form-message": message,
      })[selector] ?? null;
    },
  };
  initializePage(documentRef);
  return { documentRef, menuButton, navigation, navLink, form, submitButton, emailInput, message };
}

test("menu mobile menyinkronkan aria-expanded dan status navigasi", () => {
  const page = makePage();
  page.menuButton.dispatch("click");
  assert.equal(page.menuButton.getAttribute("aria-expanded"), "true");
  assert.equal(page.navigation.classList.contains("is-open"), true);
  page.menuButton.dispatch("click");
  assert.equal(page.menuButton.getAttribute("aria-expanded"), "false");
  assert.equal(page.navigation.classList.contains("is-open"), false);
});

test("memilih tautan navigasi menutup menu", () => {
  const page = makePage();
  page.menuButton.dispatch("click");
  page.navLink.dispatch("click");
  assert.equal(page.menuButton.getAttribute("aria-expanded"), "false");
  assert.equal(page.navigation.classList.contains("is-open"), false);
});

test("form hanya aktif setelah JavaScript memasang handler submit", () => {
  assert.match(html, /<button[^>]*type="submit"[^>]*disabled/);
  const page = makePage();
  assert.equal(page.submitButton.disabled, false);
  assert.equal(page.documentRef.documentElement.classList.contains("js"), true);
});

test("form menampilkan error dan mempertahankan input yang tidak valid", () => {
  const page = makePage();
  page.emailInput.value = "a@.com";
  page.form.dispatch("submit");
  assert.equal(page.message.dataset.state, "error");
  assert.match(page.message.textContent, /Format email belum tepat/);
  assert.equal(page.emailInput.focused, true);
  assert.equal(page.form.resetCalled, false);
  assert.equal(page.form.lastDefaultPrevented, true);
});

test("form menampilkan sukses dan reset hanya untuk email valid", () => {
  const page = makePage();
  page.emailInput.value = "nama@contoh.com";
  page.form.dispatch("submit");
  assert.equal(page.message.dataset.state, "success");
  assert.match(page.message.textContent, /tidak ada data yang dikirim/);
  assert.equal(page.form.resetCalled, true);
  assert.equal(page.form.lastDefaultPrevented, true);
});
