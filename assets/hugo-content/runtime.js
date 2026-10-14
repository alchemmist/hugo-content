(() => {
  const settings = document.currentScript.dataset;
  const containers = [...document.querySelectorAll(".hc-content")];
  const loadScript = (url) => new Promise((resolve, reject) => {
    const script = document.createElement("script");
    script.src = url;
    script.onload = resolve;
    script.onerror = () => reject(new Error(`Unable to load ${url}`));
    document.head.append(script);
  });
  const report = (feature, error) => {
    console.error(`hugo-content: ${feature}`, error);
  };

  const images = [...document.querySelectorAll(".hc-content img:not(.no-zoom), [data-content-zoom] img:not(.no-zoom)")];
  if (settings.zoom && images.length) {
    import(settings.zoom).then(({ default: mediumZoom }) => {
      images.forEach((image) => image.classList.add("hc-zoom-image"));
      const zoom = mediumZoom(images, {
        background: "rgba(0, 0, 0, 0.7)",
        margin: window.innerWidth < 868 ? 25 : 50,
        scrollOffset: 50,
      });
      zoom.on("open", () => { document.body.dataset.hcZoomActive = ""; });
      zoom.on("closed", () => { delete document.body.dataset.hcZoomActive; });
      window.addEventListener("resize", () => zoom.update({ margin: window.innerWidth < 868 ? 25 : 50 }));
    }).catch((error) => report("image zoom", error));
  }

  if (settings.mermaid) {
    import(settings.mermaid).then(async ({ default: mermaid }) => {
      mermaid.initialize({
        startOnLoad: false,
        securityLevel: "strict",
        theme: "base",
        flowchart: { useMaxWidth: false },
        sequence: { useMaxWidth: false },
        gitGraph: { useMaxWidth: false },
      });
      for (const node of document.querySelectorAll(".hc-content .mermaid")) {
        const source = node.textContent;
        try {
          await mermaid.run({ nodes: [node] });
        } catch (error) {
          node.replaceChildren(document.createTextNode(source));
          node.classList.add("hc-error");
          report("diagram", error);
        }
      }
    }).catch((error) => report("diagrams", error));
  }

  if (settings.math && containers.length) {
    window.MathJax = {
      tex: { displayMath: [["$$", "$$"], ["\\[", "\\]"]], inlineMath: [["$", "$"], ["\\(", "\\)"]] },
      loader: { paths: { mathjax: settings.math }, load: ["ui/safe"] },
      svg: { fontCache: "local" },
      options: { enableMenu: false },
      startup: { typeset: false },
    };
    loadScript(`${settings.math}/tex-svg.js`)
      .then(() => window.MathJax.startup.promise)
      .then(() => window.MathJax.typesetPromise(containers))
      .catch((error) => report("mathematics", error));
  }
})();
