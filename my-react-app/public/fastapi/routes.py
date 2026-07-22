from fastapi import APIRouter
router=APIRouter()

@router.get("/user/get")
def get_user():
    return "Get user"

@router.post("/user/post")
def post_user():
    return "Create user"

@router.put("/user/put")
def put_user():
    return "Upload user"

@router.patch("/user/patch")
def patch_user():
    return "Update user"

@router.delete("/user/delete")
def delete_user():
    return "Delete user"
