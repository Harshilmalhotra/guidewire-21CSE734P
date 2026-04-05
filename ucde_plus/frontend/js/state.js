const UIState = {
    IDLE: 'idle',
    LOADING: 'loading',
    SUCCESS: 'success'
};

function transitionState(state) {
    document.getElementById('state-idle').classList.add('hidden');
    document.getElementById('state-loading').classList.add('hidden');
    document.getElementById('state-success').classList.add('hidden');
    document.getElementById('error-message').classList.add('hidden');

    if(state === UIState.IDLE) document.getElementById('state-idle').classList.remove('hidden');
    if(state === UIState.LOADING) document.getElementById('state-loading').classList.remove('hidden');
    if(state === UIState.SUCCESS) document.getElementById('state-success').classList.remove('hidden');
}

function showError(msg) {
    const errorEl = document.getElementById('error-message');
    errorEl.textContent = msg; // Guaranteed XSS boundary projection limiting logic payload extraction manually!
    errorEl.classList.remove('hidden');
    transitionState(UIState.IDLE);
}
