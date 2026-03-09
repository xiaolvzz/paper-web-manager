/**
 * 全局加载动画管理
 */

// 创建全局加载遮罩
function createGlobalLoader() {
    const existingLoader = document.getElementById('globalLoader');
    if (existingLoader) return;

    const loader = document.createElement('div');
    loader.id = 'globalLoader';
    loader.innerHTML = `
        <div class="loader-backdrop">
            <div class="loader-content">
                <div class="spinner-border text-primary" role="status" style="width: 3rem; height: 3rem;">
                    <span class="visually-hidden">加载中...</span>
                </div>
                <p class="mt-3 mb-0" id="loaderText">加载中...</p>
            </div>
        </div>
    `;
    document.body.appendChild(loader);
}

// 显示全局加载动画
function showGlobalLoader(text = '加载中...') {
    createGlobalLoader();
    const loader = document.getElementById('globalLoader');
    const loaderText = document.getElementById('loaderText');
    if (loaderText) loaderText.textContent = text;
    if (loader) loader.style.display = 'flex';
}

// 隐藏全局加载动画
function hideGlobalLoader() {
    const loader = document.getElementById('globalLoader');
    if (loader) {
        loader.style.display = 'none';
    }
}

// 页面加载时自动初始化
document.addEventListener('DOMContentLoaded', () => {
    createGlobalLoader();
});
