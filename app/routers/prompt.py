from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import SessionLocal
from app.models.prompt import Prompt
from app.schemas.prompt import PromptCreate, PromptUpdate, PromptResponse
from app.dependencies import get_current_user
from app.models.user import User

router = APIRouter()

# Dependência para injetar a sessão do banco de dados
async def get_db():
    async with SessionLocal() as session:
        yield session

# Criar um novo prompt
@router.post("/", response_model=PromptResponse)
async def create_prompt(
    prompt: PromptCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Verifica se já existe um prompt com o mesmo nome
    existing_prompt = await db.execute(select(Prompt).where(Prompt.name == prompt.name))
    if existing_prompt.scalars().first():
        raise HTTPException(status_code=400, detail="Prompt name already exists.")

    new_prompt = Prompt(
        name=prompt.name,
        content=prompt.content,
        created_by=current_user.id,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    db.add(new_prompt)
    await db.commit()
    await db.refresh(new_prompt)
    # Retorna a resposta formatada
    return PromptResponse(
        id=new_prompt.id,
        name=new_prompt.name,
        content=new_prompt.content,
        version=new_prompt.version,
        created_by=new_prompt.created_by,
        created_at=new_prompt.created_at.isoformat(),
        updated_at=new_prompt.updated_at.isoformat(),
    )

# Listar todos os prompts
@router.get("/", response_model=list[PromptResponse])
async def list_prompts(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Prompt))
    prompts = result.scalars().all()
    # Converte os prompts para o formato esperado pelo PromptResponse
    response = [
        PromptResponse(
            id=prompt.id,
            name=prompt.name,
            content=prompt.content,
            version=prompt.version,
            created_by=prompt.created_by,
            created_at=prompt.created_at.isoformat(),  # Converte para string
            updated_at=prompt.updated_at.isoformat(),  # Converte para string
        )
        for prompt in prompts
    ]
    return response

# Obter um prompt por ID
@router.get("/{prompt_id}", response_model=PromptResponse)
async def get_prompt(prompt_id: int, db: AsyncSession = Depends(get_db)):
    prompt = await db.get(Prompt, prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    # Retorna a resposta formatada
    return PromptResponse(
        id=prompt.id,
        name=prompt.name,
        content=prompt.content,
        version=prompt.version,
        created_by=prompt.created_by,
        created_at=prompt.created_at.isoformat(),  # Converte para string
        updated_at=prompt.updated_at.isoformat(),  # Converte para string
    )

# Atualizar um prompt
@router.put("/{prompt_id}", response_model=PromptResponse)
async def update_prompt(
    prompt_id: int,
    prompt_data: PromptUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    prompt = await db.get(Prompt, prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")

    # Permite que apenas o criador do prompt o edite
    if prompt.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this prompt")

    for key, value in prompt_data.dict(exclude_unset=True).items():
        setattr(prompt, key, value)

    await db.commit()
    await db.refresh(prompt)
    # Retorna a resposta formatada
    return PromptResponse(
        id=prompt.id,
        name=prompt.name,
        content=prompt.content,
        version=prompt.version,
        created_by=prompt.created_by,
        created_at=prompt.created_at.isoformat(),  # Converte para string
        updated_at=prompt.updated_at.isoformat(),  # Converte para string
    )

# Excluir um prompt
@router.delete("/{prompt_id}")
async def delete_prompt(
    prompt_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    prompt = await db.get(Prompt, prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")

    # Permite que apenas o criador ou admin exclua o prompt
    if prompt.created_by != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to delete this prompt")

    await db.delete(prompt)
    await db.commit()
    return {"detail": "Prompt deleted successfully"}
