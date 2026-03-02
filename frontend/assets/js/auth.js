/**
 * 认证管理模块
 */

// 获取 token
function getToken() {
    return localStorage.getItem('access_token');
}

// 获取用户名
function getUsername() {
    return localStorage.getItem('username');
}

// 检查是否已登录
function isLoggedIn() {
    return !!getToken();
}

// 登出
function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('username');
    window.location.href = '/login';
}

// 验证 token 是否有效
async function verifyToken() {
    const token = getToken();
    if (!token) return false;

    try {
        const response = await fetch('/api/auth/verify', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        return response.ok;
    } catch (error) {
        console.error('验证 token 失败:', error);
        return false;
    }
}

// 保护页面（如果未登录，跳转到登录页）
async function protectPage() {
    // 登录页面不需要保护
    if (window.location.pathname === '/login') {
        return;
    }

    const token = getToken();
    if (!token) {
        window.location.href = '/login';
        return;
    }

    // 验证 token
    const isValid = await verifyToken();
    if (!isValid) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('username');
        window.location.href = '/login';
    }
}

// 为所有 API 请求添加认证头
function addAuthHeader(headers = {}) {
    const token = getToken();
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    return headers;
}

// 封装 fetch，自动添加认证头
async function authFetch(url, options = {}) {
    options.headers = addAuthHeader(options.headers || {});

    const response = await fetch(url, options);

    // 如果返回 401，跳转到登录页
    if (response.status === 401) {
        logout();
        return response;
    }

    return response;
}

// 显示用户信息（在导航栏）
function displayUserInfo() {
    const username = getUsername();
    if (!username) return;

    // 在导航栏显示用户名和登出按钮
    const navbarNav = document.querySelector('.navbar-nav');
    if (navbarNav) {
        const userInfo = document.createElement('div');
        userInfo.className = 'nav-item dropdown';
        userInfo.innerHTML = `
            <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                👤 ${username}
            </a>
            <ul class="dropdown-menu dropdown-menu-end">
                <li><a class="dropdown-item" href="#" onclick="openChangePasswordModal(); return false;">🔒 修改密码</a></li>
                <li><hr class="dropdown-divider"></li>
                <li><a class="dropdown-item" href="#" onclick="logout(); return false;">🚪 登出</a></li>
            </ul>
        `;
        navbarNav.appendChild(userInfo);
    }
}

// 打开修改密码模态框
function openChangePasswordModal() {
    // 创建模态框（如果不存在）
    let modal = document.getElementById('changePasswordModal');
    if (!modal) {
        const modalHTML = `
            <div class="modal fade" id="changePasswordModal" tabindex="-1">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">🔒 修改密码</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <div id="changePasswordAlert" class="alert d-none"></div>
                            <form id="changePasswordForm">
                                <div class="mb-3">
                                    <label for="oldPassword" class="form-label">旧密码</label>
                                    <input type="password" class="form-control" id="oldPassword" required>
                                </div>
                                <div class="mb-3">
                                    <label for="newPassword" class="form-label">新密码</label>
                                    <input type="password" class="form-control" id="newPassword" required minlength="6">
                                    <small class="text-muted">至少6个字符</small>
                                </div>
                                <div class="mb-3">
                                    <label for="confirmPassword" class="form-label">确认新密码</label>
                                    <input type="password" class="form-control" id="confirmPassword" required>
                                </div>
                            </form>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">取消</button>
                            <button type="button" class="btn btn-primary" onclick="submitChangePassword()">确认修改</button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        document.body.insertAdjacentHTML('beforeend', modalHTML);
    }

    // 显示模态框
    const bsModal = new bootstrap.Modal(document.getElementById('changePasswordModal'));
    bsModal.show();
}

// 提交修改密码
async function submitChangePassword() {
    const oldPassword = document.getElementById('oldPassword').value;
    const newPassword = document.getElementById('newPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    const alertDiv = document.getElementById('changePasswordAlert');

    // 验证
    if (!oldPassword || !newPassword || !confirmPassword) {
        showChangePasswordAlert('请填写所有字段', 'danger');
        return;
    }

    if (newPassword.length < 6) {
        showChangePasswordAlert('新密码至少6个字符', 'danger');
        return;
    }

    if (newPassword !== confirmPassword) {
        showChangePasswordAlert('两次输入的新密码不一致', 'danger');
        return;
    }

    try {
        const response = await authFetch('/api/auth/change-password', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                old_password: oldPassword,
                new_password: newPassword
            })
        });

        const data = await response.json();

        if (response.ok) {
            showChangePasswordAlert('密码修改成功！', 'success');
            setTimeout(() => {
                const modal = bootstrap.Modal.getInstance(document.getElementById('changePasswordModal'));
                modal.hide();
                document.getElementById('changePasswordForm').reset();
            }, 1500);
        } else {
            showChangePasswordAlert(data.detail || '修改失败', 'danger');
        }
    } catch (error) {
        console.error('修改密码失败:', error);
        showChangePasswordAlert('修改失败，请重试', 'danger');
    }
}

// 显示修改密码提示
function showChangePasswordAlert(message, type) {
    const alertDiv = document.getElementById('changePasswordAlert');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;
    alertDiv.classList.remove('d-none');

    setTimeout(() => {
        alertDiv.classList.add('d-none');
    }, 5000);
}

// 页面加载时执行
document.addEventListener('DOMContentLoaded', async () => {
    // 保护页面
    await protectPage();

    // 显示用户信息
    if (isLoggedIn()) {
        displayUserInfo();
    }
});
