# Supabase Storage 配置指南

## 问题：上传图片失败

如果遇到"上传图片失败"错误，请按以下步骤检查和配置：

## 1. 检查存储桶是否存在

1. 登录 Supabase Dashboard
2. 进入你的项目
3. 点击左侧菜单 **Storage**
4. 查看是否存在名为 `paper-pdfs` 的存储桶

## 2. 创建或配置存储桶

### 如果存储桶不存在：

1. 点击 **"New bucket"** 按钮
2. 填写信息：
   - **Name**: `paper-pdfs`
   - **Public bucket**: ✅ **勾选**（重要！）
   - **File size limit**: 50 MB（可选）
   - **Allowed MIME types**: 留空或填写 `image/*`
3. 点击 **"Create bucket"**

### 如果存储桶已存在但是私有的：

1. 点击存储桶旁边的 **⚙️ 设置图标**
2. 进入 **Configuration** 标签
3. 确认 **"Public bucket"** 已启用
4. 如果没有，切换为 Public
5. 保存更改

## 3. 设置存储策略（重要）

即使存储桶是公开的，也需要配置存储策略允许上传：

1. 在 Storage 页面，点击存储桶名称
2. 点击顶部的 **Policies** 标签
3. 点击 **"New policy"**
4. 选择 **"Custom policy"**
5. 填写策略信息：
   ```
   Policy name: Allow public uploads to note-images
   Target roles: public (anon)
   ```
6. 在 **Policy definition** 中，选择：
   - **Operation**: INSERT
   - **Table**: storage.objects
   - **WITH CHECK expression**:
     ```sql
     bucket_id = 'paper-pdfs' AND (storage.foldername(name))[1] = 'note-images'
     ```
7. 点击 **"Review"** 然后 **"Save policy"**

## 4. 验证配置

使用以下 SQL 在 SQL Editor 中验证：

```sql
-- 查看存储桶配置
SELECT * FROM storage.buckets WHERE name = 'paper-pdfs';

-- 查看存储策略
SELECT * FROM storage.policies WHERE bucket_id = 'paper-pdfs';
```

## 5. 测试上传

配置完成后，刷新网页并重试上传图片。

## 常见错误和解决方法

### 错误1: "Bucket not found"
**原因**：存储桶不存在
**解决**：按步骤2创建存储桶

### 错误2: "Access denied" 或 "Unauthorized"
**原因**：存储桶是私有的或缺少上传策略
**解决**：
1. 确保存储桶是 Public
2. 添加上传策略（步骤3）

### 错误3: "File too large"
**原因**：图片超过5MB
**解决**：压缩图片或使用更小的截图

### 错误4: "Invalid file type"
**原因**：文件类型不支持
**解决**：确保上传的是 JPG、PNG、GIF 或 WebP 格式

## 快速配置 SQL（一键执行）

在 Supabase SQL Editor 中执行以下 SQL 一键配置：

```sql
-- 1. 确保存储桶存在且为公开
INSERT INTO storage.buckets (id, name, public)
VALUES ('paper-pdfs', 'paper-pdfs', true)
ON CONFLICT (id) DO UPDATE SET public = true;

-- 2. 添加上传策略
INSERT INTO storage.policies (name, bucket_id, definition, check_expression)
VALUES (
  'Allow public uploads to note-images',
  'paper-pdfs',
  'INSERT',
  'bucket_id = ''paper-pdfs'' AND (storage.foldername(name))[1] = ''note-images'''
)
ON CONFLICT DO NOTHING;

-- 3. 添加读取策略（允许查看图片）
INSERT INTO storage.policies (name, bucket_id, definition, check_expression)
VALUES (
  'Allow public read from note-images',
  'paper-pdfs',
  'SELECT',
  'bucket_id = ''paper-pdfs'''
)
ON CONFLICT DO NOTHING;
```

## 验证是否配置成功

执行以下查询：

```sql
-- 应该显示 public = true
SELECT id, name, public FROM storage.buckets WHERE name = 'paper-pdfs';

-- 应该显示至少2条策略
SELECT * FROM storage.policies WHERE bucket_id = 'paper-pdfs';
```

## 需要帮助？

如果以上步骤都无法解决问题：

1. 打开浏览器开发者工具（F12）
2. 切换到 **Network** 标签
3. 尝试上传图片
4. 查找 `/api/code-notes/upload-image` 请求
5. 查看响应内容中的具体错误信息
6. 将错误信息提供给我，我会帮你进一步诊断
