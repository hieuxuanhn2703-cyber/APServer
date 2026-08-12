/**
 * Excel-Style Column Filtering for Tables
 * Supports multi-column filtering, search within filter, select all / deselect all,
 * active filter indicators, and real-time client-side table row updates.
 */

(function() {
    'use strict';

    // Store active filters per table: Map<HTMLTableElement, Map<colIndex, Set<string>>>
    const tableFilters = new Map();
    let currentTable = null;
    let currentColumn = null;
    let currentBtn = null;
    let popupEl = null;

    const SVG_DOWN_ARROW = `<svg viewBox="0 0 24 24" width="8" height="8" fill="currentColor"><path d="M7 10l5 5 5-5z"/></svg>`;
    const SVG_FUNNEL_ACTIVE = `<svg viewBox="0 0 24 24" width="9" height="9" fill="currentColor"><path d="M10 18h4v-2h-4v2zM3 6v2h18V6H3zm3 7h12v-2H6v2z"/></svg>`;

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

        // Event listeners for popup elements
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

    function getDistinctValues(table, colIndex) {
        const rows = table.querySelectorAll('tbody tr:not(.empty-row):not(.filter-empty-row)');
        const valuesSet = new Set();

        rows.forEach(row => {
            const cells = row.children;
            if (cells && cells.length > colIndex) {
                // If this cell has colspan, skip or handle
                const cell = cells[colIndex];
                if (cell) {
                    const text = cell.textContent.trim();
                    if (text && !cell.classList.contains('empty')) {
                        valuesSet.add(text);
                    }
                }
            }
        });

        const values = Array.from(valuesSet);
        // Sort values: try numeric, then locale
        values.sort((a, b) => {
            const numA = Number(a);
            const numB = Number(b);
            if (!isNaN(numA) && !isNaN(numB)) {
                return numA - numB;
            }
            return a.localeCompare(b, 'vi', { numeric: true });
        });

        return values;
    }

    function showPopup(btn) {
        createPopup();

        currentBtn = btn;
        currentTable = btn.closest('table');
        currentColumn = parseInt(btn.getAttribute('data-col'), 10);
        const colTitle = btn.getAttribute('data-title') || 'cột';

        document.getElementById('ef-popup-title').textContent = `Lọc: ${colTitle}`;
        const searchInput = document.getElementById('ef-search-input');
        searchInput.value = '';

        // Get all distinct values in this column
        const distinctVals = getDistinctValues(currentTable, currentColumn);
        const listContainer = document.getElementById('ef-list');
        listContainer.innerHTML = '';

        if (!tableFilters.has(currentTable)) {
            tableFilters.set(currentTable, new Map());
        }
        const activeTableFilters = tableFilters.get(currentTable);
        const activeColumnFilter = activeTableFilters.get(currentColumn); // Set or undefined

        if (distinctVals.length === 0) {
            listContainer.innerHTML = `<div style="padding:10px 12px; color:#888; font-style:italic;">(Không có dữ liệu)</div>`;
            document.getElementById('ef-select-all-label').style.display = 'none';
        } else {
            document.getElementById('ef-select-all-label').style.display = 'flex';
            distinctVals.forEach(val => {
                const isChecked = activeColumnFilter ? activeColumnFilter.has(val) : true;
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
        currentColumn = null;
    }

    function applyCurrentColumnFilter() {
        if (!currentTable || currentColumn === null || !currentBtn) return;

        const distinctVals = getDistinctValues(currentTable, currentColumn);
        const checkedBoxes = popupEl.querySelectorAll('#ef-list input[type="checkbox"]:checked');
        const selectedVals = new Set(Array.from(checkedBoxes).map(cb => cb.value));

        const activeTableFilters = tableFilters.get(currentTable);

        // If all are selected (or none are available), no filtering is active on this column
        if (selectedVals.size >= distinctVals.length || selectedVals.size === 0 && distinctVals.length === 0) {
            activeTableFilters.delete(currentColumn);
            currentBtn.classList.remove('is-filtered');
            currentBtn.innerHTML = SVG_DOWN_ARROW;
            currentBtn.title = `Lọc ${currentBtn.getAttribute('data-title') || ''}`;
        } else {
            activeTableFilters.set(currentColumn, selectedVals);
            currentBtn.classList.add('is-filtered');
            currentBtn.innerHTML = SVG_FUNNEL_ACTIVE;
            currentBtn.title = `Đang lọc: ${selectedVals.size}/${distinctVals.length} giá trị`;
        }

        applyAllFilters(currentTable);
        hidePopup();
    }

    function clearCurrentColumnFilter() {
        if (!currentTable || currentColumn === null || !currentBtn) return;

        const activeTableFilters = tableFilters.get(currentTable);
        activeTableFilters.delete(currentColumn);

        currentBtn.classList.remove('is-filtered');
        currentBtn.innerHTML = SVG_DOWN_ARROW;
        currentBtn.title = `Lọc ${currentBtn.getAttribute('data-title') || ''}`;

        applyAllFilters(currentTable);
        hidePopup();
    }

    function applyAllFilters(table) {
        if (!table) return;

        const activeTableFilters = tableFilters.get(table) || new Map();
        const rows = table.querySelectorAll('tbody tr:not(.empty):not(.filter-empty-row)');
        let visibleCount = 0;

        rows.forEach(row => {
            // Check if this row is the backend empty message
            if (row.querySelector('td.empty')) return;

            let isRowVisible = true;
            for (const [colIdx, allowedSet] of activeTableFilters.entries()) {
                const cell = row.children[colIdx];
                if (cell) {
                    const text = cell.textContent.trim();
                    if (!allowedSet.has(text)) {
                        isRowVisible = false;
                        break;
                    }
                }
            }

            row.style.display = isRowVisible ? '' : 'none';
            if (isRowVisible) visibleCount++;
        });

        // Manage dynamic empty state if all rows filtered out
        let filterEmptyRow = table.querySelector('.filter-empty-row');
        if (visibleCount === 0 && rows.length > 0) {
            if (!filterEmptyRow) {
                filterEmptyRow = document.createElement('tr');
                filterEmptyRow.className = 'filter-empty-row';
                filterEmptyRow.innerHTML = `<td colspan="30" style="text-align:center; color:#e74c3c; padding:18px; font-style:italic; background:#fff9f9;">Không có dữ liệu phù hợp với bộ lọc cột hiện tại.</td>`;
                const tbody = table.querySelector('tbody');
                if (tbody) tbody.appendChild(filterEmptyRow);
            }
            filterEmptyRow.style.display = '';
        } else if (filterEmptyRow) {
            filterEmptyRow.style.display = 'none';
        }
    }

    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // Initialize all Excel filter buttons
    function initExcelFilters() {
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
