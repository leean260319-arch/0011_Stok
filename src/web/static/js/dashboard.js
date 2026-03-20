/**
 * dashboard.js
 * StokAI Dashboard - Main controller
 * WebSocket 기반 실시간 데이터 갱신 + REST API 제어
 */

class StokAIDashboard {
    constructor() {
        this.token = localStorage.getItem('stokai_token');
        this.wsManager = null;
        this._clockTimer = null;
        this._prevValues = {};  // for flash animation comparison
        this.init();
    }

    // =========================================================
    // Initialization
    // =========================================================

    init() {
        if (!this.token) {
            window.location.href = '/login';
            return;
        }
        this._startClock();
        this._connectWebSocket();
        this._bindEvents();
    }

    _connectWebSocket() {
        const protocol = location.protocol === 'https:' ? 'wss:' : 'ws:';
        const url = `${protocol}//${location.host}/ws?token=${encodeURIComponent(this.token)}`;

        this.wsManager = new WebSocketManager(url, {
            onMessage: (data) => this._handleMessage(data),
            onOpen:    ()     => console.log('[Dashboard] WebSocket open'),
            onClose:   ()     => console.log('[Dashboard] WebSocket closed'),
            onError:   (e)    => console.error('[Dashboard] WebSocket error', e),
        });

        this.wsManager.connect();
    }

    _startClock() {
        const el = document.getElementById('header-time');
        if (!el) return;
        const tick = () => {
            const now = new Date();
            const pad = (n) => String(n).padStart(2, '0');
            el.textContent = `${now.getFullYear()}-${pad(now.getMonth()+1)}-${pad(now.getDate())} `
                           + `${pad(now.getHours())}:${pad(now.getMinutes())}:${pad(now.getSeconds())}`;
        };
        tick();
        this._clockTimer = setInterval(tick, 1000);
    }

    _bindEvents() {
        this._on('btn-autotrade-start', 'click', () => this.startAutoTrade());
        this._on('btn-autotrade-stop',  'click', () => this.stopAutoTrade());
        this._on('btn-kill-on',         'click', () => this.killSwitchOn());
        this._on('btn-kill-off',        'click', () => this.killSwitchOff());
        this._on('btn-logout',          'click', () => this.logout());
    }

    _on(id, event, fn) {
        const el = document.getElementById(id);
        if (el) el.addEventListener(event, fn);
    }

    // =========================================================
    // WebSocket message handler
    // =========================================================

    _handleMessage(msg) {
        if (msg.type === 'state_update') {
            this.updateUI(msg.data);
        } else if (msg.type === 'alert') {
            this._prependAlert(msg.data);
        } else if (msg.type === 'trade_log') {
            this._prependTradeLog(msg.data);
        }
    }

    // =========================================================
    // Full UI update from state snapshot
    // =========================================================

    updateUI(data) {
        if (!data) return;
        this._updateAccount(data.account);
        this._updateDailyPnl(data.account);
        this._updateAISignal(data.ai_signal);
        this._updateSentiment(data.sentiment);
        this._updateAutoTrade(data.auto_trade);
        this._updateKillSwitch(data.kill_switch_active);
        this._updateMarketIndex(data.market_index);
        this._updatePositions(data.positions);
        this._updateTradeLogs(data.trade_logs);
        this._updateAlerts(data.alerts);
        this._updateMarketStatus(data.system);
    }

    // =========================================================
    // Account summary card
    // =========================================================

    _updateAccount(account) {
        if (!account) return;
        const a = account;

        this._setFlashText('total-asset', this._fmtKRW(a.total_asset));
        this._setFlashText('deposit',     this._fmtKRW(a.deposit));

        const rateEl = document.getElementById('profit-rate');
        if (rateEl) {
            const rate = a.profit_rate || 0;
            rateEl.textContent = this._fmtRate(rate);
            rateEl.className   = rate >= 0 ? 'card-value text-up' : 'card-value text-down';
        }
    }

    // =========================================================
    // Daily P&L card
    // =========================================================

    _updateDailyPnl(account) {
        if (!account) return;

        this._setPnlText('realized-pnl',   account.realized_pnl);
        this._setPnlText('unrealized-pnl', account.unrealized_pnl);

        const dayRateEl = document.getElementById('day-profit-rate');
        if (dayRateEl) {
            const r = account.day_profit_rate || 0;
            dayRateEl.textContent = this._fmtRate(r);
            dayRateEl.className   = r >= 0 ? 'card-value text-up' : 'card-value text-down';
        }
    }

    _setPnlText(id, value) {
        const el = document.getElementById(id);
        if (!el) return;
        const v = value || 0;
        el.textContent = (v >= 0 ? '+' : '') + this._fmtKRW(v);
        el.className   = v >= 0 ? 'card-value text-up' : 'card-value text-down';
    }

    // =========================================================
    // AI Signal card
    // =========================================================

    _updateAISignal(signal) {
        if (!signal) return;

        const typeEl = document.getElementById('signal-type');
        if (typeEl) {
            const type = signal.signal_type || 'hold';
            const labelMap = { buy: '매수', sell: '매도', hold: '관망' };
            typeEl.textContent = labelMap[type] || type.toUpperCase();
            typeEl.className   = 'signal-main ' + this._signalClass(type);
        }

        const confidence = Math.min(Math.max(signal.confidence || 0, 0), 1);
        const confPct = Math.round(confidence * 100);

        const confBar = document.getElementById('signal-confidence-bar');
        const confLbl = document.getElementById('signal-confidence-label');
        if (confBar) confBar.style.width = confPct + '%';
        if (confLbl) confLbl.textContent = confPct + '%';

        this._setText('signal-reasoning', signal.reasoning || '-');
    }

    _signalClass(type) {
        return { buy: 'text-up', sell: 'text-down', hold: 'text-neutral' }[type] || 'text-neutral';
    }

    // =========================================================
    // Market Sentiment card
    // =========================================================

    _updateSentiment(sentiment) {
        if (!sentiment) return;

        const score = sentiment.score || 0;  // -1.0 ~ +1.0
        const scoreEl = document.getElementById('sentiment-score');
        if (scoreEl) {
            scoreEl.textContent = score.toFixed(2);
            scoreEl.className   = score > 0.1 ? 'card-value text-up'
                                : score < -0.1 ? 'card-value text-down'
                                : 'card-value text-neutral';
        }

        const labelEl = document.getElementById('sentiment-label');
        if (labelEl) {
            labelEl.textContent = score > 0.1 ? '긍정' : score < -0.1 ? '부정' : '중립';
        }

        this._setText('sentiment-news-count', (sentiment.news_count || 0) + '건 분석');

        // Gauge needle: map -1..+1 to 5%..95%
        const needle = document.getElementById('sentiment-needle');
        if (needle) {
            const pct = Math.round(((score + 1) / 2) * 90 + 5);
            needle.style.left = pct + '%';
        }
    }

    // =========================================================
    // Auto-trade control panel
    // =========================================================

    _updateAutoTrade(autoTrade) {
        if (!autoTrade) return;

        const isRunning = autoTrade.is_running === true;
        const statusEl  = document.getElementById('autotrade-status-badge');
        if (statusEl) {
            statusEl.textContent = isRunning ? '실행 중' : '정지';
            statusEl.className   = isRunning ? 'badge badge-online' : 'badge badge-system';
        }

        const statusWrap = document.getElementById('autotrade-status-wrap');
        if (statusWrap) {
            statusWrap.className = isRunning ? 'auto-trade-status running' : 'auto-trade-status stopped';
        }

        this._setText('strategy-name', autoTrade.strategy_name || '-');

        const btnStart = document.getElementById('btn-autotrade-start');
        const btnStop  = document.getElementById('btn-autotrade-stop');
        if (btnStart) btnStart.disabled = isRunning;
        if (btnStop)  btnStop.disabled  = !isRunning;

        // Daily loss limit progress bar
        const limit     = autoTrade.daily_loss_limit || 0;
        const current   = Math.abs(autoTrade.current_loss || 0);
        const pct       = limit > 0 ? Math.min(Math.round((current / limit) * 100), 100) : 0;
        const lossBar   = document.getElementById('daily-loss-bar');
        const lossLabel = document.getElementById('daily-loss-label');
        if (lossBar)   lossBar.style.width = pct + '%';
        if (lossLabel) lossLabel.textContent = `${this._fmtKRW(current)} / ${this._fmtKRW(limit)} (${pct}%)`;
    }

    // =========================================================
    // Kill Switch
    // =========================================================

    _updateKillSwitch(active) {
        const btn      = document.getElementById('btn-kill-on');
        const btnOff   = document.getElementById('btn-kill-off');
        const statusEl = document.getElementById('kill-status');

        if (btn) {
            if (active) {
                btn.classList.add('active');
                btn.title = '킬 스위치 발동 중';
            } else {
                btn.classList.remove('active');
                btn.title = '킬 스위치 활성화';
            }
        }

        if (btnOff) {
            btnOff.classList.toggle('hidden', !active);
        }

        if (statusEl) {
            statusEl.textContent = active ? '발동 중' : '대기';
            statusEl.className   = active ? 'badge badge-danger' : 'badge badge-system';
        }
    }

    // =========================================================
    // Market Index
    // =========================================================

    _updateMarketIndex(marketIndex) {
        if (!marketIndex) return;

        const indices = [
            { key: 'kospi',  priceId: 'kospi-price',  changeId: 'kospi-change' },
            { key: 'kosdaq', priceId: 'kosdaq-price', changeId: 'kosdaq-change' },
        ];

        indices.forEach(({ key, priceId, changeId }) => {
            const idx = marketIndex[key];
            if (!idx) return;

            const priceEl  = document.getElementById(priceId);
            const changeEl = document.getElementById(changeId);
            const rate     = idx.change_rate || 0;

            if (priceEl)  priceEl.textContent  = this._fmtNum(idx.price || 0);
            if (changeEl) {
                changeEl.textContent = (rate >= 0 ? '+' : '') + rate.toFixed(2) + '%';
                changeEl.className   = 'market-index-change ' + (rate >= 0 ? 'text-up' : 'text-down');
            }
        });
    }

    // =========================================================
    // Positions table
    // =========================================================

    _updatePositions(positions) {
        const tbody = document.querySelector('#positions-table tbody');
        if (!tbody) return;

        if (!positions || positions.length === 0) {
            tbody.innerHTML = '<tr class="empty-row"><td colspan="6">보유 종목 없음</td></tr>';
            return;
        }

        tbody.innerHTML = '';
        positions.forEach((p) => {
            const rate     = p.profit_rate || 0;
            const rowClass = rate >= 0 ? 'row-up' : 'row-down';
            const tr       = document.createElement('tr');
            tr.className   = rowClass;
            tr.innerHTML = `
                <td>${this._esc(p.name || p.symbol || '-')}</td>
                <td>${this._fmtNum(p.quantity || 0)}</td>
                <td>${this._fmtKRW(p.avg_price || 0)}</td>
                <td>${this._fmtKRW(p.current_price || 0)}</td>
                <td class="${rate >= 0 ? 'text-up' : 'text-down'}">${this._fmtRate(rate)}</td>
                <td>${this._fmtKRW(p.eval_amount || 0)}</td>
            `;
            tbody.appendChild(tr);
        });
    }

    // =========================================================
    // Trade logs
    // =========================================================

    _updateTradeLogs(logs) {
        const tbody = document.querySelector('#trade-log-table tbody');
        if (!tbody) return;

        if (!logs || logs.length === 0) {
            tbody.innerHTML = '<tr class="empty-row"><td colspan="5">매매 내역 없음</td></tr>';
            return;
        }

        tbody.innerHTML = '';
        // Show up to 20 entries; most recent first
        const recent = logs.slice(0, 20);
        recent.forEach((log) => {
            tbody.appendChild(this._buildTradeRow(log));
        });
    }

    _prependTradeLog(log) {
        const tbody = document.querySelector('#trade-log-table tbody');
        if (!tbody) return;

        // Remove "no records" row if present
        const emptyRow = tbody.querySelector('.empty-row');
        if (emptyRow) emptyRow.remove();

        const tr = this._buildTradeRow(log);
        tr.classList.add('trade-log-new');
        tbody.insertBefore(tr, tbody.firstChild);

        // Keep max 20 rows
        while (tbody.rows.length > 20) tbody.deleteRow(tbody.rows.length - 1);
    }

    _buildTradeRow(log) {
        const action   = log.action || '';
        const badgeMap = { buy: 'badge-up', sell: 'badge-down', signal: 'badge-gold' };
        const labelMap = { buy: '매수', sell: '매도', signal: '시그널' };
        const badgeCls = badgeMap[action] || 'badge-system';
        const label    = labelMap[action] || action;

        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${this._fmtTime(log.timestamp)}</td>
            <td><span class="badge ${badgeCls}">${this._esc(label)}</span></td>
            <td>${this._esc(log.symbol || '-')}</td>
            <td>${this._fmtKRW(log.price || 0)}</td>
            <td>${this._fmtNum(log.quantity || 0)}</td>
        `;
        return tr;
    }

    // =========================================================
    // Alerts panel
    // =========================================================

    _updateAlerts(alerts) {
        const list = document.getElementById('alert-list');
        if (!list) return;

        if (!alerts || alerts.length === 0) {
            list.innerHTML = '<div class="alert-item"><div class="alert-body"><div class="alert-message text-muted">알림 없음</div></div></div>';
            this._updateAlertBadge(0);
            return;
        }

        list.innerHTML = '';
        alerts.forEach((al) => {
            list.appendChild(this._buildAlertItem(al));
        });

        const unread = alerts.filter(a => !a.is_read).length;
        this._updateAlertBadge(unread);
    }

    _prependAlert(alert) {
        const list = document.getElementById('alert-list');
        if (!list) return;

        // Remove "no alerts" placeholder
        const placeholder = list.querySelector('.text-muted');
        if (placeholder) list.innerHTML = '';

        const item = this._buildAlertItem(alert);
        list.insertBefore(item, list.firstChild);

        // Increment unread badge
        const badge = document.getElementById('alert-badge');
        if (badge) {
            const cur = parseInt(badge.textContent) || 0;
            this._updateAlertBadge(cur + 1);
        }
    }

    _buildAlertItem(al) {
        const catMap = {
            trade:    { cls: 'cat-trade',    icon: '\u25CF' },
            analysis: { cls: 'cat-analysis', icon: '\u25B2' },
            system:   { cls: 'cat-system',   icon: '\u25A0' },
            danger:   { cls: 'cat-danger',   icon: '\u26A0' },
        };
        const cfg = catMap[al.category] || catMap['system'];
        const div = document.createElement('div');
        div.className = `alert-item ${cfg.cls}${al.is_read ? '' : ' unread'}`;
        div.innerHTML = `
            <div class="alert-icon">${cfg.icon}</div>
            <div class="alert-body">
                <div class="alert-message">${this._esc(al.message || '')}</div>
                <div class="alert-time">${this._fmtTime(al.created_at)}</div>
            </div>
        `;
        return div;
    }

    _updateAlertBadge(count) {
        const badge = document.getElementById('alert-badge');
        if (!badge) return;
        badge.textContent = count;
        badge.classList.toggle('hidden', count === 0);
    }

    // =========================================================
    // Market status badge
    // =========================================================

    _updateMarketStatus(system) {
        if (!system) return;
        const el = document.getElementById('market-status-badge');
        if (!el) return;

        const statusMap = {
            open:        { label: '개장', cls: 'badge badge-online' },
            closed:      { label: '폐장', cls: 'badge badge-system' },
            pre_market:  { label: '장전', cls: 'badge badge-gold' },
            post_market: { label: '장후', cls: 'badge badge-gold' },
        };
        const cfg = statusMap[system.market_status] || statusMap['closed'];
        el.textContent = cfg.label;
        el.className   = cfg.cls;
    }

    // =========================================================
    // API calls (REST)
    // =========================================================

    async apiCall(method, path, body) {
        const options = {
            method,
            headers: {
                'Content-Type':  'application/json',
                'Authorization': `Bearer ${this.token}`,
            },
        };
        if (body !== undefined) options.body = JSON.stringify(body);

        const res = await fetch(path, options);

        if (res.status === 401) {
            localStorage.removeItem('stokai_token');
            window.location.href = '/login';
            return null;
        }

        try {
            return await res.json();
        } catch {
            return null;
        }
    }

    async startAutoTrade() {
        const btn = document.getElementById('btn-autotrade-start');
        if (btn) btn.disabled = true;
        const result = await this.apiCall('POST', '/api/autotrade/start', { strategy_name: 'default' });
        if (!result || result.status === 'error') {
            console.error('[API] startAutoTrade failed:', result);
            if (btn) btn.disabled = false;
        }
    }

    async stopAutoTrade() {
        const btn = document.getElementById('btn-autotrade-stop');
        if (btn) btn.disabled = true;
        const result = await this.apiCall('POST', '/api/autotrade/stop');
        if (!result || result.status === 'error') {
            console.error('[API] stopAutoTrade failed:', result);
            if (btn) btn.disabled = false;
        }
    }

    async killSwitchOn() {
        if (!confirm('킬 스위치를 활성화하면 모든 자동매매가 즉시 중단됩니다.\n계속하시겠습니까?')) return;
        await this.apiCall('POST', '/api/kill-switch/on');
    }

    async killSwitchOff() {
        await this.apiCall('POST', '/api/kill-switch/off');
    }

    async logout() {
        try {
            await this.apiCall('POST', '/api/logout');
        } catch (e) {
            // ignore errors on logout
        }
        if (this.wsManager) this.wsManager.disconnect();
        if (this._clockTimer) clearInterval(this._clockTimer);
        localStorage.removeItem('stokai_token');
        window.location.href = '/login';
    }

    // =========================================================
    // Formatting helpers
    // =========================================================

    /** Korean currency format: 1234567 -> "1,234,567" */
    _fmtKRW(value) {
        if (typeof value !== 'number' || isNaN(value)) return '0';
        return Math.round(value).toLocaleString('ko-KR');
    }

    /** General number format */
    _fmtNum(value) {
        if (typeof value !== 'number' || isNaN(value)) return '0';
        return value.toLocaleString('ko-KR');
    }

    /** Rate format: +1.23% or -1.23% */
    _fmtRate(value) {
        if (typeof value !== 'number' || isNaN(value)) return '0.00%';
        return (value >= 0 ? '+' : '') + value.toFixed(2) + '%';
    }

    /** Timestamp: ISO string -> "HH:MM:SS" */
    _fmtTime(ts) {
        if (!ts) return '-';
        try {
            const d = new Date(ts);
            if (isNaN(d)) return ts.substring(0, 19);
            const pad = (n) => String(n).padStart(2, '0');
            return `${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`;
        } catch {
            return '-';
        }
    }

    /** XSS-safe string escape */
    _esc(str) {
        return String(str)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;');
    }

    // =========================================================
    // DOM helpers
    // =========================================================

    _setText(id, text) {
        const el = document.getElementById(id);
        if (el) el.textContent = text;
    }

    /**
     * Set text and briefly flash the element if the value changed.
     * Flash direction is determined by whether new value > old value.
     */
    _setFlashText(id, text) {
        const el = document.getElementById(id);
        if (!el) return;

        const prev = this._prevValues[id];
        if (prev !== undefined && prev !== text) {
            // Parse numeric values for direction comparison
            const prevNum = parseFloat(String(prev).replace(/,/g, ''));
            const nextNum = parseFloat(String(text).replace(/,/g, ''));
            el.classList.remove('value-flash-up', 'value-flash-down');
            // Force reflow to restart animation
            void el.offsetWidth;
            if (!isNaN(prevNum) && !isNaN(nextNum)) {
                el.classList.add(nextNum >= prevNum ? 'value-flash-up' : 'value-flash-down');
            }
        }

        el.textContent = text;
        this._prevValues[id] = text;
    }
}

// =========================================================
// Bootstrap: instantiate once DOM is ready
// =========================================================
document.addEventListener('DOMContentLoaded', () => {
    window.dashboard = new StokAIDashboard();
});
