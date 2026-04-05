function renderSuccess(data) {
    const decisionEl = document.getElementById('res-decision');
    decisionEl.innerHTML = `<span style="display:block; font-size:0.7rem; color:var(--text-muted);">RL ACTION PIPELINE</span>${data.decision}`;
    decisionEl.style.color = data.decision === 'INVESTIGATE' ? 'var(--danger)' : 'var(--approve)';
    
    const baselineEl = document.getElementById('res-baseline');
    baselineEl.innerHTML = `<span style="display:block; font-size:0.7rem; color:var(--text-muted);">BASELINE RULESET PREDICTION</span>${data.baseline_decision}`;
    
    document.getElementById('res-fraud').textContent = data.scores.fraud.toFixed(2);
    document.getElementById('res-severity').textContent = data.scores.severity.toFixed(2);
    document.getElementById('res-graph').textContent = data.scores.graph.toFixed(2);
    
    // Reward formatting Semantic
    const rew = data.expected_reward;
    let rewText = rew.toFixed(2);
    if(rew < -2.0) rewText += ' (High Risk Penalty)';
    else if(rew > -1.0) rewText += ' (Clean Action Expectancy)';
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
    
    const graphUl = document.getElementById('xai-graph');
    graphUl.innerHTML = '';
    if(data.scores.graph_breakdown && Object.keys(data.scores.graph_breakdown).length > 0) {
        for(let key in data.scores.graph_breakdown) {
            graphUl.innerHTML += `<li>${key}: +${data.scores.graph_breakdown[key].toFixed(2)}</li>`;
        }
    } else {
        graphUl.innerHTML = `<li>No Graph Links Detected</li>`;
    }
    
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
