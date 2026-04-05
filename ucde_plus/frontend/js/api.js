async function submitClaim(payload, isDebug) {
    const params = new URLSearchParams();
    if (isDebug) params.append("mode", "debug");
    else params.append("mode", "production");
    
    try {
        const response = await fetch(`/v1/fnol?${params.toString()}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            let msg = data.detail || 'Server communication error';
            if (Array.isArray(data.detail)) msg = "Validation Error: Structure violates Pydantic constraints.";
            throw new Error(msg);
        }
        
        return data;
    } catch(err) {
        throw new Error(err.message || 'API Communication Timeout');
    }
}
