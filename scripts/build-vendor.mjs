import { build } from "esbuild";
import { cp, mkdir, readFile, readdir, rm, writeFile } from "node:fs/promises";
import path from "node:path";

const destination = "static/hugo-content/lib";
await rm(destination, { recursive: true, force: true });
await mkdir(destination, { recursive: true });
await build({
  entryPoints: { mermaid: "node_modules/mermaid/dist/mermaid.esm.mjs", zoom: "node_modules/medium-zoom/dist/medium-zoom.esm.js" },
  outdir: destination,
  bundle: true,
  splitting: true,
  format: "esm",
  platform: "browser",
  target: "es2020",
  minify: true,
  legalComments: "linked",
  chunkNames: "chunks/[name]-[hash]",
});
await cp("node_modules/mathjax/es5", `${destination}/mathjax`, { recursive: true });
const notices = [];
const lock = JSON.parse(await readFile("package-lock.json", "utf8"));
const visit = async (directory) => {
  for (const item of await readdir(directory, { withFileTypes: true })) {
    if (!item.isDirectory() || item.name.startsWith(".")) continue;
    const folder = path.join(directory, item.name);
    if (item.name.startsWith("@")) { await visit(folder); continue; }
    let manifest;
    try { manifest = JSON.parse(await readFile(path.join(folder, "package.json"), "utf8")); } catch { continue; }
    if (lock.packages[folder]?.dev) continue;
    for (const name of await readdir(folder)) {
      if (/^(license|licence|copying|notice)(\.|$)/i.test(name)) {
        try { notices.push(`${manifest.name}@${manifest.version} — ${name}\n\n${await readFile(path.join(folder, name), "utf8")}`); } catch {}
      }
    }
    try { await visit(path.join(folder, "node_modules")); } catch {}
  }
};
await visit("node_modules");
await mkdir("licenses", { recursive: true });
await writeFile("licenses/javascript-notices.txt", notices.sort().join("\n\n----------------------------------------\n\n"));
