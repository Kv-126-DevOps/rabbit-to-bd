from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'Users'
    UserId = Column(String(32), primary_key=True)
    HtmlUrl = Column(String(512), unique=True)
    AvatarUrl = Column(String(512), unique=True)
    IssueActions = relationship("IssueAction")

    def __init__(self, UserId, HtmlUrl, AvatarUrl):
        self.UserId = UserId
        self.HtmlUrl = HtmlUrl
        self.AvatarUrl = AvatarUrl

    def __repr__(self):
        return f"UserId: {self.UserId}, HtmlUrl: {self.HtmlUrl}, AvatarUrl: {self.AvatarUrl}"


class IssueAction(Base):
    __tablename__ = 'IssueActions'
    IssueId = Column(ForeignKey('Issues.IssueId'), primary_key=True)
    ActionId = Column(ForeignKey('Actions.ActionId'), primary_key=True)
    UserId = Column(String(32), ForeignKey('Users.UserId'))
    ModifiedDate = Column(DateTime)
    Action = relationship("Action")

    def __init__(self, IssueId, ActionId, UserId, ModifiedDate):
        self.IssueId = IssueId
        self.ActionId = ActionId
        self.UserId = UserId
        self.ModifiedDate = ModifiedDate

    def __repr__(self):
        return f"IssueId: {self.IssueId}, " \
               f"ActionId: {self.ActionId}, " \
               f"UserId: {self.UserId}, " \
               f"ModifiedDate: {self.ModifiedDate}"


class Issue(Base):
    __tablename__ = 'Issues'
    IssueId = Column(Integer, primary_key=True)
    HtmlUrl = Column(String(512))
    Number = Column(Integer)
    Title = Column(String(32))
    Body = Column(String(32))
    Actions = relationship("IssueAction")
    States = relationship("IssueState")
    Labels = relationship("IssueLabel")

    def __init__(self, IssueId):
        self.IssueId = IssueId

    def __init__(self, IssueId, HtmlUrl, Number, Title, Body):
        self.IssueId = IssueId
        self.HtmlUrl = HtmlUrl
        self.Number = Number
        self.Title = Title
        self.Body = Body

    def __repr__(self):
        return f"IssueId: {self.IssueId}, " \
               f"HtmlUrl: {self.HtmlUrl}, " \
               f"Number: {self.Number}, " \
               f"Title: {self.Title}, " \
               f"Body: {self.Body}"


class Action(Base):
    __tablename__ = 'Actions'
    ActionId = Column(Integer, primary_key=True)
    Title = Column(String(32), unique=True)

    def __init__(self, Title):
        self.Title = Title

    def __repr__(self):
        return f"ActionId: {self.ActionId}, Title: {self.Title}"


class Label(Base):
    __tablename__ = 'Labels'
    LabelId = Column(Integer, primary_key=True)
    Title = Column(String(32), unique=True)

    def __init__(self, Title):
        self.Title = Title

    def __repr__(self):
        return f"LabelId: {self.LabelId}, Title: {self.Title}"


class State(Base):
    __tablename__ = 'States'
    StateId = Column(Integer, primary_key=True)
    Title = Column(String(32), unique=True)

    def __init__(self, Title):
        self.Title = Title

    def __repr__(self):
        return f"StateId: {self.StateId}, Title: {self.Title}"


class IssueLabel(Base):
    __tablename__ = 'IssueLabels'
    IssueId = Column(ForeignKey('Issues.IssueId'), primary_key=True)
    LabelId = Column(ForeignKey('Labels.LabelId'), primary_key=True)
    Label = relationship("Label")

    def __repr__(self):
        return f"IssueId: {self.IssueId}, LabelId: {self.LabelId}"


class IssueState(Base):
    __tablename__ = 'IssueStates'
    # IssueStateId = Column(Integer, primary_key=True)
    IssueId = Column(ForeignKey('Issues.IssueId'), primary_key=True)
    StateId = Column(ForeignKey('States.StateId'), primary_key=True)
    ModifiedDate = Column(DateTime)
    State = relationship("State")

    def __init__(self, IssueId, StateId, ModifiedDate):
        self.IssueId = IssueId
        self.StateId = StateId
        self.ModifiedDate = ModifiedDate

    def __repr__(self):
        return f"IssueId: {self.IssueId}, StateId: {self.StateId}, ModifiedDate: {self.ModifiedDate}"
