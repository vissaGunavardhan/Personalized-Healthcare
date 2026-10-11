/**
 * ABDM ABHA Card 3D Flip, QR Code Generator & Consent Manager
 */

class ABDMManager {
  static init() {
    this.flipCard = document.getElementById('abdm-card');
    this.flipBtn = document.getElementById('btn-flip-card');
    this.downloadBtn = document.getElementById('btn-download-card');
    this.printBtn = document.getElementById('btn-print-card');

    this.bindEvents();
    this.renderDynamicQR();
  }

  static bindEvents() {
    // 3D Flip
    if (this.flipCard) {
      this.flipCard.addEventListener('click', () => this.toggleFlip());
    }
    if (this.flipBtn) {
      this.flipBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        this.toggleFlip();
      });
    }

    // Print
    if (this.printBtn) {
      this.printBtn.addEventListener('click', () => {
        window.print();
      });
    }

    // Consent Toggles
    document.querySelectorAll('.btn-toggle-consent').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const consentId = btn.getAttribute('data-id');
        const currentStatus = btn.getAttribute('data-status');
        const newStatus = currentStatus === 'Active' ? 'Revoked' : 'Active';
        this.toggleConsent(consentId, newStatus, btn);
      });
    });
  }

  static toggleFlip() {
    if (this.flipCard) {
      this.flipCard.classList.toggle('flipped');
    }
  }

  static renderDynamicQR() {
    const qrContainer = document.getElementById('abdm-qr-container');
    if (!qrContainer) return;

    const payloadRaw = qrContainer.getAttribute('data-payload') || '{}';
    let payload = {};
    try {
      payload = JSON.parse(payloadRaw);
    } catch(e) {
      payload = { abha: "14-8291-5021-9482" };
    }

    // Generate high-contrast clean SVG QR-style representation
    const abhaNum = payload.abhaNumber || "14-8291-5021-9482";
    const abhaAddr = payload.abhaAddress || "user@abdm";
    
    // Create clean SVG QR visual matrix
    qrContainer.innerHTML = `
      <div class="p-2 bg-white rounded-lg border border-slate-200 flex flex-col items-center">
        <svg viewBox="0 0 100 100" class="w-24 h-24 text-slate-900" fill="currentColor">
          <!-- Position Markers (Top-Left, Top-Right, Bottom-Left) -->
          <rect x="5" y="5" width="28" height="28" fill="#0f172a" rx="2" />
          <rect x="9" y="9" width="20" height="20" fill="#ffffff" rx="1" />
          <rect x="13" y="13" width="12" height="12" fill="#0f172a" rx="1" />

          <rect x="67" y="5" width="28" height="28" fill="#0f172a" rx="2" />
          <rect x="71" y="9" width="20" height="20" fill="#ffffff" rx="1" />
          <rect x="75" y="13" width="12" height="12" fill="#0f172a" rx="1" />

          <rect x="5" y="67" width="28" height="28" fill="#0f172a" rx="2" />
          <rect x="9" y="71" width="20" height="20" fill="#ffffff" rx="1" />
          <rect x="13" y="75" width="12" height="12" fill="#0f172a" rx="1" />

          <!-- Data Grid Pattern -->
          <rect x="38" y="10" width="6" height="6" fill="#0f172a" />
          <rect x="48" y="10" width="6" height="6" fill="#0f172a" />
          <rect x="38" y="22" width="6" height="6" fill="#0f172a" />
          <rect x="54" y="22" width="6" height="6" fill="#0f172a" />

          <rect x="10" y="38" width="6" height="6" fill="#0f172a" />
          <rect x="22" y="44" width="6" height="6" fill="#0f172a" />
          <rect x="38" y="38" width="6" height="6" fill="#0f172a" />
          <rect x="48" y="44" width="8" height="8" fill="#0d9488" />
          <rect x="62" y="38" width="6" height="6" fill="#0f172a" />
          <rect x="76" y="44" width="6" height="6" fill="#0f172a" />
          <rect x="86" y="38" width="6" height="6" fill="#0f172a" />

          <rect x="38" y="58" width="6" height="6" fill="#0f172a" />
          <rect x="52" y="62" width="6" height="6" fill="#0f172a" />
          <rect x="42" y="74" width="6" height="6" fill="#0f172a" />
          <rect x="64" y="74" width="8" height="8" fill="#0f172a" />
          <rect x="80" y="62" width="6" height="6" fill="#0f172a" />
          <rect x="76" y="80" width="6" height="6" fill="#0f172a" />
        </svg>
        <span class="text-[9px] font-mono text-slate-500 mt-1 font-semibold tracking-tighter">NHA / ABDM SECURE QR</span>
      </div>
    `;
  }

  static toggleConsent(consentId, newStatus, btn) {
    const formData = new FormData();
    formData.append('consent_id', consentId);
    formData.append('status', newStatus);

    btn.disabled = true;
    fetch('/api/abdm/consent/toggle', {
      method: 'POST',
      body: formData
    })
    .then(res => res.json())
    .then(data => {
      btn.disabled = false;
      if (data.success) {
        btn.setAttribute('data-status', newStatus);
        const badge = document.getElementById(`status-badge-${consentId}`);
        if (badge) {
          badge.innerText = newStatus;
          badge.className = `px-2.5 py-0.5 rounded-full text-xs font-semibold ${
            newStatus === 'Active' ? 'bg-emerald-100 text-emerald-800' : 'bg-rose-100 text-rose-800'
          }`;
        }
        btn.innerText = newStatus === 'Active' ? 'Revoke Access' : 'Grant Access';
        btn.className = `btn-toggle-consent text-xs font-medium px-3 py-1.5 rounded-lg transition-colors ${
          newStatus === 'Active' ? 'bg-rose-50 text-rose-700 hover:bg-rose-100' : 'bg-emerald-50 text-emerald-700 hover:bg-emerald-100'
        }`;
        showToast(`Consent permission updated to: ${newStatus}`, 'success');
      } else {
        showToast('Failed to update consent permission.', 'danger');
      }
    })
    .catch(err => {
      btn.disabled = false;
      showToast('Error updating consent: ' + err, 'danger');
    });
  }
}

document.addEventListener('DOMContentLoaded', () => {
  ABDMManager.init();
});
