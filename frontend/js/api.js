/* ResuMate AI — API client v3 */

window.API = (() => {
    const BASE = '';
    const TOKEN_KEY = 'arb_token';
    const USER_KEY  = 'arb_user';

    function getToken() { return localStorage.getItem(TOKEN_KEY); }
    function getUser()  { try { return JSON.parse(localStorage.getItem(USER_KEY) || 'null'); } catch { return null; } }
    function setAuth(token, user) {
        localStorage.setItem(TOKEN_KEY, token);
        localStorage.setItem(USER_KEY, JSON.stringify(user));
    }
    function clearAuth() {
        localStorage.removeItem(TOKEN_KEY);
        localStorage.removeItem(USER_KEY);
    }

    async function request(path, { method = 'GET', body, headers = {}, raw = false } = {}) {
        const opts = { method, headers: { ...headers } };
        const token = getToken();
        if (token) opts.headers.Authorization = `Bearer ${token}`;
        if (body !== undefined) {
            if (body instanceof FormData) {
                opts.body = body;
            } else {
                opts.headers['Content-Type'] = 'application/json';
                opts.body = JSON.stringify(body);
            }
        }
        const res = await fetch(BASE + path, opts);
        if (raw) return res;
        if (res.status === 401) {
            clearAuth();
            if (!location.pathname.startsWith('/login') && !location.pathname.startsWith('/register')) {
                location.href = '/login';
            }
            throw new Error('Unauthorized');
        }
        if (!res.ok) {
            let detail = `HTTP ${res.status}`;
            try { const j = await res.json(); detail = j.detail || detail; } catch {}
            throw new Error(detail);
        }
        if (res.status === 204) return null;
        const ct = res.headers.get('Content-Type') || '';
        if (ct.includes('application/json')) return res.json();
        return res.text();
    }

    // ── Toast ──
    function ensureStack() {
        let el = document.querySelector('.toast-stack');
        if (!el) { el = document.createElement('div'); el.className = 'toast-stack'; document.body.appendChild(el); }
        return el;
    }
    function toast(message, kind = 'info', ttl = 3500) {
        const stack = ensureStack();
        const el = document.createElement('div');
        el.className = `toast ${kind}`;
        el.textContent = message;
        stack.appendChild(el);
        setTimeout(() => {
            el.style.opacity = '0'; el.style.transition = 'opacity .2s ease';
            setTimeout(() => el.remove(), 220);
        }, ttl);
    }

    // ── Theme ──
    function applyTheme(theme) {
        const t = theme || localStorage.getItem('arb_theme') || 'light';
        document.documentElement.classList.toggle('dark', t === 'dark');
        localStorage.setItem('arb_theme', t);
        return t;
    }
    function toggleTheme() {
        const cur = localStorage.getItem('arb_theme') || 'light';
        return applyTheme(cur === 'dark' ? 'light' : 'dark');
    }
    function getTheme() { return localStorage.getItem('arb_theme') || 'light'; }

    // ── Format date ──
    function fmtDate(iso) {
        if (!iso) return '—';
        const d = new Date(iso);
        return d.toLocaleDateString('en-IN', { day:'numeric', month:'short', year:'numeric' });
    }
    function fmtDateTime(iso) {
        if (!iso) return '—';
        const d = new Date(iso);
        return d.toLocaleDateString('en-IN', { day:'numeric', month:'short', year:'numeric', hour:'2-digit', minute:'2-digit' });
    }
    function timeAgo(iso) {
        if (!iso) return '—';
        const secs = Math.round((Date.now() - new Date(iso)) / 1000);
        if (secs < 60)    return `${secs}s ago`;
        if (secs < 3600)  return `${Math.floor(secs/60)}m ago`;
        if (secs < 86400) return `${Math.floor(secs/3600)}h ago`;
        return `${Math.floor(secs/86400)}d ago`;
    }

    return {
        getToken, getUser, setAuth, clearAuth,
        toast, applyTheme, toggleTheme, getTheme,
        fmtDate, fmtDateTime, timeAgo,

        // Auth
        register: (email, name, password) =>
            request('/api/auth/register', { method:'POST', body:{email, name, password} }),
        login: (email, password) =>
            request('/api/auth/login', { method:'POST', body:{email, password} }),
        me: () => request('/api/auth/me'),
        updateProfile: (data) =>
            request('/api/auth/profile', { method:'PUT', body:data }),
        changePassword: (current_password, new_password) =>
            request('/api/auth/change-password', { method:'POST', body:{current_password, new_password} }),

        // Resumes
        listResumes:      ()            => request('/api/resumes'),
        getResume:        (id)          => request(`/api/resumes/${id}`),
        createResume:     (payload)     => request('/api/resumes', { method:'POST', body:payload }),
        updateResume:     (id, payload) => request(`/api/resumes/${id}`, { method:'PUT', body:payload }),
        deleteResume:     (id)          => request(`/api/resumes/${id}`, { method:'DELETE' }),
        duplicateResume:  (id)          => request(`/api/resumes/${id}/duplicate`, { method:'POST' }),
        getShared:        (token)       => request(`/api/resumes/share/${token}`),

        // Analysis
        ats:   (resume)      => request('/api/analyze/ats',   { method:'POST', body:{resume} }),
        match: (resume, jd)  => request('/api/analyze/match', { method:'POST', body:{resume, job_description:jd} }),

        // AI
        enhanceBullet: (bullet, role_hint) =>
            request('/api/ai/enhance-bullet', { method:'POST', body:{bullet, role_hint} }),
        genSummary: (resume) =>
            request('/api/ai/summary', { method:'POST', body:{resume} }),
        genCover:  (resume, jd, company) =>
            request('/api/ai/cover-letter', { method:'POST', body:{resume, job_description:jd, company} }),
        suggestSkills: (resume) =>
            request('/api/ai/suggest-skills', { method:'POST', body:{resume} }),
        skillsList: () => request('/api/ai/skill-suggestions'),
        chat: (message, resume) =>
            request('/api/ai/chat', { method:'POST', body:{message, resume} }),

        // Export
        async parseUpload(file) {
            const fd = new FormData(); fd.append('file', file);
            return request('/api/parse', { method:'POST', body:fd });
        },
        async pdfUrl(resumeId) {
            const t = getToken();
            return fetch(`/api/export/pdf/${resumeId}`, { headers:{ Authorization:`Bearer ${t}` } })
                .then(r => { if (!r.ok) throw new Error('PDF export failed'); return r.blob(); })
                .then(b => URL.createObjectURL(b));
        },
        async coverLetterPdf(text, name, template) {
            const t = getToken();
            const res = await fetch('/api/export/cover-letter/pdf', {
                method:'POST',
                headers:{'Content-Type':'application/json', Authorization:`Bearer ${t}`},
                body: JSON.stringify({text, name, template}),
            });
            if (!res.ok) throw new Error('Cover letter export failed');
            return res.blob();
        },

        // Admin
        adminStats:           ()               => request('/api/admin/stats'),
        adminGrowth:          (days=30)         => request(`/api/admin/growth?days=${days}`),
        adminUsers:           (skip=0,limit=50,search='') =>
            request(`/api/admin/users?skip=${skip}&limit=${limit}&search=${encodeURIComponent(search)}`),
        adminGetUser:         (id)              => request(`/api/admin/users/${id}`),
        adminUpdateUser:      (id, data)        => request(`/api/admin/users/${id}`, { method:'PATCH', body:data }),
        adminDeleteUser:      (id)              => request(`/api/admin/users/${id}`, { method:'DELETE' }),
        adminResumes:         (skip=0,limit=50) => request(`/api/admin/resumes?skip=${skip}&limit=${limit}`),
        adminDeleteResume:    (id)              => request(`/api/admin/resumes/${id}`, { method:'DELETE' }),
        adminActivity:        (skip=0,limit=50) => request(`/api/admin/activity?skip=${skip}&limit=${limit}`),

        health: () => request('/api/health'),
    };
})();

window.API.applyTheme();
