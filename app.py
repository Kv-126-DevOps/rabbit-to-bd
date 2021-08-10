import sys
from types import SimpleNamespace

import pika
import pika.exceptions
import json

from sqlalchemy import create_engine
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import sessionmaker

from config import *
from models import *
from testdata import opened, other

engine = create_engine(DB_URL)
dbSession = sessionmaker(bind=engine)


def main():
    """RabbitMQ integration Component"""
    credentials = pika.PlainCredentials(username=RABBIT_USER, password=RABBIT_PW)
    parameters = pika.ConnectionParameters()
    parameters.host = RABBIT_HOST
    parameters.port = RABBIT_PORT
    # parameters.virtual_host
    parameters.credentials = credentials

    def callback(channel, method, properties, body):
        if method.message_count:
            data = parseJson(body.decode())
            if data.action == 'opened':
                addIssueActionLabelStateCommands(body.decode())
                print(f"{data.issue.id} is {data.action} added")
            else:
                if isIssueExist(data.issue.id):
                    sessionAddIssueActionState = dbSession()
                    sessionAddIssueActionState.expire_on_commit = False
                    addIssueActionState(body.decode())
                    print(f"{data.issue.id} is {data.action} updated")
                else:
                    print(f"{data.issue.id} not found")
            channel.basic_ack(delivery_tag=method.delivery_tag)

    while True:
        try:
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()
            channel.basic_qos(prefetch_count=1)
            channel.queue_declare(queue=RABBIT_QUEUE, durable=False, auto_delete=True)
            channel.basic_consume(RABBIT_QUEUE, callback)
            try:
                channel.start_consuming()
            except KeyboardInterrupt:
                channel.stop_consuming()
                connection.close()
                break
        except pika.exceptions.ConnectionClosedByBroker:
            continue
        except pika.exceptions.AMQPChannelError as ex:
            print(f"Caught a channel error: {ex}, stopping...")
            break
        except pika.exceptions.AMQPConnectionError:
            print("Connection was closed, retrying...")
            continue
        except Exception as ex:
            print(ex)


def parseJson(dataJson: str) -> SimpleNamespace:
    """
    The function converts a string to a dictionary.

    :param dataJson: str
    :return: SimpleNamespace
    """
    return json.loads(dataJson, object_hook=lambda d: SimpleNamespace(**d))


def addUser(dataJson: str) -> User:
    """
    The function checks for the existence of a User
    record in the db, if there is none, the record is added.

    :param dataJson: str
    :return: User from models
    """

    data = parseJson(dataJson)
    user = User(UserId=data.issue.user.login,
                HtmlUrl=data.issue.user.html_url,
                AvatarUrl=data.issue.user.avatar_url)
    sessionAddUser = dbSession()
    sessionAddUser.expire_on_commit = False
    query = sessionAddUser.query(User).filter(User.UserId == user.UserId)
    try:
        user = query.one()
        print(f"Function addUser() - user exists")
    except NoResultFound:
        sessionAddUser.add(user)
        print(f"Function addUser() - user added")
    finally:
        sessionAddUser.commit()
        print(f"{user}")
        return user


def addAction(dataJson: str) -> Action:
    """
    The function checks for the existence of a Action
    record in the db, if there is none, the record is added.

    :param dataJson: str
    :return: Action from models
    """
    data = parseJson(dataJson)
    action = Action(Title=data.action)
    sessionAddAction = dbSession()
    sessionAddAction.expire_on_commit = False
    query = sessionAddAction.query(Action).filter(Action.Title == action.Title)
    try:
        action = query.one()
        print(f"Function addAction() - action exist")
    except NoResultFound:
        sessionAddAction.add(action)
        print(f"Function addAction() - action added")
    finally:
        sessionAddAction.commit()
        print(f"{action}")
        return action


def addState(dataJson: str) -> State:
    """
    The function checks for the existence of a State
    record in the db, if there is none, the record is added.

    :param dataJson: str
    :return: State from models
    """
    data = parseJson(dataJson)

    state = State(Title=data.issue.state)

    sessionAddAction = dbSession()
    sessionAddAction.expire_on_commit = False
    query = sessionAddAction.query(State).filter(State.Title == state.Title)

    try:
        state = query.one()
        print(f"Function addState() - state exist")
    except NoResultFound:
        sessionAddAction.add(state)
        print(f"Function addState() - state added")
    finally:
        sessionAddAction.commit()
        print(f"{state}")
        return state


def addLabel(dataJson: str):
    """
    The function checks for the existence of a Label
    records in the db, if there is none, the records is added.

    :param dataJson: str
    :return: list Label from models
    """
    sessionAddLabel = dbSession()
    sessionAddLabel.expire_on_commit = False

    data = parseJson(dataJson)
    labels = []
    for item in data.issue.labels:
        label = Label(item.name)
        labels.append(label)
    ls = []
    for label in labels:
        query = sessionAddLabel.query(Label).filter(Label.Title == label.Title)
        try:
            label = query.one()
            ls.append(label)
            print(f"{label} - exist")
        except NoResultFound:
            sessionAddLabel.add(label)
            sessionAddLabel.commit()
            ls.append(label)
            print(f"{label} - added")
    sessionAddLabel.commit()
    return ls


def addIssue(dataJson: str) -> Issue:
    """
    The function checks for the existence of a Issue
    records in the db, if there is none, the records is added.

    :param dataJson: str
    :return: Issue from models
    """
    data = parseJson(dataJson)
    issue = Issue(IssueId=data.issue.id,
                  HtmlUrl=data.issue.html_url,
                  Number=data.issue.number,
                  Title=data.issue.title,
                  Body=data.issue.body)

    sessionAddIssue = dbSession()
    query = sessionAddIssue.query(Issue).filter(Issue.IssueId == issue.IssueId)
    try:
        issue = query.one()
        print(f"Function addIssue() - issue exist")
    except NoResultFound:
        sessionAddIssue.add(issue)
        print(f"Function addIssue() - issue added")
    finally:
        sessionAddIssue.commit()
        print(f"{issue}")
    return issue


def addIssueActionLabelStateCommands(dataJson: str):
    """
    The function checks for the existence of a User, Issue,
    Action, State, Label records in the db, if there is none,
    the records is added. And adds records to the IssueAction,
    IssueState, IssueLabel tables.

    :param dataJson: str
    :return: None
    """
    addUser(dataJson)
    data = parseJson(dataJson)
    issue = Issue(IssueId=data.issue.id,
                  HtmlUrl=data.issue.html_url,
                  Number=data.issue.number,
                  Title=data.issue.title,
                  Body=data.issue.body)

    sessionAddIssueActionLabelState = dbSession()
    sessionAddIssueActionLabelState.expire_on_commit = False
    query = sessionAddIssueActionLabelState \
        .query(Issue) \
        .filter(Issue.IssueId == issue.IssueId)
    try:
        issue = query.one()
        print(f"Function addIssueActionLabelState() - issue exist")
    except NoResultFound:
        issueAction = IssueAction(UserId=data.issue.user.login,
                                  ModifiedDate=data.issue.data)
        issueAction.Action = addAction(dataJson)
        issue.Actions.append(issueAction)

        issueState = IssueState(ModifiedDate=data.issue.data)
        issueState.State = addState(dataJson)
        issue.States.append(issueState)
        labels = []
        for label in addLabel(dataJson):
            labels.append(label)

        for label in labels:
            issueLabel = IssueLabel()
            issueLabel.IssueId = issue.IssueId
            issueLabel.LabelId = label.LabelId
            sessionAddIssueActionLabelState.add(issueLabel)
        sessionAddIssueActionLabelState.add(issue)
        print(f"Function addIssueActionLabelState() - issue added")
    finally:
        sessionAddIssueActionLabelState.commit()
        print(f"{issue}")


def isIssueExist(issueId):
    isExist = False
    sessionIsIssueExist = dbSession()
    sessionIsIssueExist.expire_on_commit = False
    query = sessionIsIssueExist \
        .query(Issue) \
        .filter(Issue.IssueId == issueId)
    try:
        query.one()
        isExist = True
    except NoResultFound:
        isExist = False
    finally:
        sessionIsIssueExist.commit()
        return isExist


def addIssueActionState(dataJson: str):
    """
    The function checks for the existence of a User, Issue,
    Action, State records in the db, if there is none,
    the records is added. And adds records to the IssueAction,
    IssueState tables.

    :param dataJson: str
    :return: None
    """

    addUser(dataJson)
    data = parseJson(dataJson)

    if isIssueExist(data.issue.id):
        sessionAddIssueActionState = dbSession()
        sessionAddIssueActionState.expire_on_commit = False
        query = sessionAddIssueActionState \
            .query(Issue) \
            .filter(Issue.IssueId == data.issue.id)
        try:
            issue = query.one()
            issueAction = IssueAction(UserId=data.issue.user.login,
                                      ModifiedDate=data.issue.data)
            issueAction.Action = addAction(dataJson)
            issue.Actions.append(issueAction)

            issueState = IssueState(ModifiedDate=data.issue.data)
            issueState.State = addState(dataJson)
            issue.States.append(issueState)
            sessionAddIssueActionState.add(issue)
        except NoResultFound as ex:
            print(ex)
        finally:
            sessionAddIssueActionState.commit()
    else:
        print(f"Issue {data.issue.id} not found")


# addIssueActionLabelStateCommands(opened)
# addIssueActionState(other)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            exit(0)
