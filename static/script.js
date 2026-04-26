const logoutBtn = document.getElementById('logoutBtn');
const lookupBtn = document.getElementById('lookupBtn');
const saveBtn = document.getElementById('saveBtn');
const startScanBtn = document.getElementById('startScanBtn');
const stopScanBtn = document.getElementById('stopScanBtn');
const medList = document.getElementById('medList');
const medicinesGrid = document.getElementById('medicinesGrid');
const scanStatus = document.getElementById('scanStatus');
const saveStatus = document.getElementById('saveStatus');
const scannerContainer = document.getElementById('scanner-container');
const barcodeInput = document.getElementById('barcodeInput');

let html5QrcodeScanner;

logoutBtn?.addEventListener('click', async () => {
    await fetch('/logout');
    window.location.href = '/login';
});

// Tab switching
document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', () => {
        const sectionId = tab.dataset.section;
        activateTab(sectionId);
    });
});

function activateTab(sectionId) {
    document.querySelectorAll('.section').forEach(section => {
        section.classList.remove('active');
    });
    document.querySelectorAll('.tab').forEach(tab => {
        tab.classList.remove('active');
    });
    document.getElementById(sectionId).classList.add('active');
    document.querySelector(`[data-section="${sectionId}"]`).classList.add('active');

    if (sectionId === 'sectionAdd') {
        const barcode = barcodeInput.value.trim();
        document.getElementById('addBarcodeValue').textContent = barcode || '(not set yet)';
    }
}

lookupBtn?.addEventListener('click', async () => {
    const barcode = barcodeInput.value.trim();
    if (!barcode) return (scanStatus.textContent = 'Enter a barcode first');

    await lookupBarcode(barcode);
});

startScanBtn?.addEventListener('click', () => {
    scannerContainer.classList.add('active');
    startScanner();
});

stopScanBtn?.addEventListener('click', () => {
    if (html5QrcodeScanner) {
        html5QrcodeScanner.clear();
    }
    scannerContainer.classList.remove('active');
    scanStatus.textContent = 'Scanner stopped';
});

const sectionAdd = document.getElementById('sectionAdd');

saveBtn?.addEventListener('click', async () => {
    const barcode = barcodeInput.value.trim();
    const name = document.getElementById('nameInput').value.trim();
    const expiry = document.getElementById('expiryInput').value;
    const use = document.getElementById('useInput').value.trim();

    if (!barcode||!name||!expiry||!use) return (saveStatus.textContent = 'All fields required');

    const res = await fetch('/save', {
        method:'POST', headers:{'Content-Type':'application/json'},
        body: JSON.stringify({barcode,name,expiry,use})
    });
    const result = await res.json();
    if (result.status === 'success') {
        saveStatus.textContent = 'Saved successfully';

        // Clear form fields and reset the add card state
        barcodeInput.value = '';
        document.getElementById('nameInput').value = '';
        document.getElementById('expiryInput').value = '';
        document.getElementById('useInput').value = '';
        document.getElementById('addBarcodeValue').textContent = '(not set yet)';

        loadMedicines();
        activateTab('sectionList');
    } else {
        saveStatus.textContent = result.message || 'Save error';
    }
});

async function lookupBarcode(barcode) {
    const res = await fetch('/scan', {
        method:'POST', headers:{'Content-Type':'application/json'},
        body: JSON.stringify({barcode})
    });
    const data = await res.json();

    const resultCard = document.getElementById('resultCard');
    const resultStatus = document.getElementById('resultStatus');
    const resultName = document.getElementById('resultName');
    const resultExpiry = document.getElementById('resultExpiry');

    if (data.status === 'found') {
        const expiry = data.expiry;
        const today = new Date();
        const expDate = new Date(expiry);
        const isExpired = expDate < new Date(today.getFullYear(), today.getMonth(), today.getDate());

        resultName.textContent = data.name;
        resultExpiry.textContent = `Expiry Date: ${expiry}`;
        resultStatus.textContent = isExpired ? 'Expired' : 'Valid';
        resultStatus.className = 'result-status ' + (isExpired ? 'expired' : 'valid');

        resultCard.style.display = 'block';
        scanStatus.textContent = '';
    } else if (data.status === 'not_found') {
        resultCard.style.display = 'none';
        scanStatus.textContent = `No record found. Please add medicine details.`;
        document.getElementById('addBarcodeValue').textContent = barcode;
        document.getElementById('nameInput').focus();
        activateTab('sectionAdd');
    } else {
        resultCard.style.display = 'none';
        scanStatus.textContent = data.message || 'Error searching barcode';
    }
}

function startScanner() {
    scannerContainer.style.display = 'block';
    scanStatus.textContent = 'Starting scanner...';

    if (html5QrcodeScanner) {
        try { html5QrcodeScanner.stop().catch(()=>{}); } catch(_) {}
        html5QrcodeScanner.clear();
    }

    html5QrcodeScanner = new Html5Qrcode("reader");

    let scanned = false; // 🔥 prevent multiple scan

    const qrConfig = {
        fps: 20,  // ⚡ FAST (10 → 20)
        qrbox: { width: 200, height: 200 }, // ⚡ smaller = faster

        aspectRatio: 1.0,

        videoConstraints: {
            facingMode: "environment",
            width: { ideal: 640 },   // ⚡ lower resolution = fast
            height: { ideal: 480 }
        }
    };

    html5QrcodeScanner.start(
        { facingMode: "environment" },
        qrConfig,

        (decodedText) => {

            if (scanned) return; // 🔥 avoid duplicate
            scanned = true;

            barcodeInput.value = decodedText;
            scanStatus.textContent = `Detected: ${decodedText}`;

            // ⚡ stop immediately (important for speed feel)
            html5QrcodeScanner.stop().then(() => {
                html5QrcodeScanner.clear();
                scannerContainer.style.display = 'none';

                lookupBarcode(decodedText); // auto lookup
            }).catch(() => {
                scannerContainer.style.display = 'none';
                lookupBarcode(decodedText);
            });
        },

        () => {
            scanStatus.textContent = 'Scanning...';
        }

    ).catch((err) => {
        console.error(err);
        scanStatus.textContent = 'Camera error';
        scannerContainer.style.display = 'none';
    });
}

async function loadMedicines(){
    const res = await fetch('/get-medicines');
    const data = await res.json();
    if(data.status==='success'){
        if (!data.medicines || data.medicines.length === 0) {
            medicinesGrid.innerHTML = `
                <div class="medicine-card empty">
                    <h3>No medicines yet</h3>
                    <p>Start by scanning a barcode or adding a new medicine.</p>
                </div>
            `;
            return;
        }

        medicinesGrid.innerHTML = data.medicines.map(m => {
            const today = new Date();
            const expDate = new Date(m.expiry);
            const isExpired = expDate < new Date(today.getFullYear(), today.getMonth(), today.getDate());
            const statusClass = isExpired ? 'expired' : 'valid';
            const statusText = isExpired ? 'Expired' : 'Valid';
            return `
                <div class="medicine-card" data-id="${m.id}">
                    <div class="medicine-status ${statusClass}">${statusText}</div>
                    <h3 class="medicine-name">${m.name}</h3>
                    <p class="medicine-barcode">Barcode: ${m.barcode}</p>
                    <p class="medicine-expiry">Expiry: ${m.expiry}</p>
                    <p class="medicine-use">Use: ${m.use}</p>
                    <button data-id="${m.id}" class="del">Delete</button>
                </div>
            `;
        }).join('');
    } else {
        medicinesGrid.innerHTML = `<div class="medicine-card error">${data.message||'Unable to fetch'}</div>`;
    }
}

medicinesGrid.addEventListener('click', async (event) => {
    const btn = event.target.closest('.del');
    if (!btn) return;

    const medicineId = btn.dataset.id;
    if (!medicineId) return;

    btn.disabled = true;
    btn.textContent = 'Deleting...';

    try {
        const deleteRes = await fetch(`/delete-medicine/${medicineId}`, { method: 'DELETE' });
        if (deleteRes.ok) {
            await loadMedicines();
        } else {
            const err = await deleteRes.json().catch(() => ({}));
            scanStatus.textContent = err.message || 'Delete failed';
            btn.disabled = false;
            btn.textContent = 'Delete';
        }
    } catch (err) {
        scanStatus.textContent = 'Delete error: ' + err;
        btn.disabled = false;
        btn.textContent = 'Delete';
    }
});

loadMedicines();
