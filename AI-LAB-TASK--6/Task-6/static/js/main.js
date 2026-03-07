/**
 * Main application logic – tabs, upload, analyze, and render results.
 */
document.addEventListener("DOMContentLoaded", () => {
  // --- Element references ---
  const tabs = document.querySelectorAll(".tab");
  const tabContents = document.querySelectorAll(".tab-content");

  const btnStartCamera = document.getElementById("btn-start-camera");
  const btnCapture = document.getElementById("btn-capture");
  const btnAnalyze = document.getElementById("btn-analyze");

  const previewWebcam = document.getElementById("preview-webcam");
  const capturedImg = document.getElementById("captured-image");

  const dropZone = document.getElementById("drop-zone");
  const fileInput = document.getElementById("file-input");
  const previewUpload = document.getElementById("preview-upload");
  const uploadedImg = document.getElementById("uploaded-image");

  const loadingEl = document.getElementById("loading");
  const resultsEl = document.getElementById("results");

  let currentImageData = null; // base64 data-URI of chosen image

  // --- Tab switching ---
  tabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      tabs.forEach((t) => t.classList.remove("active"));
      tabContents.forEach((tc) => tc.classList.remove("active"));
      tab.classList.add("active");
      document.getElementById("tab-" + tab.dataset.tab).classList.add("active");
    });
  });

  // --- Webcam controls ---
  btnStartCamera.addEventListener("click", async () => {
    try {
      await Webcam.start();
      btnStartCamera.textContent = "Camera Running";
      btnStartCamera.disabled = true;
      btnCapture.disabled = false;
    } catch (err) {
      alert("Could not access camera: " + err.message);
    }
  });

  btnCapture.addEventListener("click", () => {
    const dataUrl = Webcam.capture();
    if (!dataUrl) return;
    currentImageData = dataUrl;
    capturedImg.src = dataUrl;
    previewWebcam.style.display = "block";
    btnAnalyze.disabled = false;
  });

  // --- File upload / drag-and-drop ---
  dropZone.addEventListener("click", () => fileInput.click());
  dropZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZone.classList.add("drag-over");
  });
  dropZone.addEventListener("dragleave", () =>
    dropZone.classList.remove("drag-over"),
  );
  dropZone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropZone.classList.remove("drag-over");
    handleFile(e.dataTransfer.files[0]);
  });
  fileInput.addEventListener("change", () => {
    if (fileInput.files.length) handleFile(fileInput.files[0]);
  });

  function handleFile(file) {
    if (!file || !file.type.startsWith("image/")) return;
    const reader = new FileReader();
    reader.onload = (e) => {
      currentImageData = e.target.result;
      uploadedImg.src = currentImageData;
      previewUpload.style.display = "block";
      btnAnalyze.disabled = false;
    };
    reader.readAsDataURL(file);
  }

  // --- Analyze ---
  btnAnalyze.addEventListener("click", async () => {
    if (!currentImageData) return;
    loadingEl.style.display = "block";
    resultsEl.style.display = "none";

    try {
      const resp = await fetch("/api/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ image: currentImageData }),
      });

      const data = await resp.json();
      loadingEl.style.display = "none";

      if (!data.success) {
        alert(data.message || data.error || "Analysis failed");
        return;
      }

      renderResults(data);
      resultsEl.style.display = "block";
      resultsEl.scrollIntoView({ behavior: "smooth" });
    } catch (err) {
      loadingEl.style.display = "none";
      alert("Error: " + err.message);
    }
  });

  // --- Render results ---
  function renderResults(data) {
    const p = data.personality;

    // Type header
    document.getElementById("result-type").textContent =
      p.type + " — " + p.name;
    document.getElementById("result-description").textContent = p.description;
    document.getElementById("result-confidence").textContent = p.confidence;

    // Dimension bars
    const dimContainer = document.getElementById("result-dimensions");
    dimContainer.innerHTML = "";
    const dimLabels = [
      ["E", "I", p.dimension_scores.E_vs_I],
      ["S", "N", p.dimension_scores.S_vs_N],
      ["T", "F", p.dimension_scores.T_vs_F],
      ["J", "P", p.dimension_scores.J_vs_P],
    ];
    dimLabels.forEach(([l, r, val]) => {
      dimContainer.innerHTML += `
                <div class="dim-row">
                    <span class="dim-label">${l}</span>
                    <div class="dim-bar"><div class="dim-fill" style="width:${val}%"></div></div>
                    <span class="dim-label">${r}</span>
                    <span class="dim-val">${val}%</span>
                </div>`;
    });

    // Strengths / Challenges
    fillList("result-strengths", p.strengths);
    fillList("result-challenges", p.challenges);

    // Recommendations
    fillList("result-recommendations", data.recommendations);

    // Feature summary chips
    const featEl = document.getElementById("result-features");
    featEl.innerHTML = "";
    for (const [k, v] of Object.entries(data.feature_summary)) {
      featEl.innerHTML += `<div class="feature-chip">${formatLabel(k)}: <span>${v}</span></div>`;
    }

    // Measurements table
    const tbody = document.querySelector("#result-measurements tbody");
    tbody.innerHTML = "";
    for (const [k, v] of Object.entries(data.normalized_measurements)) {
      const row = tbody.insertRow();
      row.insertCell().textContent = formatLabel(k);
      row.insertCell().textContent = v;
    }
  }

  function fillList(id, arr) {
    const ul = document.getElementById(id);
    ul.innerHTML = "";
    arr.forEach((item) => {
      const li = document.createElement("li");
      li.textContent = item;
      ul.appendChild(li);
    });
  }

  function formatLabel(key) {
    return key.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
  }
});
