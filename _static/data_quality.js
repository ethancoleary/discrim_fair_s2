// Save users browser data
const browser = navigator.userAgent;

function saveBrowserData() {
    const browserField = document.getElementById('id_browser');
    if (browserField) {
        browserField.value = browser;
    }
}

// Page key
function getPageKey() {
    if (typeof PAGE_KEY !== 'undefined') {
        return PAGE_KEY;
    }
    const segments = window.location.pathname.split('/').filter(s => s);
    return segments.slice(-2).join('/');
}

// Global blur counter (persists across pages)
let warned = false;
const threshold = 3;  // or 1
let count = 0;

// Track if we are submitting the form (Next button)
window.IS_SUBMITTING = false;
document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function () {
            window.IS_SUBMITTING = true;
        });
    }

    // Load stored count and log into hidden fields
    const storedCount = localStorage.getItem('blur_count_global');
    count = storedCount ? parseInt(storedCount, 10) : 0;
    const blur_list_raw = localStorage.getItem('blur_pages');
    const blur_list = blur_list_raw ? JSON.parse(blur_list_raw) : [];
    const logField = document.getElementById('id_blur_log');
    const countField = document.getElementById('id_blur_count');
    if (logField) logField.value = JSON.stringify(blur_list);
    if (countField) countField.value = count;
});

// Count only when page actually becomes hidden (tab/window not visible)
document.addEventListener('visibilitychange', function () {
    // Only act when visibility is hidden and the document has *really* lost focus,
    // and we are not in the middle of a form submit/navigation.
    if (document.visibilityState !== 'hidden') return;
    if (document.hasFocus && document.hasFocus()) return;
    if (window.IS_SUBMITTING) return;

    const warnedField = document.getElementById('id_blur_warned');
    const logField = document.getElementById('id_blur_log');
    const countField = document.getElementById('id_blur_count');
    if (!logField || !countField || !warnedField) return;

    if (warnedField.value === '1') warned = true;

    // Increment global counter and persist it
    count++;
    localStorage.setItem('blur_count_global', String(count));

    // Append page key to list
    const key = getPageKey();
    let blur_list_raw = localStorage.getItem('blur_pages');
    let blur_list = blur_list_raw ? JSON.parse(blur_list_raw) : [];
    blur_list.push(key);
    localStorage.setItem('blur_pages', JSON.stringify(blur_list));

    // Update hidden fields
    logField.value = JSON.stringify(blur_list);
    countField.value = count;

    if (!warned && count >= threshold) {
        warned = true;
        warnedField.value = '1';
        alert(
          "We noticed you switched tabs or windows. Please stay on our experiment page " +
          "to ensure your full attention and that your data is recorded correctly."
        );
    }
});