/* Auth page controller */

document.addEventListener('alpine:init', () => {
    Alpine.data('authPage', () => ({
        mode: 'login',
        form: { name: '', email: '', password: '' },
        busy: false,
        error: '',

        init() {
            // If already logged in, go straight to app
            if (API.getToken()) { location.href = '/app'; return; }
            // Pre-select mode from URL path
            if (location.pathname === '/register') this.mode = 'register';
        },

        async submit() {
            this.error = '';
            this.busy  = true;
            try {
                let data;
                if (this.mode === 'login') {
                    data = await API.login(this.form.email, this.form.password);
                } else {
                    data = await API.register(this.form.email, this.form.name, this.form.password);
                }
                API.setAuth(data.access_token, data.user);
                location.href = '/app';
            } catch (e) {
                this.error = e.message || 'Something went wrong. Please try again.';
            } finally {
                this.busy = false;
            }
        },
    }));
});
