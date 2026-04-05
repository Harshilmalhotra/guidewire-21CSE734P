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
        } catch (err) {
            showError(err.message);
        }
    });
});
