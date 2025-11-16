const API_BASE = 'http://localhost:5000/api';
let allQueries = [];
let categories = [];

// Navigation
function showSection(sectionName) {
    document.querySelectorAll('.section').forEach(section => {
        section.classList.remove('active');
    });

    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('active');
    });

    document.getElementById(sectionName).classList.add('active');
    event.target.classList.add('active');

    switch(sectionName) {
        case 'dashboard':
            loadDashboard();
            break;
        case 'queries':
            loadQueries();
            break;
        case 'analytics':
            loadAnalytics();
            break;
    }
}

// Load dashboard data
async function loadDashboard() {
    try {
        const [statsResponse, queriesResponse] = await Promise.all([
            fetch(`${API_BASE}/queries/stats`),
            fetch(`${API_BASE}/queries?limit=10`)
        ]);

        const stats = await statsResponse.json();
        const queries = await queriesResponse.json();

        // Update stats
        document.getElementById('total-queries').textContent = stats.total_queries;
        document.getElementById('resolved-queries').textContent = stats.by_status.resolved || 0;
        document.getElementById('high-priority').textContent = stats.by_priority.priority_3 || 0;

        // Update charts
        updateCategoryChart(stats.by_category);
        updateStatusChart(stats.by_status);

        // Update recent queries
        updateRecentQueries(queries);

    } catch (error) {
        console.error('Error loading dashboard:', error);
    }
}

// Update category chart
function updateCategoryChart(categoryData) {
    const ctx = document.getElementById('categoryChart').getContext('2d');

    if (window.categoryChart) {
        window.categoryChart.destroy();
    }

    const colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c'];

    window.categoryChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: Object.keys(categoryData).map(key => key.charAt(0).toUpperCase() + key.slice(1)),
            datasets: [{
                data: Object.values(categoryData),
                backgroundColor: colors,
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

// Update status chart
function updateStatusChart(statusData) {
    const ctx = document.getElementById('statusChart').getContext('2d');

    if (window.statusChart) {
        window.statusChart.destroy();
    }

    window.statusChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: Object.keys(statusData).map(key => key.replace('-', ' ').toUpperCase()),
            datasets: [{
                label: 'Queries',
                data: Object.values(statusData),
                backgroundColor: '#3498db',
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
}

// Update recent queries
function updateRecentQueries(queries) {
    const container = document.getElementById('recent-queries-list');
    container.innerHTML = '';

    queries.forEach(query => {
        const queryElement = createQueryElement(query);
        container.appendChild(queryElement);
    });
}

// Load all queries with filtering
async function loadQueries() {
    try {
        const statusFilter = document.getElementById('status-filter').value;
        const priorityFilter = document.getElementById('priority-filter').value;
        const categoryFilter = document.getElementById('category-filter').value;

        let url = `${API_BASE}/queries`;
        const params = new URLSearchParams();

        if (statusFilter !== 'all') params.append('status', statusFilter);
        if (priorityFilter !== 'all') params.append('priority', priorityFilter);
        if (categoryFilter !== 'all') params.append('category', categoryFilter);

        if (params.toString()) url += '?' + params.toString();

        const response = await fetch(url);
        allQueries = await response.json();

        updateAllQueriesList(allQueries);

    } catch (error) {
        console.error('Error loading queries:', error);
    }
}

function updateAllQueriesList(queries) {
    const container = document.getElementById('all-queries-list');
    container.innerHTML = '';

    if (queries.length === 0) {
        container.innerHTML = '<div class="query-item">No queries found matching your filters.</div>';
        return;
    }

    queries.forEach(query => {
        const queryElement = createQueryElement(query, true);
        container.appendChild(queryElement);
    });
}

function createQueryElement(query, showActions = false) {
    const queryElement = document.createElement('div');
    queryElement.className = `query-item ${query.priority === 3 ? 'high-priority' : query.priority === 2 ? 'medium-priority' : ''}`;

    const priorityText = query.priority === 3 ? 'High' : query.priority === 2 ? 'Medium' : 'Low';

    queryElement.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div style="flex: 1;">
                <div style="margin-bottom: 10px;">
                    <span class="query-category">${query.category.toUpperCase()}</span>
                    <span class="query-priority priority-${query.priority}">${priorityText}</span>
                    <span style="background: #3498db; color: white; padding: 4px 12px; border-radius: 20px; font-size: 0.8em;">
                        ${query.status.toUpperCase()}
                    </span>
                </div>
                <h4 style="margin: 5px 0;">${query.subject}</h4>
                <p style="color: #666; margin: 8px 0;">${query.content.substring(0, 150)}...</p>
                <div style="font-size: 0.9em; color: #999;">
                    <strong>From:</strong> ${query.customer_email} |
                    <strong>Source:</strong> ${query.source} |
                    <strong>Assigned to:</strong> ${query.assigned_to} |
                    <strong>Received:</strong> ${new Date(query.created_at).toLocaleDateString()}
                </div>
            </div>
            ${showActions ? `
            <div style="display: flex; gap: 10px; flex-direction: column;">
                <select onchange="updateQueryStatus(${query.id}, this.value)" style="padding: 5px;">
                    <option value="new" ${query.status === 'new' ? 'selected' : ''}>New</option>
                    <option value="in-progress" ${query.status === 'in-progress' ? 'selected' : ''}>In Progress</option>
                    <option value="resolved" ${query.status === 'resolved' ? 'selected' : ''}>Resolved</option>
                </select>
            </div>
            ` : ''}
        </div>
    `;

    return queryElement;
}

// Update query status
async function updateQueryStatus(queryId, newStatus) {
    try {
        await fetch(`${API_BASE}/queries/${queryId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                status: newStatus
            })
        });

        loadQueries(); // Refresh the list
    } catch (error) {
        console.error('Error updating query:', error);
        alert('Error updating query status');
    }
}

// Load analytics
async function loadAnalytics() {
    try {
        const [responseTimes, teamPerformance] = await Promise.all([
            fetch(`${API_BASE}/analytics/response-times`),
            fetch(`${API_BASE}/analytics/team-performance`)
        ]);

        const times = await responseTimes.json();
        const teams = await teamPerformance.json();

        document.getElementById('response-times').innerHTML = `
            <div style="font-size: 2em; text-align: center; color: #3498db; margin: 20px 0;">
                ${times.average_response_time_hours} hours
            </div>
            <p style="text-align: center; color: #666;">
                Average response time across ${times.queries_with_responses} queries
            </p>
        `;

        let teamHtml = '';
        for (const [team, stats] of Object.entries(teams)) {
            teamHtml += `
                <div style="background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 8px;">
                    <h4>${team}</h4>
                    <div>Total Queries: ${stats.total_queries}</div>
                    <div>Resolved: ${stats.resolved_queries}</div>
                    <div>Resolution Rate: ${stats.resolution_rate}%</div>
                </div>
            `;
        }

        document.getElementById('team-performance').innerHTML = teamHtml;

    } catch (error) {
        console.error('Error loading analytics:', error);
    }
}

// Handle new query form
document.getElementById('new-query-form').addEventListener('submit', async function(e) {
    e.preventDefault();

    const formData = {
        source: document.getElementById('query-source').value,
        customer_email: document.getElementById('customer-email').value,
        subject: document.getElementById('query-subject').value,
        content: document.getElementById('query-content').value
    };

    try {
        const response = await fetch(`${API_BASE}/queries`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });

        if (response.ok) {
            alert('Query submitted successfully!');
            document.getElementById('new-query-form').reset();
            showSection('queries');
            loadQueries();
        } else {
            alert('Error submitting query');
        }
    } catch (error) {
        console.error('Error submitting query:', error);
        alert('Error submitting query');
    }
});

// Initialize dashboard when page loads
document.addEventListener('DOMContentLoaded', function() {
    loadDashboard();
});