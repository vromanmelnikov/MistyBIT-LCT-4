from io import BytesIO
import os
from fastapi import FastAPI, File, Response, UploadFile
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import string
import random
import glob
import zipfile

from config import settings


NAME_DIR = "public"


def generate_img_name(n: int):
    return "".join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(n)
    )


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_URL,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/static", StaticFiles(directory=NAME_DIR))


@app.post("/")
async def upload_img(file: UploadFile = File(...)):
    names = file.filename.split(".")
    filename = names[0].replace(" ", "_")
    f_n = f"{filename}_{generate_img_name(16)}.{names[1]}"
    file_location = f"{NAME_DIR}/{f_n}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
    return f_n


@app.delete("/")
async def upload_img(filename: str):
    filename = f"{NAME_DIR}/{filename}"
    os.remove(filename)
    return "Ok"


@app.post("/download")
async def download_folder():
    return await _zipfiles(glob.glob("public/*"))


async def _zipfiles(file_list):
    io = BytesIO()
    zip_sub_dir = "final_archive"
    zip_filename = "%s.zip" % zip_sub_dir
    with zipfile.ZipFile(io, mode="w", compression=zipfile.ZIP_DEFLATED) as zip:
        for fpath in file_list:
            zip.write(fpath)
        # close zip
        zip.close()
    return StreamingResponse(
        iter([io.getvalue()]),
        media_type="application/x-zip-compressed",
        headers={"Content-Disposition": f"attachment;filename=%s" % zip_filename},
    )
