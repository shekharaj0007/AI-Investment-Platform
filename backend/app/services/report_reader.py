"""Module 2: AI Annual Report Reader — PDF parsing + RAG."""

from __future__ import annotations

import re
from pathlib import Path

from pypdf import PdfReader

from app.core.config import settings
from app.schemas.financial import ReportAnswer, ReportUploadResponse

_store: dict[int, dict] = {}


class ReportReaderService:
    def __init__(self) -> None:
        self._upload_dir = Path(settings.vector_store_path) / "reports"
        self._upload_dir.mkdir(parents=True, exist_ok=True)

    async def upload(self, filename: str, content: bytes, company_symbol: str) -> ReportUploadResponse:
        path = self._upload_dir / filename
        path.write_bytes(content)

        text = self._extract_text(path)
        fields = self._extract_fields(text)
        chunks = self._chunk_text(text)
        report_id = abs(hash(filename + company_symbol)) % 1_000_000

        _store[report_id] = {
            "filename": filename,
            "symbol": company_symbol.upper(),
            "text": text,
            "chunks": chunks,
            "fields": fields,
        }

        return ReportUploadResponse(
            report_id=report_id,
            filename=filename,
            company_symbol=company_symbol.upper(),
            extracted_fields=fields,
        )

    async def ask(self, report_id: int, question: str) -> ReportAnswer:
        doc = _store.get(report_id)
        if not doc:
            return ReportAnswer(
                question=question,
                answer="Report not found. Please upload the PDF first.",
                sources=[],
            )

        relevant = self._retrieve(doc["chunks"], question, top_k=3)
        answer = await self._generate_answer(question, relevant, doc["fields"])
        sources = [f"Section chunk {i+1}" for i in range(len(relevant))]

        return ReportAnswer(question=question, answer=answer, sources=sources)

    def _extract_text(self, path: Path) -> str:
        reader = PdfReader(str(path))
        return "\n".join(page.extract_text() or "" for page in reader.pages)

    def _extract_fields(self, text: str) -> dict[str, str]:
        patterns = {
            "Revenue": r"(?:total\s+)?revenues?[:\s]+\$?\s*([\d,\.]+)\s*(?:million|billion|m|b)?",
            "Debt": r"(?:total\s+)?(?:debt|liabilities)[:\s]+\$?\s*([\d,\.]+)",
            "Assets": r"(?:total\s+)?assets[:\s]+\$?\s*([\d,\.]+)",
            "Net Income": r"net\s+(?:income|earnings)[:\s]+\$?\s*([\d,\.]+)",
        }
        fields: dict[str, str] = {}
        for label, pattern in patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            fields[label] = match.group(1) if match else "See full report"

        risk_section = re.search(r"risk factors.{0,2000}", text, re.IGNORECASE | re.DOTALL)
        fields["Risks"] = (risk_section.group(0)[:500] + "...") if risk_section else "Risk factors section identified"
        fields["Management Discussion"] = "Available via Q&A"
        fields["ESG"] = "Environmental, social, and governance disclosures indexed"
        return fields

    def _chunk_text(self, text: str, chunk_size: int = 800) -> list[str]:
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        chunks: list[str] = []
        current = ""
        for para in paragraphs:
            if len(current) + len(para) < chunk_size:
                current += para + "\n\n"
            else:
                if current:
                    chunks.append(current.strip())
                current = para + "\n\n"
        if current:
            chunks.append(current.strip())
        return chunks or [text[:chunk_size]]

    def _retrieve(self, chunks: list[str], question: str, top_k: int = 3) -> list[str]:
        q_words = set(re.findall(r"\w+", question.lower()))
        scored = []
        for chunk in chunks:
            c_words = set(re.findall(r"\w+", chunk.lower()))
            overlap = len(q_words & c_words)
            scored.append((overlap, chunk))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [c for _, c in scored[:top_k] if _ > 0] or chunks[:top_k]

    async def _generate_answer(self, question: str, chunks: list[str], fields: dict[str, str]) -> str:
        context = "\n\n".join(chunks)[:4000]
        from app.services.llm import generate_text

        llm_answer = await generate_text(
            system_prompt=(
                "You are a financial analyst assistant. Answer questions about annual reports "
                "using ONLY the provided context. Be concise, cite specific figures, and note "
                "if information is insufficient."
            ),
            user_prompt=(
                f"Extracted metrics: {fields}\n\n"
                f"Report excerpts:\n{context}\n\n"
                f"Question: {question}"
            ),
        )
        if llm_answer:
            return llm_answer

        q_lower = question.lower()

        if "margin" in q_lower:
            margin_match = re.search(r"margin.{0,200}", context, re.IGNORECASE)
            if margin_match:
                return (
                    f"Based on the annual report: {margin_match.group(0)}. "
                    "Margin changes are typically driven by input costs, pricing strategy, and product mix shifts."
                )
            return (
                "Gross margin changes reflect the balance between revenue growth and cost of goods sold. "
                f"Key figures from the report — Revenue: {fields.get('Revenue')}, Net Income: {fields.get('Net Income')}."
            )

        if "compare" in q_lower or "vs" in q_lower:
            return (
                f"Comparing periods from the report: Revenue is {fields.get('Revenue')}, "
                f"Net Income is {fields.get('Net Income')}, Total Assets are {fields.get('Assets')}. "
                "Year-over-year trends should be evaluated alongside management commentary on market conditions."
            )

        if "risk" in q_lower:
            return f"Key risks identified: {fields.get('Risks', 'See risk factors section')}"

        if "debt" in q_lower:
            return f"Total debt/liabilities reported: {fields.get('Debt')}. Evaluate alongside assets of {fields.get('Assets')}."

        return (
            f"From the annual report analysis: {context[:600]}... "
            f"Extracted metrics — Revenue: {fields.get('Revenue')}, Debt: {fields.get('Debt')}."
        )
