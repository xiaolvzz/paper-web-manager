/**
 * 简单的客户端缓存管理
 * 用于减少重复的API请求
 */

class SimpleCache {
    constructor(ttl = 5 * 60 * 1000) { // 默认5分钟过期
        this.cache = new Map();
        this.ttl = ttl; // Time to live in milliseconds
    }

    /**
     * 生成缓存键
     */
    generateKey(url, params = {}) {
        const paramsStr = JSON.stringify(params);
        return `${url}:${paramsStr}`;
    }

    /**
     * 获取缓存
     */
    get(key) {
        const item = this.cache.get(key);
        if (!item) return null;

        // 检查是否过期
        if (Date.now() > item.expiry) {
            this.cache.delete(key);
            return null;
        }

        return item.data;
    }

    /**
     * 设置缓存
     */
    set(key, data, customTTL = null) {
        const ttl = customTTL || this.ttl;
        this.cache.set(key, {
            data,
            expiry: Date.now() + ttl
        });
    }

    /**
     * 清除缓存
     */
    clear(pattern = null) {
        if (!pattern) {
            this.cache.clear();
            return;
        }

        // 按模式清除
        for (const key of this.cache.keys()) {
            if (key.includes(pattern)) {
                this.cache.delete(key);
            }
        }
    }

    /**
     * 清除过期缓存
     */
    cleanup() {
        const now = Date.now();
        for (const [key, value] of this.cache.entries()) {
            if (now > value.expiry) {
                this.cache.delete(key);
            }
        }
    }
}

// 创建全局缓存实例
const apiCache = new SimpleCache();

// 定期清理过期缓存（每5分钟）
setInterval(() => {
    apiCache.cleanup();
}, 5 * 60 * 1000);

/**
 * 带缓存的fetch封装
 */
async function cachedFetch(url, options = {}, useCache = true, cacheTTL = null) {
    const cacheKey = apiCache.generateKey(url, options);

    // 尝试从缓存获取
    if (useCache && options.method !== 'POST' && options.method !== 'PUT' && options.method !== 'DELETE') {
        const cached = apiCache.get(cacheKey);
        if (cached) {
            console.log(`📦 从缓存加载: ${url}`);
            return Promise.resolve(new Response(JSON.stringify(cached), {
                status: 200,
                headers: { 'Content-Type': 'application/json' }
            }));
        }
    }

    // 执行实际请求
    const response = await fetch(url, options);

    // 缓存成功的GET请求
    if (useCache && response.ok && (!options.method || options.method === 'GET')) {
        const clonedResponse = response.clone();
        const data = await clonedResponse.json();
        apiCache.set(cacheKey, data, cacheTTL);
    }

    return response;
}

/**
 * 清除特定资源的缓存
 */
function clearResourceCache(resourceType) {
    apiCache.clear(resourceType);
    console.log(`🗑️ 已清除 ${resourceType} 缓存`);
}
