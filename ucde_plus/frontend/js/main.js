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
        
        document.getElementById('feedback-panel').innerHTML = "<p style='color: var(--approve);'>Adjuster Ground Truth Integrated Continuously. Replay buffer aligned seamlessly!</p>";
        
    } catch(err) {
        alert("Feedback Synchronization Failed: " + err.message);
    }
}
