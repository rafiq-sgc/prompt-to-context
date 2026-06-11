// Context Engineering Learning Guide - Shared App JS

function toggleMobileMenu() {
    const nav = document.getElementById('nav-sidebar');
    if (nav) nav.classList.toggle('open');
}

document.addEventListener('click', function (event) {
    const nav = document.getElementById('nav-sidebar');
    const toggle = document.querySelector('.mobile-menu-toggle');
    if (nav && toggle &&
        !nav.contains(event.target) &&
        !toggle.contains(event.target) &&
        nav.classList.contains('open')) {
        nav.classList.remove('open');
    }
});

document.querySelectorAll('.nav-sidebar a').forEach(link => {
    link.addEventListener('click', function () {
        const nav = document.getElementById('nav-sidebar');
        if (nav && window.innerWidth <= 768) nav.classList.remove('open');
    });
});

// Tab panels (weak vs strong, failure vs fix)
document.querySelectorAll('[data-tab-group]').forEach(group => {
    const tabs = group.querySelectorAll('[data-tab]');
    const panels = group.querySelectorAll('[data-panel]');
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const target = tab.dataset.tab;
            tabs.forEach(t => t.classList.toggle('active', t.dataset.tab === target));
            panels.forEach(p => p.classList.toggle('active', p.dataset.panel === target));
        });
    });
});

// Collapsible sections
document.querySelectorAll('[data-collapse]').forEach(btn => {
    btn.addEventListener('click', () => {
        const target = document.getElementById(btn.dataset.collapse);
        if (target) {
            target.classList.toggle('open');
            btn.classList.toggle('open');
        }
    });
});

// Copy code blocks
document.querySelectorAll('.copy-btn').forEach(btn => {
    btn.addEventListener('click', async () => {
        const code = btn.closest('.code-block')?.querySelector('code')?.textContent;
        if (code) {
            await navigator.clipboard.writeText(code);
            const orig = btn.textContent;
            btn.textContent = 'Copied!';
            setTimeout(() => { btn.textContent = orig; }, 1500);
        }
    });
});

// Mermaid init
if (typeof mermaid !== 'undefined') {
    mermaid.initialize({
        startOnLoad: true,
        theme: 'base',
        themeVariables: {
            primaryColor: '#e0e7ff',
            primaryTextColor: '#1e1b4b',
            primaryBorderColor: '#6366f1',
            lineColor: '#6366f1',
            secondaryColor: '#ccfbf1',
            tertiaryColor: '#fef3c7'
        },
        flowchart: { useMaxWidth: true, htmlLabels: true, curve: 'basis' }
    });
}

// Reading progress bar
(function () {
    const bar = document.querySelector('.reading-progress');
    if (!bar) return;
    window.addEventListener('scroll', () => {
        const doc = document.documentElement;
        const scrolled = (doc.scrollTop / (doc.scrollHeight - doc.clientHeight)) * 100;
        bar.style.width = Math.min(100, scrolled) + '%';
    });
})();
