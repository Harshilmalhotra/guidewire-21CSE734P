async function fetchMetrics() {
    const adminToken = "Bearer admin-api-token"; // Demo extraction variable
    try {
        const response = await fetch('/v1/metrics?days=7&model_version=v1.0.0', {
            method: 'GET',
            headers: { 'Authorization': adminToken }
        });
        
        if (!response.ok) throw new Error("Unauthorized mapping");
        
        const data = await response.json();
        
        document.getElementById('m_total_claims').textContent = data.total_claims_processed || 0;
        document.getElementById('m_agreements').textContent = `${((data.system_agreement_rate || 0) * 100).toFixed(1)}%`;
        
        let p = ((data.precision || 0) * 100).toFixed(1);
        let r = ((data.recall || 0) * 100).toFixed(1);
        let f = ((data.f1_score || 0) * 100).toFixed(1);
        document.getElementById('m_fraud_rate').textContent = `P: ${p}% | R: ${r}% | F1: ${f}%`;
        document.getElementById('m_drift_rate').textContent = `${((data.disagreement_drift_rate || 0) * 100).toFixed(1)}%`;
        
        let dist = data.trigger_distribution || {};
        document.getElementById('m_trigger_dist').textContent = `Sev: ${dist.Severity || 0}% | Frd: ${dist.Fraud || 0}% | Grph: ${dist.Graph || 0}% (n=${data.total_claims_processed || 0} cases)`;
        
        // Update 10/10 Enterprise Health Dashboard
        updateHealthHUD(data);
        
    } catch(err) {
        console.error("Admin KPI Block Disabled: ", err);
    }
}

// Global System Health & Training Logic
async function updateHealthHUD(data) {
    // LLM & Model Info
    document.getElementById('h-model').textContent = data.model_v || "v1";
    document.getElementById('h-samples').textContent = data.total_samples_collected || 0;
    
    const count = data.total_samples_collected || 0;
    const btn = document.getElementById('btn-retrain');
    const read = document.getElementById('h-readiness');
    
    // Hard threshold for demo logic
    if (count >= 10) {
        read.textContent = "READY (>10 samples)";
        read.style.color = "var(--success)";
        if (data.training_status !== "RUNNING") {
            btn.disabled = false;
            btn.style.opacity = "1";
            btn.style.cursor = "pointer";
        } else {
            btn.disabled = true;
            btn.style.opacity = "0.5";
        }
    } else {
        read.textContent = "WAITING (min 10)";
        read.style.color = "var(--text-muted)";
        btn.disabled = true;
        btn.style.opacity = "0.5";
    }

    // Training Progress HUD
    const prog = document.getElementById('training-progress-container');
    if (data.training_status === "RUNNING") {
        prog.classList.remove('hidden');
        document.getElementById('h-training-status').textContent = "RUNNING";
        // Manual jitter for the progress bar to show life
        const jitter = 40 + Math.random() * 20;
        document.getElementById('h-progress-bar').style.width = jitter + "%";
    } else {
        prog.classList.add('hidden');
    }

    // Fetch live Health tier for LLM Mode
    try {
        const h = await fetch('/v1/health');
        const hData = await h.json();
        document.getElementById('h-llm').textContent = hData.llm_mode;
        
        const hTag = document.getElementById('h-status-tag');
        if (hData.status === "HEALTHY") {
            hTag.textContent = "HEALTHY";
            hTag.style.background = "var(--success)";
        } else {
            hTag.textContent = "DEGRADED";
            hTag.style.background = "var(--danger)";
        }
    } catch(e) {}
}

document.addEventListener('DOMContentLoaded', () => {
    fetchMetrics();
    
    document.getElementById('btn-retrain').addEventListener('click', async () => {
        try {
            const res = await fetch('/v1/train', {
                method: 'POST',
                headers: { 'Authorization': 'Bearer admin-api-token' }
            });
            const data = await res.json();
            if (data.status === "SUCCESS") {
                fetchMetrics(); // Update status to RUNNING
            } else {
                alert(data.error || "Training failed.");
            }
        } catch(e) {
            console.error("Retrain error: ", e);
        }
    });

    // Poll every 5 seconds for training status & metrics
    setInterval(fetchMetrics, 5000);
});
