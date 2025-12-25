"""
字典数据接口：学校、专业等基础数据查询
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from app.db.session import get_session
from app.repositories.school import SchoolRepository
from app.repositories.major import MajorRepository
from app.models.school import School
from app.models.major import Major
from pydantic import BaseModel

router = APIRouter(prefix="/dict", tags=["字典数据"])
school_repo = SchoolRepository()
major_repo = MajorRepository()


class SchoolResponse(BaseModel):
    """学校响应模型"""
    id: int
    name: str
    code: Optional[str] = None
    province: Optional[str] = None
    city: Optional[str] = None


@router.get("/schools", response_model=List[SchoolResponse])
def get_schools(
    province: Optional[str] = Query(None, description="省份筛选"),
    city: Optional[str] = Query(None, description="城市筛选"),
    keyword: Optional[str] = Query(None, description="关键词搜索（学校名称）"),
    session: Session = Depends(get_session),
):
    """
    获取学校列表
    - 支持按省份、城市筛选
    - 支持关键词搜索
    """
    # 构建查询
    stmt = school_repo._base_stmt()
    
    if province:
        stmt = stmt.where(School.province == province)
    
    if city:
        stmt = stmt.where(School.city == city)
    
    if keyword:
        stmt = stmt.where(School.name.contains(keyword))
    
    # 按名称排序
    stmt = stmt.order_by(School.name)
    
    schools = list(session.exec(stmt).all())
    
    return [
        SchoolResponse(
            id=school.id,
            name=school.name,
            code=school.code,
            province=school.province,
            city=school.city,
        )
        for school in schools
    ]


@router.get("/schools/{school_id}", response_model=SchoolResponse)
def get_school(
    school_id: int,
    session: Session = Depends(get_session),
):
    """获取学校详情"""
    school = school_repo.get(session, school_id)
    if not school:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="学校不存在",
        )
    
    return SchoolResponse(
        id=school.id,
        name=school.name,
        code=school.code,
        province=school.province,
        city=school.city,
    )


@router.get("/provinces", response_model=List[str])
def get_provinces(
    session: Session = Depends(get_session),
):
    """
    获取所有省份列表（去重）
    """
    from sqlmodel import select, distinct
    stmt = (
        select(distinct(School.province))
        .where(School.is_deleted == 0)
        .where(School.province.isnot(None))
        .order_by(School.province)
    )
    provinces = list(session.exec(stmt).all())
    return [p for p in provinces if p]


@router.get("/cities", response_model=List[str])
def get_cities(
    province: Optional[str] = Query(None, description="省份筛选"),
    session: Session = Depends(get_session),
):
    """
    获取城市列表（去重）
    - 支持按省份筛选
    """
    from sqlmodel import select, distinct
    stmt = (
        select(distinct(School.city))
        .where(School.is_deleted == 0)
        .where(School.city.isnot(None))
    )
    
    if province:
        stmt = stmt.where(School.province == province)
    
    stmt = stmt.order_by(School.city)
    
    cities = list(session.exec(stmt).all())
    return [c for c in cities if c]


class MajorResponse(BaseModel):
    """专业响应模型"""
    id: int
    name: str
    code: Optional[str] = None
    category: Optional[str] = None
    school_id: Optional[int] = None


@router.get("/majors", response_model=List[MajorResponse])
def get_majors(
    school_id: Optional[int] = Query(None, description="学校ID（不传则返回通用专业）"),
    keyword: Optional[str] = Query(None, description="关键词搜索（专业名称）"),
    session: Session = Depends(get_session),
):
    """
    获取专业列表
    - 支持按学校筛选
    - 支持关键词搜索
    """
    if keyword:
        majors = major_repo.search_by_keyword(session, keyword)
    else:
        majors = major_repo.get_by_school(session, school_id)
    
    return [
        MajorResponse(
            id=major.id,
            name=major.name,
            code=major.code,
            category=major.category,
            school_id=major.school_id,
        )
        for major in majors
    ]


@router.get("/major-categories", response_model=List[str])
def get_major_categories(
    session: Session = Depends(get_session),
):
    """
    获取所有专业类别列表（去重）
    """
    from sqlmodel import select, distinct
    stmt = (
        select(distinct(Major.category))
        .where(Major.is_deleted == 0)
        .where(Major.category.isnot(None))
        .order_by(Major.category)
    )
    categories = list(session.exec(stmt).all())
    return [c for c in categories if c]

