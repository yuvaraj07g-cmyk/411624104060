"""Document listing and retrieval endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Request

from rti_mate.api.deps import get_repo
from rti_mate.db.repository import FILTER_KEY, DocumentRepository

router = APIRouter()


@router.get("/documents")
async def list_documents(
    request: Request,
    repository: Annotated[DocumentRepository, Depends(get_repo)],
    q: str | None = None,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    reserved = {"q", "limit", "offset"}
    filters = {key: value for key, value in request.query_params.items() if key not in reserved}
    invalid = [key for key in filters if not FILTER_KEY.fullmatch(key)]
    if invalid:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid filter name: {invalid[0]}",
        )
    total, items = await repository.list(q=q, filters=filters, limit=limit, offset=offset)
    return {"total": total, "items": items, "filters": filters}


@router.get("/documents/{document_id}")
async def get_document(
    document_id: str,
    repository: Annotated[DocumentRepository, Depends(get_repo)],
):
    record = await repository.get(document_id)
    if record is None:
        raise HTTPException(status_code=404, detail=f"No document with id '{document_id}'.")
    return record
