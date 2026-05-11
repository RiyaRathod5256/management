from extensions import db

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(
        db.String(200),
        nullable=False
    )

    description = db.Column(
        db.Text
    )

    status = db.Column(
        db.Enum(
            'pending',
            'in_progress',
            'completed'
        ),
        default='pending'
    )

    due_date = db.Column(
        db.Date
    )

    project_id = db.Column(
        db.Integer,
        db.ForeignKey('projects.id')
    )

    assigned_to = db.Column(
        db.Integer,
        db.ForeignKey('users.id')
    )

    created_at = db.Column(
        db.TIMESTAMP,
        server_default=db.func.current_timestamp()
    )