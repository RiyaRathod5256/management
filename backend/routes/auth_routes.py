from flask import Blueprint, request, jsonify
from models.user import User
from models.project import Project
from models.team_member import TeamMember
from extensions import db
from models.task import Task
from datetime import date

import bcrypt
import re

from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)

auth = Blueprint('auth', __name__)


# =====================================================
# REGISTER
# =====================================================

@auth.route('/register', methods=['POST'])
def register():

    data = request.get_json()

    # -----------------------------------
    # GET DATA
    # -----------------------------------

    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    # -----------------------------------
    # EMPTY FIELD VALIDATION
    # -----------------------------------

    if not name:
        return jsonify({
            'message': 'Name is required'
        }), 400

    if not email:
        return jsonify({
            'message': 'Email is required'
        }), 400

    if not password:
        return jsonify({
            'message': 'Password is required'
        }), 400

    name = name.strip()
    email = email.strip().lower()

    # -----------------------------------
    # NAME VALIDATION
    # -----------------------------------

    if len(name) < 3:
        return jsonify({
            'message': 'Name must be at least 3 characters'
        }), 400

    if len(name) > 50:
        return jsonify({
            'message': 'Name must not exceed 50 characters'
        }), 400

    name_pattern = r'^[A-Za-z ]+$'

    if not re.match(name_pattern, name):
        return jsonify({
            'message': (
                'Name must contain only letters and spaces'
            )
        }), 400

    # -----------------------------------
    # EMAIL VALIDATION
    # -----------------------------------

    email_pattern = (
        r'^[A-Za-z]'
        r'[A-Za-z0-9._%+-]*'
        r'@[A-Za-z0-9]+'
        r'([.-][A-Za-z0-9]+)*'
        r'\.[A-Za-z]{2,}$'
    )

    if not re.match(email_pattern, email):
        return jsonify({
            'message': 'Invalid email format'
        }), 400

    # -----------------------------------
    # PASSWORD VALIDATION
    # -----------------------------------

    if len(password) < 8:
        return jsonify({
            'message': (
                'Password must be at least 8 characters'
            )
        }), 400

    password_pattern = (
        r'^(?=.*[a-z])'
        r'(?=.*[A-Z])'
        r'(?=.*\d)'
        r'(?=.*[@$!%*?&])'
        r'[A-Za-z\d@$!%*?&]{8,}$'
    )

    if not re.match(password_pattern, password):
        return jsonify({
            'message': (
                'Password must contain uppercase, '
                'lowercase, number and special character'
            )
        }), 400

    # -----------------------------------
    # CHECK EXISTING USER
    # -----------------------------------

    existing_user = User.query.filter_by(
        email=email
    ).first()

    if existing_user:
        return jsonify({
            'message': 'Email already exists'
        }), 409

    # -----------------------------------
    # HASH PASSWORD
    # -----------------------------------

    hashed_password = bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')

    # -----------------------------------
    # CREATE USER
    # -----------------------------------

    new_user = User(
        name=name,
        email=email,
        password=hashed_password,
        role='member'
    )

    db.session.add(new_user)
    db.session.commit()

    # -----------------------------------
    # RESPONSE
    # -----------------------------------

    return jsonify({
        'message': 'User registered successfully'
    }), 201


# =====================================================
# LOGIN
# =====================================================

@auth.route('/login', methods=['POST'])
def login():

    data = request.get_json()

    # -----------------------------------
    # GET DATA
    # -----------------------------------

    email = data.get('email')
    password = data.get('password')

    # -----------------------------------
    # EMPTY FIELD VALIDATION
    # -----------------------------------

    if not email:
        return jsonify({
            'message': 'Email is required'
        }), 400

    if not password:
        return jsonify({
            'message': 'Password is required'
        }), 400

    email = email.strip().lower()

    # -----------------------------------
    # EMAIL VALIDATION
    # -----------------------------------

    email_pattern = (
        r'^[A-Za-z]'
        r'[A-Za-z0-9._%+-]*'
        r'@[A-Za-z0-9]+'
        r'([.-][A-Za-z0-9]+)*'
        r'\.[A-Za-z]{2,}$'
    )

    if not re.match(email_pattern, email):
        return jsonify({
            'message': 'Invalid email format'
        }), 400

    # -----------------------------------
    # FIND USER
    # -----------------------------------

    user = User.query.filter_by(
        email=email
    ).first()

    if not user:
        return jsonify({
            'message': 'Invalid email or password'
        }), 401

    # -----------------------------------
    # VERIFY PASSWORD
    # -----------------------------------

    is_password_correct = bcrypt.checkpw(
        password.encode('utf-8'),
        user.password.encode('utf-8')
    )

    if not is_password_correct:
        return jsonify({
            'message': 'Invalid email or password'
        }), 401

    # -----------------------------------
    # CREATE JWT TOKEN
    # -----------------------------------

    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={
            'role': user.role
        }
    )

    # -----------------------------------
    # RESPONSE
    # -----------------------------------

    return jsonify({
        'message': 'Login successful',
        'token': access_token,
        'user': {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'role': user.role
        }
    }), 200


# =====================================================
# CREATE PROJECT
# =====================================================

@auth.route('/create-project', methods=['POST'])
@jwt_required()
def create_project():

    current_user_id = get_jwt_identity()

    claims = get_jwt()

    current_user_role = claims['role']

    if current_user_role != 'admin':

        return jsonify({
            'message': 'Only admin can create projects'
        }), 403

    data = request.get_json()

    title = data.get('title')
    description = data.get('description')

    # -----------------------------------
    # VALIDATION
    # -----------------------------------

    if not title:

        return jsonify({
            'message': 'Project title is required'
        }), 400

    # -----------------------------------
    # CREATE PROJECT
    # -----------------------------------

    new_project = Project(
        title=title,
        description=description,
        created_by=current_user_id
    )

    db.session.add(new_project)
    db.session.commit()

    # -----------------------------------
    # RESPONSE
    # -----------------------------------

    return jsonify({
        'message': 'Project created successfully'
    }), 201


# =====================================================
# GET PROJECT
# =====================================================

@auth.route('/project/<int:id>', methods=['GET'])
@jwt_required()
def get_project(id):

    current_user_id = get_jwt_identity()

    project = Project.query.filter_by(
        id=id,
        created_by=current_user_id
    ).first()

    if not project:
        return jsonify({
            "msg": "Project not found"
        }), 404

    return jsonify({
        "id": project.id,
        "title": project.title,
        "description": project.description
    }), 200


# =====================================================
# UPDATE PROJECT
# =====================================================

@auth.route('/project/<int:id>', methods=['PUT'])
@jwt_required()
def update_project(id):

    current_user_id = get_jwt_identity()

    project = Project.query.filter_by(
        id=id,
        created_by=current_user_id
    ).first()

    if not project:
        return jsonify({
            "msg": "Project not found"
        }), 404

    data = request.get_json()

    project.title = data.get(
        'title',
        project.title
    )

    project.description = data.get(
        'description',
        project.description
    )

    db.session.commit()

    return jsonify({
        "msg": "Project updated"
    }), 200


# =====================================================
# DELETE PROJECT
# =====================================================

@auth.route('/project/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_project(id):

    current_user_id = get_jwt_identity()

    project = Project.query.filter_by(
        id=id,
        created_by=current_user_id
    ).first()

    if not project:
        return jsonify({
            "msg": "Project not found"
        }), 404

    db.session.delete(project)
    db.session.commit()

    return jsonify({
        "msg": "Project deleted"
    }), 200


# =====================================================
# ADD MEMBER
# =====================================================

@auth.route('/add-member', methods=['POST'])
@jwt_required()
def add_member():

    claims = get_jwt()

    current_user_role = claims['role']

    # -----------------------------------
    # ADMIN CHECK
    # -----------------------------------

    if current_user_role != 'admin':

        return jsonify({
            'message': 'Only admin can add members'
        }), 403

    # -----------------------------------
    # GET REQUEST DATA
    # -----------------------------------

    data = request.get_json()

    project_id = data.get('project_id')
    user_id = data.get('user_id')

    # -----------------------------------
    # VALIDATION
    # -----------------------------------

    if not project_id or not user_id:

        return jsonify({
            'message': 'Project ID and User ID required'
        }), 400

    # -----------------------------------
    # CHECK PROJECT
    # -----------------------------------

    project = Project.query.get(project_id)

    if not project:

        return jsonify({
            'message': 'Project not found'
        }), 404

    # -----------------------------------
    # CHECK USER
    # -----------------------------------

    user = User.query.get(user_id)

    if not user:

        return jsonify({
            'message': 'User not found'
        }), 404

    # -----------------------------------
    # CHECK DUPLICATE MEMBER
    # -----------------------------------

    existing_member = TeamMember.query.filter_by(
        project_id=project_id,
        user_id=user_id
    ).first()

    if existing_member:

        return jsonify({
            'message': 'User already added'
        }), 409

    # -----------------------------------
    # ADD MEMBER
    # -----------------------------------

    new_member = TeamMember(
        project_id=project_id,
        user_id=user_id
    )

    db.session.add(new_member)
    db.session.commit()

    return jsonify({
        'message': 'Member added successfully'
    }), 201

@auth.route('/create-task', methods=['POST'])
@jwt_required()
def create_task():

    claims = get_jwt()

    current_user_role = claims['role']

    # -----------------------------------
    # ADMIN CHECK
    # -----------------------------------

    if current_user_role != 'admin':

        return jsonify({
            'message': 'Only admin can create tasks'
        }), 403

    # -----------------------------------
    # GET DATA
    # -----------------------------------

    data = request.get_json()

    title = data.get('title')
    description = data.get('description')
    due_date = data.get('due_date')
    project_id = data.get('project_id')
    assigned_to = data.get('assigned_to')

    # -----------------------------------
    # VALIDATION
    # -----------------------------------

    if not title:
        return jsonify({
            'message': 'Task title is required'
        }), 400

    if not project_id:
        return jsonify({
            'message': 'Project ID required'
        }), 400

    if not assigned_to:
        return jsonify({
            'message': 'Assigned user required'
        }), 400

    # -----------------------------------
    # CHECK PROJECT
    # -----------------------------------

    project = Project.query.get(project_id)

    if not project:
        return jsonify({
            'message': 'Project not found'
        }), 404

    # -----------------------------------
    # CHECK USER
    # -----------------------------------

    user = User.query.get(assigned_to)

    if not user:
        return jsonify({
            'message': 'User not found'
        }), 404

    # -----------------------------------
    # CREATE TASK
    # -----------------------------------

    new_task = Task(
        title=title,
        description=description,
        due_date=due_date,
        project_id=project_id,
        assigned_to=assigned_to
    )

    db.session.add(new_task)
    db.session.commit()

    return jsonify({
        'message': 'Task created successfully'
    }), 201

@auth.route('/my-tasks', methods=['GET'])
@jwt_required()
def my_tasks():

    current_user_id = get_jwt_identity()

    tasks = Task.query.filter_by(
        assigned_to=current_user_id
    ).all()

    task_list = []

    for task in tasks:

        task_list.append({
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'status': task.status,
            'due_date': str(task.due_date)
        })

    return jsonify(task_list), 200


@auth.route('/update-task-status/<int:id>', methods=['PUT'])
@jwt_required()
def update_task_status(id):

    current_user_id = get_jwt_identity()

    # -----------------------------------
    # FIND TASK
    # -----------------------------------

    task = Task.query.filter_by(
        id=id,
        assigned_to=current_user_id
    ).first()

    # -----------------------------------
    # TASK NOT FOUND
    # -----------------------------------

    if not task:

        return jsonify({
            'message': (
                'Task not found or not assigned to you'
            )
        }), 404

    # -----------------------------------
    # GET REQUEST DATA
    # -----------------------------------

    data = request.get_json()

    status = data.get('status')

    # -----------------------------------
    # VALID STATUS CHECK
    # -----------------------------------

    valid_status = [
        'pending',
        'in_progress',
        'completed'
    ]

    if status not in valid_status:

        return jsonify({
            'message': 'Invalid task status'
        }), 400

    # -----------------------------------
    # UPDATE STATUS
    # -----------------------------------

    task.status = status

    db.session.commit()

    # -----------------------------------
    # RESPONSE
    # -----------------------------------

    return jsonify({
        'message': 'Task status updated successfully',
        'new_status': task.status
    }), 200
    


    







# =========================================================
# EMPLOYEE DASHBOARD
# =========================================================

@auth.route('/employee-dashboard', methods=['GET'])
@jwt_required()
def employee_dashboard():

    current_user_id = get_jwt_identity()

    # -------------------------------------------------
    # USER INFO
    # -------------------------------------------------

    user = User.query.get(current_user_id)

    # -------------------------------------------------
    # TASK COUNTS
    # -------------------------------------------------

    total_tasks = Task.query.filter_by(
        assigned_to=current_user_id
    ).count()

    completed_tasks = Task.query.filter_by(
        assigned_to=current_user_id,
        status='completed'
    ).count()

    in_progress_tasks = Task.query.filter_by(
        assigned_to=current_user_id,
        status='in_progress'
    ).count()

    pending_tasks = Task.query.filter_by(
        assigned_to=current_user_id,
        status='pending'
    ).count()

    # -------------------------------------------------
    # OVERDUE TASKS
    # -------------------------------------------------

    overdue_tasks = Task.query.filter(
        Task.assigned_to == current_user_id,
        Task.due_date < date.today(),
        Task.status != 'completed'
    ).count()

    # -------------------------------------------------
    # PROGRESS %
    # -------------------------------------------------

    progress_percentage = 0

    if total_tasks > 0:

        progress_percentage = (
            completed_tasks / total_tasks
        ) * 100

    # -------------------------------------------------
    # MY TASKS
    # -------------------------------------------------

    tasks = Task.query.filter_by(
        assigned_to=current_user_id
    ).all()

    task_list = []

    for task in tasks:

        project = Project.query.get(
            task.project_id
        )

        task_list.append({

            'task_id': task.id,

            'project_name': (
                project.title
                if project else None
            ),

            'task_title': task.title,

            'task_description': task.description,

            'status': task.status,

            'due_date': (
                str(task.due_date)
                if task.due_date else None
            ),

            'assigned_date': (
                str(task.created_at)
                if task.created_at else None
            )
        })

    # -------------------------------------------------
    # PROJECTS I'M WORKING ON
    # -------------------------------------------------

    project_ids = db.session.query(
        Task.project_id
    ).filter_by(
        assigned_to=current_user_id
    ).distinct().all()

    projects_data = []

    for project_id in project_ids:

        project = Project.query.get(
            project_id[0]
        )

        if project:

            total_project_tasks = Task.query.filter_by(
                project_id=project.id,
                assigned_to=current_user_id
            ).count()

            completed_project_tasks = Task.query.filter_by(
                project_id=project.id,
                assigned_to=current_user_id,
                status='completed'
            ).count()

            progress = 0

            if total_project_tasks > 0:

                progress = (
                    completed_project_tasks /
                    total_project_tasks
                ) * 100

            projects_data.append({

                'project_id': project.id,

                'project_name': project.title,

                'progress_percentage': round(
                    progress,
                    2
                )
            })

    # -------------------------------------------------
    # RESPONSE
    # -------------------------------------------------

    return jsonify({

        'employee': {

            'id': user.id,
            'name': user.name,
            'email': user.email,
            'role': user.role
        },

        'dashboard_summary': {

            'total_tasks': total_tasks,

            'completed_tasks': completed_tasks,

            'in_progress_tasks': in_progress_tasks,

            'pending_tasks': pending_tasks,

            'overdue_tasks': overdue_tasks,

            'progress_percentage': round(
                progress_percentage,
                2
            )
        },

        'my_tasks': task_list,

        'projects_working_on': projects_data

    }), 200



# =========================================================
# ADMIN DASHBOARD
# =========================================================

@auth.route('/admin-dashboard', methods=['GET'])
@jwt_required()
def admin_dashboard():

    claims = get_jwt()

    current_user_role = claims['role']

    # -------------------------------------------------
    # ADMIN CHECK
    # -------------------------------------------------

    if current_user_role != 'admin':

        return jsonify({
            'message': 'Only admin can access dashboard'
        }), 403

    # -------------------------------------------------
    # TOTAL COUNTS
    # -------------------------------------------------

    total_projects = Project.query.count()

    total_members = User.query.filter_by(
        role='member'
    ).count()

    total_tasks = Task.query.count()

    completed_tasks = Task.query.filter_by(
        status='completed'
    ).count()

    in_progress_tasks = Task.query.filter_by(
        status='in_progress'
    ).count()

    pending_tasks = Task.query.filter_by(
        status='pending'
    ).count()

    overdue_tasks = Task.query.filter(
        Task.due_date < date.today(),
        Task.status != 'completed'
    ).count()

    # -------------------------------------------------
    # OVERALL PROGRESS
    # -------------------------------------------------

    overall_progress = 0

    if total_tasks > 0:

        overall_progress = (
            completed_tasks / total_tasks
        ) * 100

    # -------------------------------------------------
    # RECENT TASKS
    # -------------------------------------------------

    recent_tasks = Task.query.order_by(
        Task.created_at.desc()
    ).limit(10).all()

    recent_task_list = []

    for task in recent_tasks:

        project = Project.query.get(
            task.project_id
        )

        user = User.query.get(
            task.assigned_to
        )

        recent_task_list.append({

            'task_id': task.id,

            'task_title': task.title,

            'project_name': (
                project.title
                if project else None
            ),

            'assigned_to': (
                user.name
                if user else None
            ),

            'status': task.status,

            'due_date': (
                str(task.due_date)
                if task.due_date else None
            ),

            'assigned_date': (
                str(task.created_at)
                if task.created_at else None
            )
        })

    # -------------------------------------------------
    # PROJECT OVERVIEW
    # -------------------------------------------------

    projects = Project.query.all()

    project_overview = []

    for project in projects:

        total_project_tasks = Task.query.filter_by(
            project_id=project.id
        ).count()

        completed_project_tasks = Task.query.filter_by(
            project_id=project.id,
            status='completed'
        ).count()

        progress = 0

        if total_project_tasks > 0:

            progress = (
                completed_project_tasks /
                total_project_tasks
            ) * 100

        project_overview.append({

            'project_id': project.id,

            'project_name': project.title,

            'total_tasks': total_project_tasks,

            'progress_percentage': round(
                progress,
                2
            )
        })

    # -------------------------------------------------
    # TASK STATUS OVERVIEW
    # -------------------------------------------------

    task_status_overview = {

        'completed_percentage': round(
            (completed_tasks / total_tasks) * 100,
            2
        ) if total_tasks > 0 else 0,

        'in_progress_percentage': round(
            (in_progress_tasks / total_tasks) * 100,
            2
        ) if total_tasks > 0 else 0,

        'pending_percentage': round(
            (pending_tasks / total_tasks) * 100,
            2
        ) if total_tasks > 0 else 0,

        'overdue_percentage': round(
            (overdue_tasks / total_tasks) * 100,
            2
        ) if total_tasks > 0 else 0
    }

    # -------------------------------------------------
    # RESPONSE
    # -------------------------------------------------

    return jsonify({

        'dashboard_summary': {

            'total_projects': total_projects,

            'total_members': total_members,

            'total_tasks': total_tasks,

            'completed_tasks': completed_tasks,

            'in_progress_tasks': in_progress_tasks,

            'pending_tasks': pending_tasks,

            'overdue_tasks': overdue_tasks,

            'overall_progress': round(
                overall_progress,
                2
            )
        },

        'task_status_overview': task_status_overview,

        'recent_tasks': recent_task_list,

        'projects_overview': project_overview

    }), 200


