from sqlalchemy.orm import Session
from sqlalchemy import func, extract, or_, and_
from datetime import datetime, timedelta
from typing import List, Optional
from . import models, schemas
import os
import json

def get_application(db: Session, application_id: int):
    return db.query(models.JobApplication).filter(models.JobApplication.id == application_id).first()

def get_applications(db: Session, skip: int = 0, limit: int = 100, status: Optional[str] = None, 
                     domain: Optional[str] = None, search: Optional[str] = None, 
                     work_type: Optional[str] = None, tags: Optional[str] = None,
                     include_archived: bool = False, sort_by: str = "created_at", 
                     sort_order: str = "desc"):
    query = db.query(models.JobApplication)
    
    # Filter by archived status
    if not include_archived:
        query = query.filter(models.JobApplication.is_archived == 0)
    
    # Filter by status
    if status:
        query = query.filter(models.JobApplication.status == status)
    
    # Filter by domain
    if domain:
        query = query.filter(models.JobApplication.domain == domain)
    
    # Filter by work type
    if work_type:
        query = query.filter(models.JobApplication.work_type == work_type)
    
    # Filter by tags
    if tags:
        tag_list = tags.split(',')
        for tag in tag_list:
            query = query.filter(models.JobApplication.tags.contains(tag.strip()))
    
    # Global search across multiple fields
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                models.JobApplication.company_name.ilike(search_term),
                models.JobApplication.job_title.ilike(search_term),
                models.JobApplication.location.ilike(search_term),
                models.JobApplication.domain.ilike(search_term),
                models.JobApplication.notes.ilike(search_term),
                models.JobApplication.job_description.ilike(search_term)
            )
        )
    
    # Sorting
    sort_column = getattr(models.JobApplication, sort_by, models.JobApplication.created_at)
    if sort_order == "asc":
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())
    
    return query.offset(skip).limit(limit).all()

def create_application(db: Session, application: schemas.JobApplicationCreate):
    app_data = application.model_dump()
    
    # Initialize status history with the initial status
    status = app_data.get("status", "Saved")
    
    # Set appropriate notes based on status
    if status in ["Saved", "To Apply"]:
        notes = "Job saved for later"
    else:
        notes = "Application submitted"
    
    initial_status = {
        "status": status,
        "date": app_data.get("application_date", datetime.now()).isoformat() if app_data.get("application_date") else datetime.now().isoformat(),
        "notes": notes
    }
    app_data["status_history"] = [initial_status]
    
    db_application = models.JobApplication(**app_data)
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return db_application

def update_application(db: Session, application_id: int, application: schemas.JobApplicationUpdate):
    db_application = get_application(db, application_id)
    if db_application:
        update_data = application.model_dump(exclude_unset=True)
        
        # Check if status is being updated
        if "status" in update_data and update_data["status"] != db_application.status:
            # Get status_date and status_notes from update_data
            status_date = update_data.pop("status_date", None) or datetime.now()
            status_notes = update_data.pop("status_notes", None)
            
            # Create new status history entry
            new_status_entry = {
                "status": update_data["status"],
                "date": status_date.isoformat() if isinstance(status_date, datetime) else status_date,
                "notes": status_notes
            }
            
            # Update status history
            if db_application.status_history is None:
                db_application.status_history = []
            
            # Convert to list if it's not already
            status_history = list(db_application.status_history) if db_application.status_history else []
            status_history.append(new_status_entry)
            db_application.status_history = status_history
        else:
            # Remove status_date and status_notes if status didn't change
            update_data.pop("status_date", None)
            update_data.pop("status_notes", None)
        
        # Apply other updates
        for field, value in update_data.items():
            setattr(db_application, field, value)
        
        db.commit()
        db.refresh(db_application)
    return db_application

def delete_application(db: Session, application_id: int):
    db_application = get_application(db, application_id)
    if db_application:
        # Delete associated files
        if db_application.cv_filepath and os.path.exists(db_application.cv_filepath):
            os.remove(db_application.cv_filepath)
        if db_application.coverletter_filepath and os.path.exists(db_application.coverletter_filepath):
            os.remove(db_application.coverletter_filepath)
        
        db.delete(db_application)
        db.commit()
        return True
    return False

def update_document(db: Session, application_id: int, doc_type: str, filename: str, filepath: str):
    db_application = get_application(db, application_id)
    if db_application:
        if doc_type == "cv":
            # Delete old CV if exists
            if db_application.cv_filepath and os.path.exists(db_application.cv_filepath):
                os.remove(db_application.cv_filepath)
            db_application.cv_filename = filename
            db_application.cv_filepath = filepath
        elif doc_type == "coverletter":
            # Delete old cover letter if exists
            if db_application.coverletter_filepath and os.path.exists(db_application.coverletter_filepath):
                os.remove(db_application.coverletter_filepath)
            db_application.coverletter_filename = filename
            db_application.coverletter_filepath = filepath
        
        db.commit()
        db.refresh(db_application)
    return db_application

def get_statistics(db: Session):
    total = db.query(models.JobApplication).count()
    
    # By status
    status_counts = db.query(
        models.JobApplication.status,
        func.count(models.JobApplication.id)
    ).group_by(models.JobApplication.status).all()
    by_status = {status: count for status, count in status_counts}
    
    # By domain
    domain_counts = db.query(
        models.JobApplication.domain,
        func.count(models.JobApplication.id)
    ).filter(models.JobApplication.domain.isnot(None)).group_by(models.JobApplication.domain).all()
    by_domain = {domain: count for domain, count in domain_counts}
    
    # By work type
    work_type_counts = db.query(
        models.JobApplication.work_type,
        func.count(models.JobApplication.id)
    ).filter(models.JobApplication.work_type.isnot(None)).group_by(models.JobApplication.work_type).all()
    by_work_type = {work_type: count for work_type, count in work_type_counts}
    
    # Recent applications (last 7 days)
    seven_days_ago = datetime.now() - timedelta(days=7)
    recent = db.query(models.JobApplication).filter(
        models.JobApplication.application_date >= seven_days_ago
    ).count()
    
    return schemas.ApplicationStats(
        total_applications=total,
        by_status=by_status,
        by_domain=by_domain,
        by_work_type=by_work_type,
        recent_applications=recent
    )

def get_all_applications_for_export(db: Session) -> List[models.JobApplication]:
    return db.query(models.JobApplication).order_by(models.JobApplication.application_date.desc()).all()

# Archive/Unarchive
def archive_application(db: Session, application_id: int, archive: bool = True):
    db_application = get_application(db, application_id)
    if db_application:
        db_application.is_archived = 1 if archive else 0
        db.commit()
        db.refresh(db_application)
    return db_application

# Bulk operations
def bulk_delete_applications(db: Session, application_ids: List[int]):
    count = 0
    for app_id in application_ids:
        if delete_application(db, app_id):
            count += 1
    return count

def bulk_archive_applications(db: Session, application_ids: List[int], archive: bool = True):
    count = 0
    for app_id in application_ids:
        if archive_application(db, app_id, archive):
            count += 1
    return count

def bulk_update_status(db: Session, application_ids: List[int], status: str):
    count = 0
    for app_id in application_ids:
        db_application = get_application(db, app_id)
        if db_application:
            db_application.status = status
            # Add to status history
            new_status_entry = {
                "status": status,
                "date": datetime.now().isoformat(),
                "notes": "Bulk status update"
            }
            status_history = list(db_application.status_history) if db_application.status_history else []
            status_history.append(new_status_entry)
            db_application.status_history = status_history
            db.commit()
            count += 1
    return count

# Get all unique tags
def get_all_tags(db: Session) -> List[str]:
    applications = db.query(models.JobApplication).all()
    all_tags = set()
    for app in applications:
        if app.tags:
            # Handle both list and JSON string formats
            if isinstance(app.tags, list):
                all_tags.update(app.tags)
            elif isinstance(app.tags, str):
                try:
                    tags_list = json.loads(app.tags)
                    all_tags.update(tags_list)
                except:
                    pass
    return sorted(list(all_tags))

