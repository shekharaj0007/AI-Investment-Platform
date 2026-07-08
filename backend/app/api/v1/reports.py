from fastapi import APIRouter, File, Form, UploadFile

from app.schemas.financial import ReportAnswer, ReportQuestionRequest, ReportUploadResponse
from app.services.report_reader import ReportReaderService

router = APIRouter()
_service = ReportReaderService()


@router.post("/upload", response_model=ReportUploadResponse)
async def upload_report(
    file: UploadFile = File(...),
    company_symbol: str = Form(...),
) -> ReportUploadResponse:
    content = await file.read()
    return await _service.upload(file.filename or "report.pdf", content, company_symbol)


@router.post("/{report_id}/ask", response_model=ReportAnswer)
async def ask_report(report_id: int, body: ReportQuestionRequest) -> ReportAnswer:
    return await _service.ask(report_id, body.question)
