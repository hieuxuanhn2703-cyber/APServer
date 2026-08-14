/**
 * Server-Side Excel-Style Column Filtering for Dashboard Tables
 * - Reads filter configuration and distinct dataset options from server (via JSON script #excel-filter-config)
 * - Highlights active filter buttons with orange badge and funnel icon
 * - Allows searching inside filter options, Select All / Deselect All
 * - When "Áp dụng" is clicked, navigates to the URL with updated GET query parameters,
 *   filtering the entire dataset across the database and resetting that table's page to 1
 * - When changing pagination pages, all active filters are preserved
 * - When "Xóa lọc" is clicked, removes that column's parameter from URL and reloads
 */

(function() {
    'use strict';

    let filterConfig = {};
    let currentTable = null;
    let currentTableType = null;
    let currentColumn = null;
    let currentColConfig = null;
    let currentBtn = null;
    let popupEl = null;

    const SVG_DOWN_ARROW = `<svg viewBox="0 0 24 24" width="8" height="8" fill="currentColor"><path d="M7 10l5 5 5-5z"/></svg>`;
    const SVG_FUNNEL_ACTIVE = `<svg viewBox="0 0 24 24" width="9" height="9" fill="currentColor"><path d="M10 18h4v-2h-4v2zM3 6v2h18V6H3zm3 7h12v-2H6v2z"/></svg>`;

    function loadConfig() {
        const scriptEl = document.getElementById('excel-filter-config');
        if (scriptEl) {
            try {
                filterConfig = JSON.parse(scriptEl.textContent);
            } catch (e) {
                console.error("Error parsing excel-filter-config:", e);
                filterConfig = {};
            }
        }
    }

    function updateButtonIndicators() {
        const filterBtns = document.querySelectorAll('.excel-filter-btn');
        filterBtns.forEach(btn => {
            const table = btn.closest('table');
            const tableType = table ? table.getAttribute('data-table-type') : null;
            const colKey = btn.getAttribute('data-col');

            if (tableType && filterConfig[tableType] && filterConfig[tableType].columns[colKey]) {
                const colConf = filterConfig[tableType].columns[colKey];
                const selected = colConf.selected || [];
                if (selected.length > 0) {
                    btn.classList.add('is-filtered');
                    btn.innerHTML = SVG_FUNNEL_ACTIVE;
                    btn.title = `Đang lọc ${colConf.title}: ${selected.join(', ')}`;
                } else {
                    btn.classList.remove('is-filtered');
                    btn.innerHTML = SVG_DOWN_ARROW;
                    btn.title = `Lọc ${colConf.title}`;
                }
            }
        });
    }

    function createPopup() {
        if (popupEl) return;

        popupEl = document.createElement('div');
        popupEl.className = 'excel-filter-popup';
        popupEl.id = 'excel-filter-popup';
        popupEl.innerHTML = `
            <div class="ef-header">
                <span class="ef-title" id="ef-popup-title">Lọc dữ liệu</span>
                <button type="button" class="ef-close-btn" id="ef-close-btn" title="Đóng">&times;</button>
            </div>
            <div class="ef-search-box">
                <input type="text" class="ef-search-input" id="ef-search-input" placeholder="Tìm kiếm giá trị..." autocomplete="off">
            </div>
            <div class="ef-options-container">
                <label class="ef-option-item ef-select-all" id="ef-select-all-label">
                    <input type="checkbox" id="ef-check-all" checked>
                    <span>(Chọn tất cả)</span>
                </label>
                <div class="ef-list" id="ef-list"></div>
            </div>
            <div class="ef-footer">
                <button type="button" class="ef-btn ef-btn-clear" id="ef-btn-clear">Xóa lọc</button>
                <button type="button" class="ef-btn ef-btn-apply" id="ef-btn-apply">Áp dụng</button>
            </div>
        `;
        document.body.appendChild(popupEl);

        document.getElementById('ef-close-btn').addEventListener('click', hidePopup);
        document.getElementById('ef-btn-clear').addEventListener('click', clearCurrentColumnFilter);
        document.getElementById('ef-btn-apply').addEventListener('click', applyCurrentColumnFilter);

        const searchInput = document.getElementById('ef-search-input');
        searchInput.addEventListener('input', handleSearchInput);

        const checkAll = document.getElementById('ef-check-all');
        checkAll.addEventListener('change', function() {
            const isChecked = this.checked;
            const optionItems = popupEl.querySelectorAll('#ef-list .ef-option-item');
            optionItems.forEach(item => {
                if (item.style.display !== 'none') {
                    const cb = item.querySelector('input[type="checkbox"]');
                    if (cb) cb.checked = isChecked;
                }
            });
        });

        // Close on click outside
        document.addEventListener('click', function(e) {
            if (!popupEl || popupEl.style.display === 'none') return;
            if (popupEl.contains(e.target)) return;
            if (currentBtn && currentBtn.contains(e.target)) return;
            hidePopup();
        });

        // Close on escape key
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && popupEl && popupEl.style.display !== 'none') {
                hidePopup();
            }
        });
    }

    function handleSearchInput(e) {
        const query = e.target.value.trim().toLowerCase();
        const optionItems = popupEl.querySelectorAll('#ef-list .ef-option-item');
        let visibleCount = 0;

        optionItems.forEach(item => {
            const val = item.getAttribute('data-value') || '';
            if (!query || val.toLowerCase().includes(query)) {
                item.style.display = 'flex';
                visibleCount++;
            } else {
                item.style.display = 'none';
            }
        });

        const selectAllLabel = document.getElementById('ef-select-all-label');
        selectAllLabel.style.display = visibleCount > 0 ? 'flex' : 'none';
        updateCheckAllState();
    }

    function updateCheckAllState() {
        const checkAll = document.getElementById('ef-check-all');
        const visibleCbs = Array.from(popupEl.querySelectorAll('#ef-list .ef-option-item'))
            .filter(item => item.style.display !== 'none')
            .map(item => item.querySelector('input[type="checkbox"]'));

        if (visibleCbs.length === 0) {
            checkAll.checked = false;
            checkAll.indeterminate = false;
            return;
        }

        const checkedCount = visibleCbs.filter(cb => cb.checked).length;
        if (checkedCount === visibleCbs.length) {
            checkAll.checked = true;
            checkAll.indeterminate = false;
        } else if (checkedCount === 0) {
            checkAll.checked = false;
            checkAll.indeterminate = false;
        } else {
            checkAll.checked = false;
            checkAll.indeterminate = true;
        }
    }

    function showPopup(btn) {
        createPopup();

        currentBtn = btn;
        currentTable = btn.closest('table');
        currentTableType = currentTable ? currentTable.getAttribute('data-table-type') : null;
        currentColumn = btn.getAttribute('data-col');

        if (!currentTableType || !filterConfig[currentTableType] || !filterConfig[currentTableType].columns[currentColumn]) {
            console.warn("No filter config found for", currentTableType, currentColumn);
            return;
        }

        currentColConfig = filterConfig[currentTableType].columns[currentColumn];
        const colTitle = currentColConfig.title || btn.getAttribute('data-title') || 'cột';

        document.getElementById('ef-popup-title').textContent = `Lọc: ${colTitle}`;
        const searchInput = document.getElementById('ef-search-input');
        searchInput.value = '';

        const distinctVals = currentColConfig.options || [];
        const selectedVals = new Set(currentColConfig.selected || []);
        const listContainer = document.getElementById('ef-list');
        listContainer.innerHTML = '';

        if (distinctVals.length === 0) {
            listContainer.innerHTML = `<div style="padding:10px 12px; color:#888; font-style:italic;">(Không có dữ liệu)</div>`;
            document.getElementById('ef-select-all-label').style.display = 'none';
        } else {
            document.getElementById('ef-select-all-label').style.display = 'flex';
            distinctVals.forEach(val => {
                const isChecked = selectedVals.size > 0 ? selectedVals.has(val) : true;
                const label = document.createElement('label');
                label.className = 'ef-option-item';
                label.setAttribute('data-value', val);
                label.innerHTML = `
                    <input type="checkbox" value="${escapeHtml(val)}" ${isChecked ? 'checked' : ''}>
                    <span>${escapeHtml(val)}</span>
                `;
                label.querySelector('input').addEventListener('change', updateCheckAllState);
                listContainer.appendChild(label);
            });
        }

        updateCheckAllState();

        // Position popup relative to button
        popupEl.style.display = 'flex';
        popupEl.style.visibility = 'hidden';

        const btnRect = btn.getBoundingClientRect();
        const popupWidth = popupEl.offsetWidth || 230;
        const popupHeight = popupEl.offsetHeight || 260;

        let top = btnRect.bottom + window.scrollY + 4;
        let left = btnRect.left + window.scrollX;

        // Check right screen boundary
        if (left + popupWidth > window.innerWidth - 10) {
            left = window.innerWidth - popupWidth - 10;
        }
        if (left < 10) left = 10;

        // Check bottom screen boundary
        if (btnRect.bottom + popupHeight > window.innerHeight - 10 && btnRect.top - popupHeight > 10) {
            top = btnRect.top + window.scrollY - popupHeight - 4;
        }

        popupEl.style.top = `${top}px`;
        popupEl.style.left = `${left}px`;
        popupEl.style.visibility = 'visible';

        // Focus search
        setTimeout(() => searchInput.focus(), 50);
    }

    function hidePopup() {
        if (popupEl) {
            popupEl.style.display = 'none';
        }
        currentBtn = null;
        currentTable = null;
        currentTableType = null;
        currentColumn = null;
        currentColConfig = null;
    }

    function applyCurrentColumnFilter() {
        if (!currentTableType || !currentColConfig || !filterConfig[currentTableType]) return;

        const distinctVals = currentColConfig.options || [];
        const checkedBoxes = popupEl.querySelectorAll('#ef-list input[type="checkbox"]:checked');
        const selectedVals = Array.from(checkedBoxes).map(cb => cb.value);

        const url = new URL(window.location.href);
        const params = url.searchParams;

        // Remove existing query params for this column filter
        params.delete(currentColConfig.param);

        // If not all are selected and at least one is selected, append them
        if (selectedVals.length < distinctVals.length && selectedVals.length > 0) {
            selectedVals.forEach(val => {
                params.append(currentColConfig.param, val);
            });
        }

        // Reset page for this table to 1
        const pageParam = filterConfig[currentTableType].page_param;
        if (pageParam) {
            params.set(pageParam, '1');
        }

        hidePopup();
        window.location.href = url.pathname + '?' + params.toString();
    }

    function clearCurrentColumnFilter() {
        if (!currentTableType || !currentColConfig || !filterConfig[currentTableType]) return;

        const url = new URL(window.location.href);
        const params = url.searchParams;

        // Remove query param for this filter
        params.delete(currentColConfig.param);

        // Reset page for this table to 1
        const pageParam = filterConfig[currentTableType].page_param;
        if (pageParam) {
            params.set(pageParam, '1');
        }

        hidePopup();
        window.location.href = url.pathname + '?' + params.toString();
    }

    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    function initExcelFilters() {
        loadConfig();
        updateButtonIndicators();

        document.addEventListener('click', function(e) {
            const btn = e.target.closest('.excel-filter-btn');
            if (btn) {
                e.preventDefault();
                e.stopPropagation();
                if (currentBtn === btn && popupEl && popupEl.style.display !== 'none') {
                    hidePopup();
                } else {
                    showPopup(btn);
                }
            }
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initExcelFilters);
    } else {
        initExcelFilters();
    }
})();
