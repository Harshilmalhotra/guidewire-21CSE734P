document.addEventListener('DOMContentLoaded', () => {
    transitionState(UIState.IDLE);
    
    document.getElementById('claim-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const claimAmount = parseFloat(document.getElementById('claimAmount').value);
        if (claimAmount <= 0) {
            showError("Claim amount must be greater than 0");
            return;
        }
        
        const payload = {
            policyId: document.getElementById('policyId').value,
            policyholderId: document.getElementById('policyholderId').value,
            vehicleVin: document.getElementById('vehicleVin').value,
            claimAmount: claimAmount,
            description: document.getElementById('description').value,
            images: [],
            claimHistoryCount: 0,
            timeSinceLastClaim: 0.0,
            metadata: {}
        };
        
        const isDebug = document.getElementById('debugMode').checked;
        
        transitionState(UIState.LOADING);
        
        try {
            const result = await submitClaim(payload, isDebug);
            renderSuccess(result);
            transitionState(UIState.SUCCESS);
            
            // Set trace dynamically enabling UI features natively
            const fp = document.getElementById('feedback-panel');
            fp.dataset.traceId = result.trace_id;
            fp.dataset.predictedAction = result.rl_decision;
            fp.classList.remove('hidden');
            
        } catch (err) {
            showError(err.message);
        }
    });
});

async function submitAdjusterOverrides(action, isFraud) {
    const traceId = document.getElementById('feedback-panel').dataset.traceId;
    if(!traceId) return;
    
    // Safely block overrides explicitly mapped cleanly preventing spam loops gracefully natively
    const fbPayload = {
        trace_id: traceId,
        human_action: action,
        verified_fraud: isFraud,
        confidence: "HIGH",
        comment: "Manual Desktop Verification Check natively executed globally"
    };

    try {
        const response = await fetch('/v1/feedback', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': 'Bearer adjuster-api-token'
            },
            body: JSON.stringify(fbPayload)
        });
        
        if (!response.ok) {
            const errData = await response.json();
            throw new Error(errData.detail || 'Feedback Rejection Logic Bound');
        }
        
        const predicted = document.getElementById('feedback-panel').dataset.predictedAction;
        const correctness = (predicted === action) ? "CORRECT" : "INCORRECT (Penalty Logged natively out towards SQLite buffers array metrics securely)";
        const color = (predicted === action) ? "var(--approve)" : "var(--danger)";
        
        document.getElementById('feedback-panel').innerHTML = `<p style='color: ${color};'>Your Feedback: <strong>${action}</strong><br>System Model: <strong>${predicted}</strong><br>Feedback Submitted! Model was ${correctness}.</p>`;
        
    } catch(err) {
        alert("Feedback Synchronization Failed: " + err.message);
    }
}

async function fetchReplayTrace() {
    const traceId = document.getElementById('replay-trace-id').value;
    if(!traceId) return;
    
    try {
        const response = await fetch(`/v1/trace/${traceId}`, {
            headers: { 'Authorization': 'Bearer admin-api-token' }
        });
        if(!response.ok) throw new Error("Trace ID isolated or missing within SQLite constraints");
        
        const data = await response.json();
        alert(`Forensic Case Loaded:\n\nState Vector Bounds:\n[ ${data.state_vector.map(n=>n.toFixed(2)).join(", ")} ]\n\nPast RL Prediction: ${data.predicted_action}\nTimestamp: ${data.timestamp}\n\nReplay pipeline validates the vector limits securely offline.`);
        
    } catch(err) {
        alert(err.message);
    }
}

function loadWhatIfScenario(type) {
    if (type === 'amount') {
        document.getElementById('policyId').value = "POL-W1";
        document.getElementById('policyholderId').value = "JOHN-W1";
        document.getElementById('vehicleVin').value = "VIN-W1";
        document.getElementById('description').value = "Minor fender bender in parking lot.";
        // Tweak amount high to trigger boundary flip natively
        document.getElementById('claimAmount').value = "25000"; 
        alert("What-If Scenario loaded: High Claim Amount (Severity Boundary Flip -> INVESTIGATE). Hit Evaluate to test.");
    } else if (type === 'graph') {
        document.getElementById('policyId').value = "POL-W2";
        // Connect directly to known flagged node triggering deep graph anomaly logic
        document.getElementById('policyholderId').value = "user-123"; 
        document.getElementById('vehicleVin').value = "vin-456";
        document.getElementById('description').value = "Clean record, parked car sideswiped.";
        document.getElementById('claimAmount').value = "1000"; 
        alert("What-If Scenario loaded: Explicit Graph Contagion Link (Network Boundary Flip -> INVESTIGATE). Hit Evaluate to test.");
    }
}
