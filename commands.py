from sqlalchemy import and_
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import scoped_session

from db import *
from models import *

Session = scoped_session(session_factory)


def addUserCommand(user: User) -> User:
    """
    The function checks for the existence of a User
    record in the db, if there is none, the record is added.

    :param user:
    :return: User from models
    """
    query = Session.query(User).filter(User.UserId == user.UserId)
    try:
        user = query.one()
        print(f"Function addUser() - user exists")
    except NoResultFound:
        Session.add(user)
        print(f"Function addUser() - user added")
    finally:
        Session.commit()
        print(f"{user}")
        return user


def addActionCommand(action: Action) -> Action:
    """
    The function checks for the existence of a Action
    record in the db, if there is none, the record is added.

    :param action:
    :return: Action from models
    """
    query = Session.query(Action).filter(Action.Title == action.Title)
    try:
        action = query.one()
        print(f"Function addAction() - action exist")
    except NoResultFound:
        Session.add(action)
        print(f"Function addAction() - action added")
    finally:
        Session.commit()
        print(f"{action}")
        return action


def addStateCommand(state: State) -> State:
    """
    The function checks for the existence of a State
    record in the db, if there is none, the record is added.

    :param state:
    :return: State from models
    """

    query = Session.query(State).filter(State.Title == state.Title)

    try:
        state = query.one()
        print(f"Function addState() - state exist")
    except NoResultFound:
        Session.add(state)
        print(f"Function addState() - state added")
    finally:
        Session.commit()
        print(f"{state}")
        return state


def addLabelCommand(label: Label):
    query = Session.query(Label).filter(Label.Title == label.Title)

    try:
        label = query.one()
        print(f"Function addLabelCommand() - {label} exist")
    except NoResultFound:
        Session.add(label)
        print(f"Function addState() - {label} added")
    finally:
        Session.commit()
        print(f"{label}")
        return label


def addLabelsCommand(labels: []):
    """
    The function checks for the existence of a Label
    records in the db, if there is none, the records is added.

    :param labels:
    :return: list Label from models
    """

    for label in labels:
        query = Session.query(Label).filter(Label.Title == label.Title)
        try:
            label = query.one()
            print(f"{label} - exist")
        except NoResultFound:
            Session.add(label)
            Session.commit()
            print(f"{label} - added")
    Session.commit()
    return labels


def addIssueCommand(issue: Issue) -> Issue:
    """
    The function checks for the existence of a Issue
    records in the db, if there is none, the records is added.

    :param issue:
    :return: Issue from models
    """

    query = Session.query(Issue).filter(Issue.IssueId == issue.IssueId)
    try:
        issue = query.one()
        print(f"Function addIssue() - issue exist")
    except NoResultFound:
        Session.add(issue)
        print(f"Function addIssue() - issue added")
    finally:
        Session.commit()
        print(f"{issue}")
    return issue


def addIssueActionCommand(issueAction: IssueAction):
    query = Session.query(IssueAction) \
            .filter((IssueAction.IssueId == issueAction.IssueId)
                    & (IssueAction.ActionId == issueAction.ActionId)
                    & (IssueAction.ModifiedDate == issueAction.ModifiedDate))
    try:
        issueAction = query.one()
        print(f"Function addIssueAction() - issueAction exist")
    except NoResultFound:
        Session.add(issueAction)
        print(f"Function addIssueAction() - issueAction added")
    finally:
        Session.commit()
        print(f"{issueAction}")
    return issueAction


def addIssueStateCommand(issueState: IssueState):
    query = Session.query(IssueState).filter(and_(IssueState.IssueId == issueState.IssueId,
                                                  IssueState.StateId == issueState.StateId,
                                                  IssueState.ModifiedDate == issueState.ModifiedDate))
    try:
        issueState = query.one()
        print(f"Function addIssueState() - {issueState} exist")
    except NoResultFound:
        Session.add(issueState)
        print(f"Function addIssueState() - {issueState} added")
    finally:
        Session.commit()
        print(f"{issueState}")
    return issueState


def addIssueLabelsCommand(issue: Issue, labels: []):
    issueLabels = []
    for label in labels:
        issueLabel = IssueLabel(IssueId=issue.IssueId, LabelId=label.LabelId)
        Session.add(issueLabel)
        issueLabels.append(issueLabel)
        print(f"Function addIssueLabels() - {issueLabel} added")
    Session.commit()
    return issueLabels


def addNewIssueToDB(data):
    """
    The function checks for the existence of a User, Issue,
    Action, State, Label records in the db, if there is none,
    the records is added. And adds records to the IssueAction,
    IssueState, IssueLabel tables.

    :param dataJson: str
    :return: None
    """

    if data.action == 'opened' and not isIssueExist(data.issue.id):
        addUserCommand(User(UserId=data.issue.user.login,
                            HtmlUrl=data.issue.user.html_url,
                            AvatarUrl=data.issue.user.avatar_url))

        issue = addIssueCommand(Issue(IssueId=data.issue.id,
                                      HtmlUrl=data.issue.html_url,
                                      Number=data.issue.number,
                                      Title=data.issue.title,
                                      Body=data.issue.body))

        action = addActionCommand(Action(Title=data.action))

        state = addStateCommand(State(Title=data.issue.state))

        issueAction = IssueAction(IssueId=issue.IssueId,
                                  ActionId=action.ActionId,
                                  UserId=data.issue.user.login,
                                  ModifiedDate=data.issue.data)

        issueState = IssueState(IssueId=issue.IssueId,
                                StateId=state.StateId,
                                ModifiedDate=data.issue.data)

        addIssueActionCommand(issueAction)
        addIssueStateCommand(issueState)
        labels = []
        for label in data.issue.labels:
            newLabel = Label(Title=label.name)
            labels.append(addLabelCommand(newLabel))

        addLabelsCommand(labels)

        addIssueLabelsCommand(issue, labels)


def updateIssue(data):
    user = addUserCommand(User(UserId=data.issue.user.login,
                               HtmlUrl=data.issue.user.html_url,
                               AvatarUrl=data.issue.user.avatar_url))
    issueId = data.issue.id
    action = addActionCommand(Action(Title=data.action))

    state = addStateCommand(State(Title=data.issue.state))

    issueAction = IssueAction(IssueId=issueId,
                              ActionId=action.ActionId,
                              UserId=data.issue.user.login,
                              ModifiedDate=data.issue.data)

    issueState = IssueState(IssueId=issueId,
                            StateId=state.StateId,
                            ModifiedDate=data.issue.data)

    addIssueActionCommand(issueAction)
    addIssueStateCommand(issueState)


def isIssueExist(issueId):
    isExist = False
    query = Session \
        .query(Issue) \
        .filter(Issue.IssueId == issueId)
    try:
        query.one()
        isExist = True
    except NoResultFound:
        isExist = False
    finally:
        Session.commit()
        return isExist
