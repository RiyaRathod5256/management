from extensions import db

class TeamMember(db.Model):
    __tablename__ = 'team_members'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id')
    )

    project_id = db.Column(
        db.Integer,
        db.ForeignKey('projects.id')
    )