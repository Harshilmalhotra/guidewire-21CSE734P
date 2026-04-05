function renderSuccess(data) {
    const decisionEl = document.getElementById('res-decision');
    decisionEl.textContent = data.decision;
    decisionEl.style.color = data.decision === 'INVESTIGATE' ? 'var(--danger)' : 'var(--approve)';
    
    document.getElementById('res-fraud').textContent = data.scores.fraud.toFixed(2);
    document.getElementById('res-severity').textContent = data.scores.severity.toFixed(2);
    document.getElementById('res-graph').textContent = data.scores.graph.toFixed(2);
    document.getElementById('res-reward').textContent = data.expected_reward.toFixed(2);
    
    // LLM Layer
    document.getElementById('res-justification').textContent = data.explanation?.justification || "No generative evaluation computed securely.";
    
    const conflictEl = document.getElementById('res-conflict');
    if(data.explanation?.conflict_explanation) {
        conflictEl.textContent = data.explanation.conflict_explanation;
        conflictEl.classList.remove('hidden');
    } else {
        conflictEl.classList.add('hidden');
    }
    
    // Debug Trace mode explicitly appending dynamically formatted blocks safely evaluating innerHTML constraints
    const traceContainer = document.getElementById('trace-container');
    const tracesUl = document.getElementById('res-traces');
    
    while(tracesUl.firstChild) {
        tracesUl.removeChild(tracesUl.firstChild);
    }
    
    if(data.decision_trace) {
        traceContainer.classList.remove('hidden');
        data.decision_trace.forEach(trace => {
            const li = document.createElement('li');
            li.textContent = trace; // Secure insertion preventing XSS
            tracesUl.appendChild(li);
        });
    } else {
        traceContainer.classList.add('hidden');
    }
}
