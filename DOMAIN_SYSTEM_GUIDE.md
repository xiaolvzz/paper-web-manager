# 领域标签系统使用指南

## 🎯 功能概述

全新的领域标签系统让你可以：
- ✅ 为论文标记多个领域（如：VLA + 强化学习）
- ✅ 按领域筛选和查看论文
- ✅ 标注论文间的各种关系（衍生、扩展、对比等）
- ✅ 可视化同领域论文的关系网络
- ✅ 快速找到交叉领域的论文

---

## 📋 第一步：执行数据库迁移

在Supabase的SQL编辑器中执行 `migrations/004_enhance_tags_and_relations.sql`

这会创建：
- ✅ `domains` 表（10个预设领域 + 自定义领域）
- ✅ `paper_domains` 表（论文-领域多对多关联）
- ✅ 扩展关系类型支持

**预设的10个领域：**
1. 🤖 VLA (视觉-语言-动作)
2. 🎮 强化学习
3. 👁️ 计算机视觉
4. 💬 自然语言处理
5. 🚗 自动驾驶
6. 🦾 具身智能
7. 🌍 世界模型
8. ⚡ Transformer
9. 🌊 扩散模型
10. 🎨 多模态

---

## 🚀 使用方法

### 1. 为论文分配领域（使用API）

目前需要通过API调用来分配领域（前端界面正在开发中）：

```javascript
// 方法1：在浏览器控制台中执行（按F12打开）
await DomainsAPI.assign(
    1,  // 论文ID
    [1, 2, 3]  // 领域ID列表：VLA、强化学习、CV
);

// 方法2：获取所有领域，找到想要的领域ID
const domains = await DomainsAPI.list();
console.table(domains);

// 然后分配
await DomainsAPI.assign(论文ID, [领域ID1, 领域ID2]);
```

### 2. 查看增强的关系图

访问：`https://your-app.vercel.app/graph`

**新功能：**
- 🎨 **节点颜色**：边框颜色表示论文的主要领域
- 🔍 **领域筛选**：下拉菜单选择领域，只显示该领域的论文
- 🔗 **关系类型筛选**：点击"🔍 筛选"按钮，选择关系类型
- 📊 **实时统计**：显示论文数、关系数、领域数
- 🏷️ **彩色图例**：不同关系类型用不同颜色标注

### 3. 添加论文关系（扩展关系类型）

在论文详情页添加关联时，现在支持更多关系类型：

**可用的关系类型：**
- 🔗 **derived_from**（衍生）：B改进了A的方法
- 📈 **extends**（扩展）：B扩展了A的工作
- 🔄 **method_similar**（方法相似）：使用类似的技术
- 🎯 **problem_related**（问题相关）：研究相关问题
- ⚖️ **compares_with**（对比）：实验对比
- 🏷️ **same_domain**（同领域）：同一研究领域
- 📐 **baseline**（基线）：A是B的基线方法
- ✏️ **custom**（自定义）：其他关系

---

## 💡 使用场景示例

### 场景1：整理VLA领域论文

1. 为所有VLA论文分配"VLA"领域标签
2. 打开关系图，筛选"VLA"领域
3. 添加论文间的关系：
   - DriveVLA `衍生自` → GPT-Driver
   - DiffusionDriver `方法相似` → DriveWorld
4. 一眼看清VLA领域的研究脉络

### 场景2：追溯方法演进

1. 找到一篇基础论文（如Transformer）
2. 添加 `derived_from` 关系，标注后续改进
3. 在关系图中看到清晰的演进路径
4. 紫色线条（衍生关系）连接整条技术路线

### 场景3：管理交叉领域论文

1. 一篇论文同时属于"VLA"、"强化学习"、"世界模型"
2. 为它分配3个领域标签
3. 在任意领域筛选中都能找到它
4. 节点颜色显示主要领域（第一个标签的颜色）

---

## 🎨 领域颜色映射

- 🤖 VLA：紫色 `#8b5cf6`
- 🎮 强化学习：绿色 `#10b981`
- 👁️ 计算机视觉：蓝色 `#3b82f6`
- 💬 NLP：橙色 `#f59e0b`
- 🚗 自动驾驶：红色 `#ef4444`
- 🦾 具身智能：粉色 `#ec4899`
- 🌍 世界模型：青色 `#06b6d4`
- ⚡ Transformer：靛蓝 `#6366f1`
- 🌊 扩散模型：紫罗兰 `#a855f7`
- 🎨 多模态：深橙 `#f97316`

---

## 🔧 高级功能

### 创建自定义领域

```javascript
await DomainsAPI.create({
    name: "神经辐射场",
    color: "#14b8a6",  // 自定义颜色
    icon: "🌟",
    description: "Neural Radiance Fields"
});
```

### 批量标记同领域论文

```javascript
// 1. 获取所有论文
const papers = await PapersAPI.list();

// 2. 筛选VLA相关论文（根据标题或标签）
const vlaPapers = papers.filter(p =>
    p.title.includes('VLA') || p.tags?.includes('VLA')
);

// 3. 批量分配领域
for (const paper of vlaPapers) {
    await DomainsAPI.assign(paper.id, [1]);  // 1 = VLA领域
}
```

### 查询某个领域的所有论文

```javascript
// 查看"自动驾驶"领域下的所有论文
const papers = await DomainsAPI.getDomainPapers(5);  // 5 = 自动驾驶
console.table(papers);
```

---

## 📱 后续改进计划

1. **论文详情页集成**
   - 在论文信息中显示领域标签
   - 点击添加/移除领域
   - 快捷按钮一键标记

2. **智能推荐**
   - AI自动识别论文领域
   - 推荐可能的关联论文
   - 自动检测衍生关系

3. **批量操作**
   - 多选论文批量标记领域
   - 批量添加同领域关系

4. **可视化增强**
   - 3D关系图
   - 时间轴视图（按年份展开）
   - 领域热力图

---

## 🆘 常见问题

### Q: 如何查看论文已分配的领域？
```javascript
const domains = await DomainsAPI.getPaperDomains(论文ID);
console.table(domains);
```

### Q: 如何删除领域标签？
```javascript
// 重新分配时会覆盖旧的领域
await DomainsAPI.assign(论文ID, [新的领域ID列表]);

// 清空所有领域
await DomainsAPI.assign(论文ID, []);
```

### Q: 关系图太复杂怎么办？
使用筛选功能：
1. 选择特定领域：只看VLA相关论文
2. 选择特定关系：只看衍生关系
3. 组合筛选：VLA领域 + 衍生关系

---

## 📞 需要帮助？

如有问题或建议，欢迎反馈！这个功能会持续改进，让论文管理更加高效。
