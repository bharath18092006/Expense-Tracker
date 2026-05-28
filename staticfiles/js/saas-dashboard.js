(function () {
  const API_BASE = "/api/v2";
  let incomeExpenseChart;
  let categoryPieChart;
  let currentPage = 1;
  let nextPage = null;
  let previousPage = null;
  let editingExpenseId = null;

  function getCookie(name) {
    const cookies = document.cookie ? document.cookie.split(";") : [];
    for (let i = 0; i < cookies.length; i += 1) {
      const cookie = cookies[i].trim();
      if (cookie.startsWith(name + "=")) {
        return decodeURIComponent(cookie.substring(name.length + 1));
      }
    }
    return null;
  }

  function formatMoney(value) {
    return Number(value || 0).toLocaleString(undefined, {
      maximumFractionDigits: 2,
      minimumFractionDigits: 2,
    });
  }

  function setLoading(isLoading) {
    const loadingEl = document.getElementById("dashboardLoading");
    if (!loadingEl) return;
    loadingEl.classList.toggle("hidden", !isLoading);
  }

  async function getJson(url) {
    const response = await fetch(url, { credentials: "include" });
    if (!response.ok) {
      throw new Error("Failed request: " + response.status);
    }
    return response.json();
  }

  function updateCards(snapshot) {
    document.getElementById("totalIncomeValue").textContent = formatMoney(snapshot.total_income);
    document.getElementById("totalExpenseValue").textContent = formatMoney(snapshot.total_expenses);
    document.getElementById("savingsValue").textContent = formatMoney(snapshot.savings);
    document.getElementById("balanceValue").textContent = formatMoney(snapshot.balance);
  }

  function drawIncomeExpenseChart(rows) {
    const ctx = document.getElementById("incomeExpenseChart");
    if (!ctx) return;
    if (incomeExpenseChart) incomeExpenseChart.destroy();
    incomeExpenseChart = new Chart(ctx, {
      type: "line",
      data: {
        labels: rows.map((item) => item.month),
        datasets: [
          {
            label: "Income",
            data: rows.map((item) => item.income),
            borderColor: "#0ea5e9",
            backgroundColor: "rgba(14,165,233,0.15)",
            tension: 0.35,
            fill: true,
          },
          {
            label: "Expense",
            data: rows.map((item) => item.expense),
            borderColor: "#f97316",
            backgroundColor: "rgba(249,115,22,0.15)",
            tension: 0.35,
            fill: true,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: { duration: 900 },
      },
    });
  }

  function drawCategoryChart(rows) {
    const ctx = document.getElementById("categoryPieChart");
    if (!ctx) return;
    if (categoryPieChart) categoryPieChart.destroy();
    categoryPieChart = new Chart(ctx, {
      type: "pie",
      data: {
        labels: rows.map((item) => item.category || "Uncategorized"),
        datasets: [
          {
            data: rows.map((item) => item.total),
            backgroundColor: ["#22c55e", "#0ea5e9", "#f59e0b", "#ef4444", "#a855f7", "#14b8a6"],
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: { duration: 900 },
      },
    });
  }

  function renderGoals(goals) {
    const list = document.getElementById("goalProgressList");
    if (!list) return;
    list.innerHTML = "";
    if (!goals.length) {
      list.innerHTML = '<p class="mb-0 text-muted">No goals found.</p>';
      return;
    }
    goals.forEach((goal) => {
      const percentage = Math.max(0, Math.min(100, Number(goal.saved_percentage || 0)));
      const item = document.createElement("div");
      item.className = "goal-item";
      item.innerHTML = `
        <div class="goal-top">
          <strong>${goal.name}</strong>
          <span>${percentage.toFixed(1)}%</span>
        </div>
        <div class="goal-progress"><span style="width:${percentage}%"></span></div>
      `;
      list.appendChild(item);
    });
  }

  function rowTemplate(row) {
    return `
      <tr>
        <td>${row.date}</td>
        <td>${row.category}</td>
        <td>${row.description}</td>
        <td class="text-right">${formatMoney(row.amount)}</td>
        <td class="text-right">
          <button class="btn btn-outline-primary action-btn edit-expense-btn"
            data-id="${row.id}"
            data-amount="${row.amount}"
            data-date="${row.date}"
            data-category="${row.category}"
            data-description="${row.description.replace(/"/g, "&quot;")}">Edit</button>
        </td>
      </tr>
    `;
  }

  async function loadTransactions(page) {
    const search = document.getElementById("transactionSearch").value || "";
    const ordering = document.getElementById("transactionSort").value || "-date";
    const data = await getJson(
      `${API_BASE}/expenses/?page=${page}&q=${encodeURIComponent(search)}&ordering=${encodeURIComponent(ordering)}`
    );
    const tbody = document.getElementById("recentTransactionsBody");
    tbody.innerHTML = (data.results || []).map(rowTemplate).join("");
    nextPage = data.next;
    previousPage = data.previous;
    currentPage = page;
    document.getElementById("paginationInfo").textContent = `Page ${currentPage}`;
  }

  function bindTableActions() {
    document.getElementById("prevPageBtn").addEventListener("click", async function () {
      if (!previousPage || currentPage <= 1) return;
      await loadTransactions(currentPage - 1);
      bindEditButtons();
    });
    document.getElementById("nextPageBtn").addEventListener("click", async function () {
      if (!nextPage) return;
      await loadTransactions(currentPage + 1);
      bindEditButtons();
    });
    document.getElementById("transactionSearch").addEventListener("input", async function () {
      await loadTransactions(1);
      bindEditButtons();
    });
    document.getElementById("transactionSort").addEventListener("change", async function () {
      await loadTransactions(1);
      bindEditButtons();
    });
  }

  function bindEditButtons() {
    document.querySelectorAll(".edit-expense-btn").forEach((btn) => {
      btn.addEventListener("click", function () {
        editingExpenseId = btn.dataset.id;
        document.getElementById("expenseModalTitle").textContent = "Edit Expense";
        document.getElementById("expenseAmount").value = btn.dataset.amount;
        document.getElementById("expenseDate").value = btn.dataset.date;
        document.getElementById("expenseCategory").value = btn.dataset.category;
        document.getElementById("expenseDescription").value = btn.dataset.description;
        openExpenseModal();
      });
    });
  }

  function resetExpenseForm() {
    editingExpenseId = null;
    document.getElementById("expenseModalTitle").textContent = "Add Expense";
    document.getElementById("expenseForm").reset();
    document.getElementById("expenseFormError").classList.add("d-none");
  }

  function openExpenseModal() {
    const modalEl = document.getElementById("expenseModal");
    if (!modalEl) return;
    if (window.bootstrap && window.bootstrap.Modal) {
      const instance = window.bootstrap.Modal.getOrCreateInstance(modalEl);
      instance.show();
      return;
    }
    if (window.jQuery) {
      window.jQuery("#expenseModal").modal("show");
    }
  }

  function closeExpenseModal() {
    const modalEl = document.getElementById("expenseModal");
    if (!modalEl) return;
    if (window.bootstrap && window.bootstrap.Modal) {
      const instance = window.bootstrap.Modal.getOrCreateInstance(modalEl);
      instance.hide();
      return;
    }
    if (window.jQuery) {
      window.jQuery("#expenseModal").modal("hide");
    }
  }

  async function saveExpense(event) {
    event.preventDefault();
    const payload = {
      amount: document.getElementById("expenseAmount").value,
      date: document.getElementById("expenseDate").value,
      category: document.getElementById("expenseCategory").value,
      description: document.getElementById("expenseDescription").value,
    };
    const isEdit = Boolean(editingExpenseId);
    const url = isEdit ? `${API_BASE}/expenses/${editingExpenseId}/` : `${API_BASE}/expenses/`;
    const method = isEdit ? "PUT" : "POST";

    const response = await fetch(url, {
      method: method,
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const data = await response.json();
      const errorEl = document.getElementById("expenseFormError");
      errorEl.textContent = JSON.stringify(data);
      errorEl.classList.remove("d-none");
      return;
    }

    closeExpenseModal();
    resetExpenseForm();
    await bootstrapDashboard();
  }

  async function bootstrapDashboard() {
    setLoading(true);
    try {
      const [snapshot, trend, category] = await Promise.all([
        getJson(`${API_BASE}/analytics/dashboard/`),
        getJson(`${API_BASE}/analytics/income-vs-expense/?months=6`),
        getJson(`${API_BASE}/analytics/category-spending/`),
      ]);

      updateCards(snapshot);
      drawIncomeExpenseChart(trend.results || []);
      drawCategoryChart(category.results || []);
      renderGoals(snapshot.goals || []);
      await loadTransactions(1);
      bindEditButtons();
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  }

  document.addEventListener("DOMContentLoaded", function () {
    bindTableActions();
    const openModalBtn = document.getElementById("openExpenseModalBtn");
    if (openModalBtn) {
      openModalBtn.addEventListener("click", function (event) {
        event.preventDefault();
        openExpenseModal();
      });
    }
    document.getElementById("expenseForm").addEventListener("submit", saveExpense);
    if (window.jQuery) {
      window.jQuery("#expenseModal").on("hidden.bs.modal", resetExpenseForm);
    }
    bootstrapDashboard();
  });
})();
