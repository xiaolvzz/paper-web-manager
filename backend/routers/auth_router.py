"""认证API路由"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from supabase import Client
from backend.database import get_db
from backend.auth import hash_password, verify_password, create_access_token, get_current_user
from datetime import datetime

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginRequest(BaseModel):
    """登录请求"""
    username: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=1)


class LoginResponse(BaseModel):
    """登录响应"""
    access_token: str
    token_type: str = "bearer"
    username: str


class ChangePasswordRequest(BaseModel):
    """修改密码请求"""
    old_password: str
    new_password: str = Field(..., min_length=6, max_length=100)


@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest, db: Client = Depends(get_db)):
    """用户登录"""
    try:
        # 查询用户
        response = db.table("users").select("*").eq("username", request.username).execute()

        if not response.data or len(response.data) == 0:
            raise HTTPException(status_code=401, detail="用户名或密码错误")

        user = response.data[0]

        # 检查账户是否激活
        if not user.get("is_active", False):
            raise HTTPException(status_code=401, detail="账户已被禁用")

        # 验证密码
        if not verify_password(request.password, user["password_hash"]):
            raise HTTPException(status_code=401, detail="用户名或密码错误")

        # 更新最后登录时间
        db.table("users").update({
            "last_login": datetime.utcnow().isoformat()
        }).eq("id", user["id"]).execute()

        # 生成访问令牌
        access_token = create_access_token(
            data={"sub": user["username"], "user_id": user["id"]}
        )

        return LoginResponse(
            access_token=access_token,
            username=user["username"]
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"登录失败: {str(e)}")


@router.post("/change-password")
async def change_password(
    request: ChangePasswordRequest,
    current_user: dict = Depends(get_current_user),
    db: Client = Depends(get_db)
):
    """修改密码"""
    try:
        # 获取用户信息
        response = db.table("users").select("*").eq("username", current_user["username"]).execute()

        if not response.data:
            raise HTTPException(status_code=404, detail="用户不存在")

        user = response.data[0]

        # 验证旧密码
        if not verify_password(request.old_password, user["password_hash"]):
            raise HTTPException(status_code=401, detail="旧密码错误")

        # 加密新密码
        new_password_hash = hash_password(request.new_password)

        # 更新密码
        db.table("users").update({
            "password_hash": new_password_hash
        }).eq("id", user["id"]).execute()

        return {"success": True, "message": "密码修改成功"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"修改密码失败: {str(e)}")


@router.get("/verify")
async def verify_token(current_user: dict = Depends(get_current_user)):
    """验证令牌是否有效"""
    return {
        "valid": True,
        "username": current_user["username"],
        "user_id": current_user["user_id"]
    }


@router.post("/logout")
async def logout(current_user: dict = Depends(get_current_user)):
    """登出（前端删除token即可）"""
    return {"success": True, "message": "登出成功"}
