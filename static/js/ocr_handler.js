/**
 * Medical Report OCR Handler & Interactive Biomarker Visualizer
 */

class OCRHandler {
  static init() {
    this.dropZone = document.getElementById('drop-zone');
    this.fileInput = document.getElementById('report-file-input');
    this.previewImg = document.getElementById('preview-image');
    this.previewContainer = document.getElementById('preview-container');
    this.scanBtn = document.getElementById('btn-run-scan');
    this.scannerBox = document.getElementById('scanner-box');
    this.resultsCard = document.getElementById('ocr-results-card');
    this.biomarkersTableBody = document.getElementById('biomarkers-table-body');
    this.scanStatusText = document.getElementById('scan-status-text');

    this.selectedFile = null;
    this.activePreset = null;

    this.bindEvents();
  }

  static bindEvents() {
    if (!this.dropZone) return;

    // Drag & Drop
    ['dragenter', 'dragover'].forEach(name => {
      this.dropZone.addEventListener(name, (e) => {
        e.preventDefault();
        this.dropZone.classList.add('border-teal-500', 'bg-teal-50');
      });
    });

    ['dragleave', 'drop'].forEach(name => {
      this.dropZone.addEventListener(name, (e) => {
        e.preventDefault();
        this.dropZone.classList.remove('border-teal-500', 'bg-teal-50');
      });
    });

    this.dropZone.addEventListener('drop', (e) => {
      if (e.dataTransfer.files && e.dataTransfer.files[0]) {
        this.handleFile(e.dataTransfer.files[0]);
      }
    });

    this.fileInput.addEventListener('change', (e) => {
      if (e.target.files && e.target.files[0]) {
        this.handleFile(e.target.files[0]);
      }
    });

    // Preset buttons
    document.querySelectorAll('.preset-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const preset = btn.getAttribute('data-preset');
        this.loadPreset(preset);
      });
    });

    // Run Scan Button
    if (this.scanBtn) {
      this.scanBtn.addEventListener('click', () => {
        this.executeOCRScan();
      });
    }
  }

  static handleFile(file) {
    this.selectedFile = file;
    this.activePreset = null;

    const reader = new FileReader();
    reader.onload = (e) => {
      this.previewImg.src = e.target.result;
      this.previewContainer.classList.remove('hidden');
      this.dropZone.classList.add('hidden');
    };
    reader.readAsDataURL(file);
    showToast(`Loaded ${file.name}`, 'info');
  }

  static loadPreset(presetKey) {
    this.activePreset = presetKey;
    this.selectedFile = null;

    const presetLabels = {
      cbc: "Complete Blood Count (CBC)",
      diabetes: "Diabetic & Metabolic Panel",
      lipid: "Lipid & Cardiovascular Panel",
      rft: "Renal & Kidney Function (RFT)",
      thyroid: "Thyroid Stimulating Hormone (TSH)"
    };

    // Load sample report preview image
    this.previewImg.src = "/static/images/sample_report.jpg";
    this.previewContainer.classList.remove('hidden');
    this.dropZone.classList.add('hidden');

    showToast(`Selected Preset: ${presetLabels[presetKey] || presetKey}`, 'info');
    // Automatically trigger scan for convenience
    this.executeOCRScan();
  }

  static resetFile() {
    this.selectedFile = null;
    this.activePreset = null;
    if (this.fileInput) this.fileInput.value = '';
    this.previewContainer.classList.add('hidden');
    this.dropZone.classList.remove('hidden');
    this.resultsCard.classList.add('hidden');
  }

  static executeOCRScan() {
    if (!this.selectedFile && !this.activePreset) {
      // Default to diabetic preset if nothing chosen
      this.activePreset = 'diabetes';
      this.previewImg.src = "/static/images/sample_report.jpg";
      this.previewContainer.classList.remove('hidden');
      this.dropZone.classList.add('hidden');
    }

    // Activate laser scanner animation
    this.scannerBox.classList.add('scanner-active');
    this.scanBtn.disabled = true;
    this.scanBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin mr-2"></i> Analyzing Document...';
    if (this.scanStatusText) {
      this.scanStatusText.innerText = "OCR AI Engine Reading Laboratory Report...";
    }

    const formData = new FormData();
    if (this.activePreset) {
      formData.append('preset', this.activePreset);
    } else if (this.selectedFile) {
      formData.append('report_file', this.selectedFile);
    }
    const notesInput = document.getElementById('report-notes');
    if (notesInput) {
      formData.append('notes', notesInput.value);
    }

    fetch('/api/ocr/analyze', {
      method: 'POST',
      body: formData
    })
    .then(res => res.json())
    .then(data => {
      this.scannerBox.classList.remove('scanner-active');
      this.scanBtn.disabled = false;
      this.scanBtn.innerHTML = '<i class="fa-solid fa-wand-magic-sparkles mr-2"></i> Run Diagnostic OCR Scan';

      if (data.success) {
        showToast("Biomarkers extracted successfully!", "success");
        this.renderResults(data.extracted, data.summary, data.report_id);
      } else {
        showToast(data.error || "Failed to parse report.", "danger");
      }
    })
    .catch(err => {
      this.scannerBox.classList.remove('scanner-active');
      this.scanBtn.disabled = false;
      this.scanBtn.innerHTML = '<i class="fa-solid fa-wand-magic-sparkles mr-2"></i> Run Diagnostic OCR Scan';
      showToast("OCR processing error: " + err, "danger");
    });
  }

  static renderResults(extracted, summary, reportId) {
    this.resultsCard.classList.remove('hidden');
    this.resultsCard.scrollIntoView({ behavior: 'smooth' });

    // Populate metadata
    document.getElementById('report-title-display').innerText = extracted.report_title || 'Diagnostic Lab Report';
    document.getElementById('report-lab-display').innerText = extracted.lab_name || 'Clinical Pathology';
    document.getElementById('report-date-display').innerText = extracted.report_date || new Date().toISOString().split('T')[0];

    // Status badge
    const badge = document.getElementById('report-status-badge');
    if (badge) {
      const st = extracted.overall_status || 'Normal';
      badge.innerText = st;
      badge.className = `px-3 py-1 rounded-full text-xs font-semibold ${
        st === 'Normal' ? 'bg-emerald-100 text-emerald-800' :
        st === 'Attention Needed' ? 'bg-amber-100 text-amber-800' : 'bg-rose-100 text-rose-800'
      }`;
    }

    // Populate Biomarkers Table
    this.biomarkersTableBody.innerHTML = '';
    (extracted.biomarkers || []).forEach(bio => {
      const row = document.createElement('tr');
      row.className = "border-b border-slate-100 hover:bg-slate-50 transition-colors";

      const statusClass = bio.status === 'Normal' ? 'badge-status-normal' :
                          bio.status === 'Borderline' ? 'badge-status-borderline' :
                          bio.status === 'Low' ? 'badge-status-low' : 'badge-status-high';

      row.innerHTML = `
        <td class="py-3 px-4 font-medium text-slate-800">
          ${bio.parameter}
        </td>
        <td class="py-3 px-4 font-bold text-slate-900">
          ${bio.value} <span class="text-xs font-normal text-slate-500">${bio.unit || ''}</span>
        </td>
        <td class="py-3 px-4 text-xs text-slate-600 font-mono">
          ${bio.ref_range || 'Standard'}
        </td>
        <td class="py-3 px-4">
          <span class="px-2.5 py-1 rounded-md text-xs font-semibold ${statusClass}">
            ${bio.status}
          </span>
        </td>
        <td class="py-3 px-4 text-xs text-slate-500 max-w-xs">
          ${bio.clinical_note || 'Standard reference parameter'}
        </td>
      `;
      this.biomarkersTableBody.appendChild(row);
    });

    // Populate inline summary
    const summaryCard = document.getElementById('inline-summary-box');
    if (summaryCard && summary) {
      summaryCard.classList.remove('hidden');
      document.getElementById('summary-overview-text').innerText = summary.overview || '';
      
      const attentionUl = document.getElementById('summary-attention-list');
      attentionUl.innerHTML = '';
      (summary.attention_points || []).forEach(pt => {
        const li = document.createElement('li');
        li.className = "flex items-start space-x-2 text-sm text-slate-700";
        li.innerHTML = `<i class="fa-solid fa-triangle-exclamation text-amber-500 mt-1"></i> <span>${pt}</span>`;
        attentionUl.appendChild(li);
      });

      const lifestyleUl = document.getElementById('summary-lifestyle-list');
      lifestyleUl.innerHTML = '';
      (summary.lifestyle_tips || []).forEach(tip => {
        const li = document.createElement('li');
        li.className = "flex items-start space-x-2 text-sm text-slate-700";
        li.innerHTML = `<i class="fa-solid fa-circle-check text-emerald-500 mt-1"></i> <span>${tip}</span>`;
        lifestyleUl.appendChild(li);
      });
    }

    // Update full summary link
    const fullSummaryBtn = document.getElementById('btn-view-full-summary');
    if (fullSummaryBtn) {
      fullSummaryBtn.href = `/health-summary${reportId ? '?report_id=' + reportId : ''}`;
    }
  }
}

document.addEventListener('DOMContentLoaded', () => {
  OCRHandler.init();
});
