from contextlib import contextmanager
from models import SessionLocal, User, LoanApplication, EditRequest, AuditLog, LoanStatus
from sqlalchemy.exc import NoResultFound, IntegrityError


@contextmanager
def session_scope():
    """Manages DB session lifecycle and ensures rollback on failure."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


# --------------------------------------------
# USER MANAGEMENT
# --------------------------------------------
def get_or_create_user(session, auth0_id, name, email):
    """
    Ensures users are not duplicated and database uniqueness is respected.

    - Checks by email first (primary identity key).
    - Updates missing auth0_id if needed.
    """

    # Check by email first (email is unique)
    user = session.query(User).filter(User.email == email).first()

    if user:
        # If user exists but does not have Auth0 ID stored, update it
        if not user.auth0_id or user.auth0_id != auth0_id:
            user.auth0_id = auth0_id
        return user

    # User does not exist → create one
    user = User(
        auth0_id=auth0_id,
        name=name,
        email=email,
        role="pending"  # User must select role on first login
    )
    session.add(user)

    try:
        session.flush()
        session.refresh(user)
    except IntegrityError:
        # Safety fallback: if someone else added the same email in parallel
        session.rollback()
        user = session.query(User).filter(User.email == email).first()

    return user


# --------------------------------------------
# LOAN MANAGEMENT
# --------------------------------------------
def save_loan(session, user_id, application_data):
    """
    Creates a new loan entry with pending status.
    """
    loan = LoanApplication(
        user_id=user_id,
        application_data=application_data,
        status=LoanStatus.pending
    )
    session.add(loan)
    session.flush()
    session.refresh(loan)
    return loan


def list_user_loans(session, user_id):
    return (
        session.query(LoanApplication)
        .filter(LoanApplication.user_id == user_id)
        .order_by(LoanApplication.created_at.desc())
        .all()
    )


def list_pending_loans(session):
    return (
        session.query(LoanApplication)
        .filter(LoanApplication.status == LoanStatus.pending)
        .order_by(LoanApplication.created_at.asc())
        .all()
    )


# --------------------------------------------
# EDIT REQUEST
# --------------------------------------------
def create_edit_request(session, **kwargs):
    req = EditRequest(**kwargs)
    session.add(req)
    session.flush()
    session.refresh(req)
    return req


# --------------------------------------------
# LOGGING
# --------------------------------------------
def log_action(session, user_id, action: str):
    """
    Saves an audit log entry.
    """
    if not action:
        return

    log = AuditLog(user_id=user_id, action=action)
    session.add(log)
