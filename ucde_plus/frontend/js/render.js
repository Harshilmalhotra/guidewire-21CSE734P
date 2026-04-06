function renderSuccess(data) {
    const stateSuccess = document.getElementById('state-success');
    stateSuccess.classList.remove('hidden');
    stateSuccess.style.animation = 'fadeInUp 0.6s ease forwards';

    const decisionEl = document.getElementById('res-decision');
    decisionEl.innerHTML = `<span style="display:block; font-size:0.6rem; color:var(--text-muted); margin-bottom: 0.5rem;">RL ACTION PIPELINE</span>${data.decision}`;
    decisionEl.style.borderColor = data.decision === 'INVESTIGATE' ? 'var(--danger)' : 'var(--primary)';
    decisionEl.style.color = data.decision === 'INVESTIGATE' ? 'var(--danger)' : 'var(--success)';
    
    const baselineEl = document.getElementById('res-baseline');
    baselineEl.innerHTML = `<span style="display:block; font-size:0.6rem; color:var(--text-muted); margin-bottom: 0.5rem;">BASELINE RULESET</span>${data.baseline_decision}`;
    
    document.getElementById('res-fraud').textContent = data.scores.fraud.toFixed(2);
    document.getElementById('res-graph').textContent = data.scores.graph.toFixed(2);
    document.getElementById('res-confidence').textContent = `${(data.confidence_score * 100).toFixed(1)}%`;
    document.getElementById('res-conf-reason').textContent = data.confidence_reason;
    
    // Reward formatting Semantic
    const rew = data.expected_reward;
    let rewText = rew.toFixed(2);
    if(rew < -2.0) rewText += ' (High Risk Penalty)';
    else if(rew > -1.0) rewText += ' (Optimal Path)';
    document.getElementById('res-reward').textContent = rewText;
    
    // Explicit Feature Breakdowns
    const fraudUl = document.getElementById('xai-fraud');
    fraudUl.innerHTML = '';
    if(data.scores.fraud_breakdown && Object.keys(data.scores.fraud_breakdown).length > 0) {
        for(let key in data.scores.fraud_breakdown) {
            fraudUl.innerHTML += `<li>${key}: +${data.scores.fraud_breakdown[key].toFixed(2)}</li>`;
        }
    } else {
        fraudUl.innerHTML = `<li>Baseline Only</li>`;
    }
    
    // Explanation Layer
    document.getElementById('res-trigger').textContent = data.primary_trigger || "Execution securely terminated.";
    document.getElementById('res-justification').textContent = data.explanation?.justification || "No generative evaluation computed.";
    
    // Feedback Station
    const feedbackPanel = document.getElementById('feedback-panel');
    if (feedbackPanel) {
        feedbackPanel.classList.remove('hidden');
        feedbackPanel.dataset.traceId = data.trace_id || "";
        feedbackPanel.dataset.predictedAction = data.decision;
    }
}
