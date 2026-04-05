async function fetchMetrics() {
    const adminToken = "Bearer admin-api-token"; // Demo extraction variable
    try {
        const response = await fetch('/v1/metrics?days=7&model_version=v1.0.0', {
            method: 'GET',
            headers: { 'Authorization': adminToken }
        });
        
        if (!response.ok) throw new Error("Unauthorized mapping");
        
        const data = await response.json();
        
        document.getElementById('m_total_claims').textContent = data.total_claims_processed;
        document.getElementById('m_agreements').textContent = `${(data.system_agreement_rate * 100).toFixed(1)}%`;
        
        let p = (data.precision * 100).toFixed(1);
        let r = (data.recall * 100).toFixed(1);
        let f = (data.f1_score * 100).toFixed(1);
        document.getElementById('m_fraud_rate').textContent = `P: ${p}% | R: ${r}% | F1: ${f}%`;
        document.getElementById('m_drift_rate').textContent = `${(data.disagreement_drift_rate * 100).toFixed(1)}% (RL Overrides Baseline)`;
        
    } catch(err) {
        console.error("Admin KPI Block Disabled Securing internal structures: ", err);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    fetchMetrics();
    // Re-poll every 30 seconds explicitly mimicking websocket dashboards smoothly caching
    setInterval(fetchMetrics, 30000);
});
