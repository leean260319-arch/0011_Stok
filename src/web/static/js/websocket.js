/**
 * websocket.js
 * StokAI - WebSocket connection manager with exponential backoff reconnect
 */

class WebSocketManager {
    /**
     * @param {string} url - WebSocket URL (ws:// or wss://)
     * @param {object} handlers - { onMessage, onOpen, onClose, onError }
     */
    constructor(url, handlers = {}) {
        this.url = url;
        this.handlers = handlers;
        this.ws = null;

        // Reconnect state
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 20;
        this.baseDelay = 1000;   // 1s
        this.maxDelay  = 30000;  // 30s
        this.reconnectTimer = null;

        // 'connecting' | 'connected' | 'disconnected' | 'reconnecting' | 'failed'
        this.state = 'disconnected';

        // Flag: do not reconnect on intentional close
        this._intentionalClose = false;

        // Messages queued while connection is not yet open
        this._sendQueue = [];
    }

    /**
     * Exponential backoff with jitter.
     * delay = min(baseDelay * 2^attempt, maxDelay) + rand(0..500)
     */
    _getReconnectDelay() {
        const exp   = Math.min(this.reconnectAttempts, 10);
        const delay = Math.min(this.baseDelay * Math.pow(2, exp), this.maxDelay);
        return Math.floor(delay + Math.random() * 500);
    }

    connect() {
        if (this.ws &&
            (this.ws.readyState === WebSocket.OPEN ||
             this.ws.readyState === WebSocket.CONNECTING)) {
            return;
        }

        this._intentionalClose = false;
        this.state = 'connecting';
        this._updateStatusUI('connecting');

        try {
            this.ws = new WebSocket(this.url);
        } catch (err) {
            console.error('[WS] Constructor error:', err);
            this._scheduleReconnect();
            return;
        }

        this.ws.onopen = (event) => {
            console.log('[WS] Connected:', this.url);
            this.state = 'connected';
            this.reconnectAttempts = 0;
            this._updateStatusUI('connected');

            // Flush queued messages
            while (this._sendQueue.length > 0) {
                this._rawSend(this._sendQueue.shift());
            }

            if (this.handlers.onOpen) this.handlers.onOpen(event);
        };

        this.ws.onmessage = (event) => {
            let data;
            try {
                data = JSON.parse(event.data);
            } catch (e) {
                console.warn('[WS] Non-JSON message:', event.data);
                return;
            }
            if (this.handlers.onMessage) this.handlers.onMessage(data);
        };

        this.ws.onclose = (event) => {
            console.log(`[WS] Closed. code=${event.code} reason="${event.reason}"`);
            this.state = 'disconnected';
            this._updateStatusUI('disconnected');
            if (this.handlers.onClose) this.handlers.onClose(event);
            if (!this._intentionalClose) this._scheduleReconnect();
        };

        this.ws.onerror = (event) => {
            console.error('[WS] Error:', event);
            this._updateStatusUI('error');
            if (this.handlers.onError) this.handlers.onError(event);
            // onclose fires automatically after onerror
        };
    }

    _scheduleReconnect() {
        if (this.reconnectAttempts >= this.maxReconnectAttempts) {
            console.error('[WS] Max reconnect attempts reached.');
            this.state = 'failed';
            this._updateStatusUI('failed');
            return;
        }

        const delay = this._getReconnectDelay();
        this.reconnectAttempts++;
        console.log(`[WS] Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
        this._updateStatusUI('reconnecting', delay);

        this.reconnectTimer = setTimeout(() => this.connect(), delay);
    }

    send(data) {
        const payload = typeof data === 'string' ? data : JSON.stringify(data);
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this._rawSend(payload);
        } else {
            this._sendQueue.push(payload);
        }
    }

    _rawSend(payload) {
        try {
            this.ws.send(payload);
        } catch (err) {
            console.error('[WS] Send failed:', err);
        }
    }

    disconnect() {
        this._intentionalClose = true;
        if (this.reconnectTimer) {
            clearTimeout(this.reconnectTimer);
            this.reconnectTimer = null;
        }
        if (this.ws) this.ws.close(1000, 'Client disconnected');
        this.state = 'disconnected';
    }

    isConnected() {
        return this.ws !== null && this.ws.readyState === WebSocket.OPEN;
    }

    /**
     * Updates DOM elements:
     *   #ws-status-dot  (class: dot dot-online|dot-offline|dot-warning)
     *   #ws-status-text (text content)
     */
    _updateStatusUI(status, reconnectDelay = null) {
        const dot  = document.getElementById('ws-status-dot');
        const text = document.getElementById('ws-status-text');
        if (!dot && !text) return;

        const secs = reconnectDelay ? Math.round(reconnectDelay / 1000) : '?';
        const map = {
            connecting:   { cls: 'dot dot-warning',  label: '연결 중...' },
            connected:    { cls: 'dot dot-online',   label: 'API 연결됨' },
            disconnected: { cls: 'dot dot-offline',  label: '연결 끊김' },
            reconnecting: { cls: 'dot dot-warning',  label: `재연결 중... (${secs}s)` },
            error:        { cls: 'dot dot-offline',  label: '연결 오류' },
            failed:       { cls: 'dot dot-offline',  label: '연결 실패' },
        };

        const cfg = map[status] || map['disconnected'];
        if (dot)  dot.className  = cfg.cls;
        if (text) text.textContent = cfg.label;
    }
}
