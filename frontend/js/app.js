/* Main SPA logic for the AI Resume Builder.
   Single Alpine component covering every view: dashboard, editor (with live
   preview + live ATS), match, cover letter, templates, chat, settings. */

const TEMPLATES = [
    { key: 'modern',   name: 'Modern',   desc: 'Blue banner header, bold sections.', primary: '#1F4E79' },
    { key: 'classic',  name: 'Classic',  desc: 'Times-Roman, conservative layout.',  primary: '#000000' },
    { key: 'minimal',  name: 'Minimal',  desc: 'Lots of whitespace, thin rules.',    primary: '#111111' },
    { key: 'creative', name: 'Creative', desc: 'Magenta accent sidebar, modern.',    primary: '#B83280' },
];

function emptyResume() {
    return {
        personal: { name: '', title: '', email: '', phone: '', location: '',
                    linkedin: '', github: '', website: '' },
        summary: '',
        experience: [],
        education: [],
        projects: [],
        skills: [],
        certifications: [],
        languages: [],
        awards: [],
    };
}

document.addEventListener('alpine:init', () => {
    Alpine.data('appShell', () => ({
        // ---------- State ----------
        user: null,
        ready: false,
        view: 'dashboard',
        templates: TEMPLATES,
        skillsList: [],

        resumes: [],
        currentId: null,
        currentTitle: 'Untitled Resume',
        currentTemplate: 'modern',
        currentIsPublic: false,
        currentShareToken: '',
        resume: emptyResume(),

        atsReport: null,
        matchReport: null,
        jobDescription: '',
        companyName: '',
        coverLetter: '',
        chatMessages: [
            { role: 'ai', text: "Hi! I'm your resume coach. Ask me about summaries, weak bullets, ATS scores, or job tailoring." },
        ],
        chatInput: '',

        saving: false,
        atsBusy: false,
        savedAt: null,
        theme: localStorage.getItem('arb_theme') || 'light',

        // Debounce timers
        _saveTimer: null,
        _atsTimer: null,

        // ---------- Init ----------
        async init() {
            try {
                this.user = await API.me();
            } catch {
                location.href = '/login';
                return;
            }
            await this.loadResumes();
            try { this.skillsList = (await API.skillsList()).skills || []; } catch {}
            this.ready = true;
            // Watch for resume edits → auto-save + live ATS
            this.$watch('resume', () => this.scheduleSave(), { deep: true });
            this.$watch('currentTitle',    () => this.scheduleSave());
            this.$watch('currentTemplate', () => this.scheduleSave());
        },

        // ---------- Theme ----------
        toggleTheme() { this.theme = API.toggleTheme(); },

        // ---------- Auth ----------
        logout() {
            API.clearAuth();
            API.toast('Signed out', 'info');
            setTimeout(() => location.href = '/', 200);
        },

        // ---------- Resume list ----------
        async loadResumes() {
            this.resumes = await API.listResumes();
        },
        async newResume() {
            const created = await API.createResume({
                title: 'Untitled Resume', template: 'modern', data: emptyResume(),
            });
            await this.loadResumes();
            this.openResume(created.id);
            API.toast('New resume created', 'good');
        },
        async loadSample() {
            // Bundled tiny sample.
            const sample = {
                personal: { name: 'Alex Kumar', title: 'Senior Software Engineer',
                            email: 'alex@example.com', phone: '+1 555 0142',
                            location: 'San Francisco, CA',
                            linkedin: 'linkedin.com/in/alexkumar',
                            github: 'github.com/alexkumar', website: 'alexkumar.dev' },
                summary: 'Senior Software Engineer with 7+ years building scalable distributed systems.',
                experience: [{
                    role: 'Senior Software Engineer', company: 'Lumen Labs',
                    start: '2022', end: 'Present', location: 'San Francisco, CA',
                    bullets: [
                        'Led the redesign of the core inference service, reducing p99 latency from 850ms to 180ms.',
                        'Architected a multi-tenant feature-flag platform used by 8 product teams.',
                        'Mentored 4 junior engineers; 2 promoted within a year.',
                    ],
                }, {
                    role: 'Software Engineer', company: 'BrightPath',
                    start: '2019', end: '2022', location: 'Remote',
                    bullets: [
                        'Built recommendation pipeline serving 12M users daily with 99.95% uptime.',
                        'Drove migration from monolith to microservices on Kubernetes.',
                    ],
                }],
                education: [{ school: 'University of Michigan', degree: 'B.S.', field: 'Computer Science',
                              start: '2013', end: '2017', gpa: '3.8', details: "Dean's List 6 semesters." }],
                projects: [], certifications: [], languages: [], awards: [],
                skills: ['Python','Go','TypeScript','FastAPI','PostgreSQL','Redis','Kafka',
                         'Kubernetes','Docker','AWS','Terraform','GraphQL','REST API',
                         'Machine Learning','MLOps','System Design','Leadership'],
            };
            const created = await API.createResume({ title: 'Sample resume', template: 'modern', data: sample });
            await this.loadResumes();
            this.openResume(created.id);
            API.toast('Sample loaded', 'good');
        },
        async openResume(id) {
            const r = await API.getResume(id);
            this.currentId = r.id;
            this.currentTitle = r.title;
            this.currentTemplate = r.template;
            this.currentIsPublic = r.is_public;
            this.currentShareToken = r.share_token;
            this.resume = { ...emptyResume(), ...r.data };
            // Ensure all collections exist
            ['experience','education','projects','skills','certifications','languages','awards'].forEach(k => {
                if (!Array.isArray(this.resume[k])) this.resume[k] = [];
            });
            this.view = 'editor';
            this.atsReport = null;
            this.matchReport = null;
            this.scheduleAts(0);
        },
        async deleteResume(id) {
            if (!confirm('Delete this resume? This cannot be undone.')) return;
            await API.deleteResume(id);
            if (this.currentId === id) { this.currentId = null; this.view = 'dashboard'; }
            await this.loadResumes();
            API.toast('Resume deleted', 'info');
        },
        async duplicateResume(id) {
            const r = await API.duplicateResume(id);
            await this.loadResumes();
            API.toast(`Duplicated as "${r.title}"`, 'good');
        },
        async togglePublic() {
            const next = !this.currentIsPublic;
            const r = await API.updateResume(this.currentId, { is_public: next });
            this.currentIsPublic = r.is_public;
            this.currentShareToken = r.share_token;
            API.toast(next ? 'Share link enabled' : 'Share link disabled', 'info');
        },

        // ---------- Auto-save / live ATS ----------
        scheduleSave() {
            if (!this.currentId) return;
            this.saving = true;
            clearTimeout(this._saveTimer);
            this._saveTimer = setTimeout(() => this.doSave(), 1200);
            this.scheduleAts();
        },
        async doSave() {
            try {
                await API.updateResume(this.currentId, {
                    title: this.currentTitle,
                    template: this.currentTemplate,
                    data: this.resume,
                });
                this.savedAt = new Date();
                // Refresh sidebar list timestamps quietly.
                this.loadResumes();
            } catch (e) { API.toast('Save failed: ' + e.message, 'bad'); }
            finally { this.saving = false; }
        },
        scheduleAts(delay = 800) {
            clearTimeout(this._atsTimer);
            this._atsTimer = setTimeout(async () => {
                this.atsBusy = true;
                try { this.atsReport = await API.ats(this.resume); }
                catch {} finally { this.atsBusy = false; }
            }, delay);
        },

        // ---------- Editor mutations ----------
        addExperience() {
            this.resume.experience.push({ role:'', company:'', start:'', end:'', location:'', bullets:[] });
        },
        addBullet(idx) { this.resume.experience[idx].bullets.push(''); },
        removeBullet(j, b) { this.resume.experience[j].bullets.splice(b, 1); },
        removeExperience(i) { this.resume.experience.splice(i, 1); },

        addEducation() {
            this.resume.education.push({ school:'', degree:'', field:'', start:'', end:'', gpa:'', details:'' });
        },
        removeEducation(i) { this.resume.education.splice(i, 1); },

        addProject() {
            this.resume.projects.push({ name:'', description:'', link:'', tech:[], bullets:[] });
        },
        removeProject(i) { this.resume.projects.splice(i, 1); },
        techString(p) { return (p.tech || []).join(', '); },
        setTechString(p, val) { p.tech = val.split(',').map(s => s.trim()).filter(Boolean); },

        addCert()  { this.resume.certifications.push({ name:'', issuer:'', year:'' }); },
        addAward() { this.resume.awards.push({ name:'', year:'', description:'' }); },
        addLang()  { this.resume.languages.push({ name:'', level:'' }); },

        skillsString() { return (this.resume.skills || []).join(', '); },
        setSkillsString(val) {
            this.resume.skills = val.split(',').map(s => s.trim()).filter(Boolean);
        },

        // ---------- AI actions ----------
        async generateSummary() {
            try {
                const r = await API.genSummary(this.resume);
                this.resume.summary = r.summary;
                API.toast('Summary generated', 'good');
            } catch (e) { API.toast(e.message, 'bad'); }
        },
        async enhanceBullet(jobIdx, bIdx) {
            try {
                const job = this.resume.experience[jobIdx];
                const r = await API.enhanceBullet(job.bullets[bIdx], job.role || '');
                job.bullets[bIdx] = r.enhanced;
                API.toast('Bullet rewritten', 'good');
            } catch (e) { API.toast(e.message, 'bad'); }
        },
        async enhanceAllBullets(jobIdx) {
            const job = this.resume.experience[jobIdx];
            for (let i = 0; i < job.bullets.length; i++) {
                try {
                    const r = await API.enhanceBullet(job.bullets[i], job.role || '');
                    job.bullets[i] = r.enhanced;
                } catch {}
            }
            API.toast(`Rewrote ${job.bullets.length} bullets`, 'good');
        },
        async suggestSkills() {
            try {
                const r = await API.suggestSkills(this.resume);
                if (!r.suggestions?.length) { API.toast('No new skills to suggest', 'info'); return; }
                const newSkills = r.suggestions.filter(s =>
                    !this.resume.skills.map(x => x.toLowerCase()).includes(s.toLowerCase())
                );
                this.resume.skills.push(...newSkills);
                API.toast(`Added ${newSkills.length} skill(s)`, 'good');
            } catch (e) { API.toast(e.message, 'bad'); }
        },

        // ---------- Match ----------
        async runMatch() {
            if (!this.jobDescription.trim()) { API.toast('Paste a job description first', 'warn'); return; }
            try {
                this.matchReport = await API.match(this.resume, this.jobDescription);
            } catch (e) { API.toast(e.message, 'bad'); }
        },

        // ---------- Cover letter ----------
        async generateCover() {
            if (!this.jobDescription.trim()) { API.toast('Paste a job description first', 'warn'); return; }
            try {
                const r = await API.genCover(this.resume, this.jobDescription, this.companyName);
                this.coverLetter = r.letter;
                API.toast('Cover letter drafted', 'good');
            } catch (e) { API.toast(e.message, 'bad'); }
        },
        async downloadCoverPdf() {
            try {
                const blob = await API.coverLetterPdf(this.coverLetter, this.user?.name || '', this.currentTemplate);
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url; a.download = 'cover_letter.pdf'; a.click();
                URL.revokeObjectURL(url);
            } catch (e) { API.toast(e.message, 'bad'); }
        },

        // ---------- PDF export ----------
        async downloadResumePdf() {
            try {
                const url = await API.pdfUrl(this.currentId);
                const a = document.createElement('a');
                a.href = url; a.download = `${this.currentTitle || 'resume'}.pdf`; a.click();
                setTimeout(() => URL.revokeObjectURL(url), 1000);
            } catch (e) { API.toast(e.message, 'bad'); }
        },
        downloadResumeJson() {
            const data = JSON.stringify({
                title: this.currentTitle, template: this.currentTemplate, ...this.resume,
            }, null, 2);
            const blob = new Blob([data], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url; a.download = `${this.currentTitle || 'resume'}.json`; a.click();
            setTimeout(() => URL.revokeObjectURL(url), 1000);
        },

        // ---------- Import / parse ----------
        async handleUpload(ev) {
            const file = ev.target.files?.[0];
            if (!file) return;
            try {
                const r = await API.parseUpload(file);
                if (!this.currentId) {
                    const created = await API.createResume({
                        title: file.name.replace(/\.[^.]+$/, ''),
                        template: 'modern',
                        data: r.resume,
                    });
                    await this.loadResumes();
                    this.openResume(created.id);
                } else {
                    this.resume = { ...emptyResume(), ...r.resume };
                    this.scheduleSave();
                    this.view = 'editor';
                }
                API.toast('Resume imported', 'good');
            } catch (e) { API.toast(e.message, 'bad'); }
            ev.target.value = '';
        },

        // ---------- Chat ----------
        async sendChat() {
            const msg = this.chatInput.trim();
            if (!msg) return;
            this.chatMessages.push({ role: 'user', text: msg });
            this.chatInput = '';
            try {
                const r = await API.chat(msg, this.resume);
                this.chatMessages.push({ role: 'ai', text: r.reply });
            } catch (e) {
                this.chatMessages.push({ role: 'ai', text: '(error: ' + e.message + ')' });
            }
            this.$nextTick(() => {
                const log = document.getElementById('chatLog');
                if (log) log.scrollTop = log.scrollHeight;
            });
        },

        // ---------- Helpers / formatters ----------
        chipFor(score) {
            if (score >= 80) return 'chip chip-good';
            if (score >= 60) return 'chip chip-warn';
            return 'chip chip-bad';
        },
        gaugeColor(score) {
            if (score >= 80) return '#10b981';
            if (score >= 60) return '#f59e0b';
            return '#ef4444';
        },
        formatTime(t) {
            if (!t) return '';
            const d = new Date(t);
            const mins = Math.round((Date.now() - d.getTime()) / 60000);
            if (mins < 1) return 'just now';
            if (mins < 60) return mins + ' min ago';
            return d.toLocaleString();
        },
        currentResumeMeta() {
            return this.resumes.find(r => r.id === this.currentId);
        },
        get shareUrl() {
            return location.origin + '/share/' + this.currentShareToken;
        },
        copyShare() {
            navigator.clipboard.writeText(this.shareUrl);
            API.toast('Share link copied', 'good');
        },
    }));
});
