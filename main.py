from fastapi import FastAPI, UploadFile, File, Form
from app.db import db
from app.models import Teacher, Class, Student, Attendance
import os, io, asyncio
from PIL import Image
import numpy as np
from bson import ObjectId
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import insightface
import cv2

app = FastAPI()
IMAGE_DIR = "data/images"
os.makedirs(IMAGE_DIR, exist_ok=True)

executor = ThreadPoolExecutor(max_workers=4)

# ----------------------
# Load InsightFace model
# ----------------------
face_model = insightface.app.FaceAnalysis(name="buffalo_l")  # model lớn
face_model.prepare(ctx_id=-1, det_size=(640, 640))           # CPU


# ----------------------
# Utils
# ----------------------
def compute_embedding_insightface(img_bytes):
    """Chuyển ảnh bytes sang embedding InsightFace."""
    try:
        img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        img_np = np.array(img)

        # Chuyển RGB sang BGR vì InsightFace dùng OpenCV
        img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

        faces = face_model.get(img_bgr)
        if not faces:
            print("Không tìm thấy mặt")
            return None

        return faces[0].embedding.tolist()

    except Exception as e:
        print("Lỗi compute_embedding_insightface:", e)
        return None


# ----------------------
# Teacher CRUD
# ----------------------
@app.post("/teachers/")
async def create_teacher(name: str = Form(...), email: str = Form(...), password_hash: str = Form(...)):
    doc = {"name": name, "email": email, "password_hash": password_hash, "class_ids": []}
    res = await db.teachers.insert_one(doc)
    return {"teacher_id": str(res.inserted_id)}


# ----------------------
# Class CRUD
# ----------------------
@app.post("/classes/")
async def create_class(name: str = Form(...), teacher_id: str = Form(...)):
    doc = {"name": name, "teacher_id": teacher_id, "student_ids": []}
    res = await db.classes.insert_one(doc)
    return {"class_id": str(res.inserted_id)}


# ----------------------
# Student CRUD + embedding
# ----------------------
@app.post("/students/")
async def create_student(
    name: str = Form(...),
    mssv: str = Form(...),
    class_id: str = Form(...),
    file: UploadFile = File(...)
):
    # ====== VALIDATE class_id ======
    if not ObjectId.is_valid(class_id):
        return {"ok": False, "msg": "class_id không hợp lệ (phải là ObjectId 24 ký tự)"}

    content = await file.read()

    # Tính embedding trong thread pool
    loop = asyncio.get_event_loop()
    embedding = await loop.run_in_executor(executor, compute_embedding_insightface, content)
    if embedding is None:
        return {"ok": False, "msg": "Không tìm thấy mặt trong ảnh"}

    # Save image
    fname = f"{mssv}_{int(datetime.utcnow().timestamp())}.jpg"
    path = os.path.join(IMAGE_DIR, fname)
    with open(path, "wb") as f:
        f.write(content)

    # Save student vào DB
    doc = {
        "name": name,
        "mssv": mssv,
        "class_id": class_id,           # class_id lưu dạng string
        "face_embedding": embedding,
        "avatar_url": path
    }
    res = await db.students.insert_one(doc)

    # Update class student list
    await db.classes.update_one(
        {"_id": ObjectId(class_id)},
        {"$push": {"student_ids": str(res.inserted_id)}}
    )

    return {"ok": True, "student_id": str(res.inserted_id)}


# ----------------------
# Attendance manual
# ----------------------
@app.post("/attendance/")
async def mark_attendance(class_id: str = Form(...), student_id: str = Form(...), status: str = Form(...)):
    # Validate ObjectId
    if not ObjectId.is_valid(class_id):
        return {"ok": False, "msg": "class_id không hợp lệ"}
    if not ObjectId.is_valid(student_id):
        return {"ok": False, "msg": "student_id không hợp lệ"}

    doc = {
        "class_id": class_id,
        "student_id": student_id,
        "time": datetime.utcnow(),
        "status": status
    }
    res = await db.attendance.insert_one(doc)
    return {"ok": True, "attendance_id": str(res.inserted_id)}


# ----------------------
# AI Recognition / Điểm danh tự động
# ----------------------
@app.post("/recognize/")
async def recognize(file: UploadFile = File(...), class_id: str = Form(...)):
    # Validate class_id
    if not ObjectId.is_valid(class_id):
        return {"ok": False, "msg": "class_id không hợp lệ"}

    content = await file.read()

    loop = asyncio.get_event_loop()
    emb = await loop.run_in_executor(executor, compute_embedding_insightface, content)
    if emb is None:
        return {"ok": True, "results": [], "msg": "Không nhận diện được mặt"}

    emb_norm = np.array(emb) / np.linalg.norm(emb)

    # Lấy toàn bộ sinh viên của lớp
    cursor = db.students.find({"class_id": class_id})
    results = []

    async for student in cursor:
        student_emb = np.array(student["face_embedding"])
        student_emb_norm = student_emb / np.linalg.norm(student_emb)
        score = float(np.dot(emb_norm, student_emb_norm))

        if score >= 0.7:  # ngưỡng 70%
            results.append({
                "name": student["name"],
                "score": score
            })

            # Tự động điểm danh
            await db.attendance.insert_one({
                "class_id": class_id,
                "student_id": str(student["_id"]),  # vẫn lưu trong DB để quản lý
                "time": datetime.utcnow(),
                "status": "present"
            })

    return {"ok": True, "results": results}