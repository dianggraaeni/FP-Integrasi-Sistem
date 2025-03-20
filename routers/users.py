from fastapi import APIRouter, HTTPException
from bson import ObjectId
from database import users_collection
import models
from datetime import datetime

router = APIRouter(prefix="/users", tags=["Users"])

# ✅ Create User
@router.post("/", response_model=models.UserResponse)
async def create_user(user: models.UserCreate):
    user_dict = user.dict()
    user_dict["created_at"] = datetime.utcnow()  # Tambah timestamp saat user dibuat
    user_dict["updated_at"] = datetime.utcnow()
    user_dict["is_active"] = True  # Default user aktif

    result = await users_collection.insert_one(user_dict)

    created_user = await users_collection.find_one({"_id": result.inserted_id})

    if not created_user:
        raise HTTPException(status_code=500, detail="Failed to create user")

    return {
        "id": str(created_user["_id"]),
        "name": created_user["name"],
        "email": created_user["email"],
        "created_at": created_user["created_at"],
        "updated_at": created_user["updated_at"],
        "is_active": created_user["is_active"]
    }

# ✅ Get All Users (Hanya yang aktif)
@router.get("/", response_model=list[models.UserResponse])
async def get_users():
    users_cursor = users_collection.find({"is_active": True}, {"_id": 1, "name": 1, "email": 1, "created_at": 1, "updated_at": 1})
    users = await users_cursor.to_list(length=100)

    return [{"id": str(user["_id"]), "name": user["name"], "email": user["email"], "created_at": user["created_at"], "updated_at": user["updated_at"]} for user in users]

# ✅ Get User by ID
@router.get("/{user_id}", response_model=models.UserResponse)
async def get_user(user_id: str):
    user = await users_collection.find_one({"_id": ObjectId(user_id), "is_active": True})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"id": str(user["_id"]), "name": user["name"], "email": user["email"], "created_at": user["created_at"], "updated_at": user["updated_at"]}

# ✅ Update User (PUT)
@router.put("/{user_id}", response_model=models.UserResponse)
async def update_user(user_id: str, updated_user: models.UserCreate):
    updated_user_dict = updated_user.dict()
    updated_user_dict["updated_at"] = datetime.utcnow()  # Update timestamp

    result = await users_collection.update_one(
        {"_id": ObjectId(user_id), "is_active": True},
        {"$set": updated_user_dict}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found or inactive")

    return await get_user(user_id)

# ✅ Partial Update User (PATCH)
@router.patch("/{user_id}", response_model=models.UserResponse)
async def partial_update_user(user_id: str, updated_user: models.UserUpdate):
    update_data = {k: v for k, v in updated_user.dict().items() if v is not None}

    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided for update")

    update_data["updated_at"] = datetime.utcnow()  # Update timestamp

    result = await users_collection.update_one(
        {"_id": ObjectId(user_id), "is_active": True},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found or inactive")

    return await get_user(user_id)

# ✅ Soft Delete User (Menonaktifkan user)
@router.patch("/{user_id}/deactivate")
async def deactivate_user(user_id: str):
    result = await users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"is_active": False, "updated_at": datetime.utcnow()}}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "User deactivated successfully"}

# ✅ Delete User (Permanent Delete)
@router.delete("/{user_id}")
async def delete_user(user_id: str):
    result = await users_collection.delete_one({"_id": ObjectId(user_id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "User deleted successfully"}
